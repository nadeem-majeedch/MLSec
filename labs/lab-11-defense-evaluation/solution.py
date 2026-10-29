"""LAB-11 reference solution: compare an undefended model with two defenses.

Run from this directory:
    python solution.py --out artifacts

Artifacts: metrics.json, run.json, report.md, manifest.json.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

SHARED = Path(__file__).resolve().parents[1] / "shared"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from mlsec_labs.artifacts import build_manifest, environment, write_json  # noqa: E402

SEED = 42
EPSILON = 0.10
STRESS_EPSILON = 0.20
TRAIN_EPSILON = 0.10
STEPS = 20
RESTARTS = 2
LEVELS = 4
ALPHA = EPSILON / 5.0


def load_data():
    X, y = load_digits(return_X_y=True)
    X = X.astype(np.float64) / 16.0
    return train_test_split(X, y, test_size=0.3, random_state=SEED, stratify=y)


def fit_clean(X_train, y_train):
    return LogisticRegression(max_iter=5000, C=1.0).fit(X_train, y_train)


def probabilities(model, X):
    scores = X @ model.coef_.T + model.intercept_
    scores -= scores.max(axis=1, keepdims=True)
    exp = np.exp(scores)
    return exp / exp.sum(axis=1, keepdims=True)


def input_gradient(model, X, y):
    p = probabilities(model, X)
    p[np.arange(len(y)), y] -= 1.0
    return p @ model.coef_


def squeeze(X, levels=LEVELS):
    """Input squeezing: snap every pixel to a coarse grid in [0, 1]."""
    return np.clip(np.round(X * (levels - 1)) / (levels - 1), 0.0, 1.0)


def adversarial_train(baseline, X_train, y_train, epsilon=TRAIN_EPSILON, steps=10, seed=SEED):
    """Augment the training set with PGD examples and refit."""
    X_adv_train = pgd(
        baseline, X_train, y_train, epsilon=epsilon,
        alpha=epsilon / 5.0, steps=steps, restarts=1, seed=seed,
    )
    return LogisticRegression(max_iter=5000, C=0.01).fit(
        np.vstack([X_train, X_adv_train]), np.concatenate([y_train, y_train])
    )


def pgd(model, X, y, epsilon=EPSILON, alpha=ALPHA, steps=STEPS, restarts=RESTARTS, seed=SEED):
    """Standard PGD on the raw input, keeping the best restart per row."""
    if epsilon == 0.0:
        return X.copy()
    rng = np.random.default_rng(seed)
    best = X.copy()
    best_success = np.zeros(len(y), dtype=bool)
    for restart in range(restarts):
        x_adv = X.copy()
        if restart:
            x_adv = np.clip(X + rng.uniform(-epsilon, epsilon, X.shape), 0.0, 1.0)
        for _ in range(steps):
            x_adv = np.clip(
                x_adv + alpha * np.sign(input_gradient(model, x_adv, y)),
                X - epsilon,
                X + epsilon,
            )
            x_adv = np.clip(x_adv, 0.0, 1.0)
        success = model.predict(x_adv) != y
        update = success & ~best_success
        best[update] = x_adv[update]
        best_success |= success
    return best


def pgd_squeezed_bpda(model, X, y, epsilon=EPSILON, alpha=ALPHA, steps=STEPS, restarts=RESTARTS, seed=SEED):
    """Adaptive attack against input squeezing with a straight-through gradient.

    Forward pass applies the quantizer; backward pass uses the identity
    Jacobian (BPDA), because the true derivative of a rounding step is zero
    almost everywhere and would stop the attack for the wrong reason.
    """
    if epsilon == 0.0:
        return X.copy()
    rng = np.random.default_rng(seed)
    best = X.copy()
    best_success = np.zeros(len(y), dtype=bool)
    for restart in range(restarts):
        x_adv = X.copy()
        if restart:
            x_adv = np.clip(X + rng.uniform(-epsilon, epsilon, X.shape), 0.0, 1.0)
        for _ in range(steps):
            grad = input_gradient(model, squeeze(x_adv), y)
            x_adv = np.clip(
                x_adv + alpha * np.sign(grad),
                X - epsilon,
                X + epsilon,
            )
            x_adv = np.clip(x_adv, 0.0, 1.0)
        success = model.predict(squeeze(x_adv)) != y
        update = success & ~best_success
        best[update] = x_adv[update]
        best_success |= success
    return best


def summarize(predict, X, y, X_eval, clean_correct):
    pred = predict(X_eval)
    success = pred[clean_correct] != y[clean_correct]
    delta = X_eval - X
    return {
        "clean_accuracy": float(clean_correct.mean()),
        "base_size": int(clean_correct.sum()),
        "asr": float(success.mean()),
        "robust_accuracy": float((pred == y).mean()),
        "mean_linf": float(np.abs(delta).max(axis=1).mean()),
        "max_linf": float(np.abs(delta).max()),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare clean, adversarially trained, and squeezed models.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    X_train, X_test, y_train, y_test = load_data()
    baseline = fit_clean(X_train, y_train)

    adv_model = adversarial_train(baseline, X_train, y_train)

    clean_pred = baseline.predict(X_test)
    clean_correct = clean_pred == y_test
    adv_pred = adv_model.predict(X_test)
    adv_clean_correct = adv_pred == y_test
    squeeze_pred = baseline.predict(squeeze(X_test))
    squeeze_clean_correct = squeeze_pred == y_test

    base_adv = pgd(baseline, X_test, y_test)
    adv_attack = pgd(adv_model, X_test, y_test)
    naive_adv = base_adv
    adaptive_adv = pgd_squeezed_bpda(baseline, X_test, y_test)

    stress_base = pgd(baseline, X_test, y_test, epsilon=STRESS_EPSILON, alpha=STRESS_EPSILON / 5.0)
    stress_adv = pgd(adv_model, X_test, y_test, epsilon=STRESS_EPSILON, alpha=STRESS_EPSILON / 5.0)
    stress_naive = pgd(baseline, X_test, y_test, epsilon=STRESS_EPSILON, alpha=STRESS_EPSILON / 5.0)
    stress_adaptive = pgd_squeezed_bpda(
        baseline, X_test, y_test, epsilon=STRESS_EPSILON, alpha=STRESS_EPSILON / 5.0
    )

    def asr(pred, mask):
        return float((pred[mask] != y_test[mask]).mean())

    squeeze_pred_naive = baseline.predict(squeeze(naive_adv))
    squeeze_pred_adaptive = baseline.predict(squeeze(adaptive_adv))
    squeeze_pred_stress = baseline.predict(squeeze(stress_naive))
    squeeze_pred_stress_adaptive = baseline.predict(squeeze(stress_adaptive))

    metrics = {
        "dataset": "sklearn.datasets.load_digits (8x8, pixels/16)",
        "test_size": int(len(y_test)),
        "epsilon": EPSILON,
        "stress_epsilon": STRESS_EPSILON,
        "train_epsilon": TRAIN_EPSILON,
        "attack": {"steps": STEPS, "alpha": ALPHA, "restarts": RESTARTS},
        "squeeze_levels": LEVELS,
        "baseline": summarize(baseline.predict, X_test, y_test, base_adv, clean_correct),
        "adversarial_training": summarize(adv_model.predict, X_test, y_test, adv_attack, adv_clean_correct),
        "input_squeezing": {
            "clean_accuracy": float(squeeze_clean_correct.mean()),
            "base_size": int(squeeze_clean_correct.sum()),
            "asr": asr(squeeze_pred_naive, squeeze_clean_correct),
            "robust_accuracy": float((squeeze_pred_naive == y_test).mean()),
            "mean_linf": float(np.abs(naive_adv - X_test).max(axis=1).mean()),
            "max_linf": float(np.abs(naive_adv - X_test).max()),
            "naive_asr": asr(squeeze_pred_naive, squeeze_clean_correct),
            "adaptive_asr": asr(squeeze_pred_adaptive, squeeze_clean_correct),
            "adaptive_robust_accuracy": float((squeeze_pred_adaptive == y_test).mean()),
            "stress_naive_asr": asr(squeeze_pred_stress, squeeze_clean_correct),
            "stress_adaptive_asr": asr(squeeze_pred_stress_adaptive, squeeze_clean_correct),
            "stress_robust_accuracy": float((squeeze_pred_stress_adaptive == y_test).mean()),
        },
        "stress": {
            "epsilon": STRESS_EPSILON,
            "baseline": summarize(
                baseline.predict, X_test, y_test, stress_base, clean_correct
            ),
            "adversarial_training": summarize(
                adv_model.predict, X_test, y_test, stress_adv, adv_clean_correct
            ),
        },
    }
    # The naive and adaptive attacks start from the same rows, so the naive ASR
    # above and the adaptive ASR below share one denominator.
    metrics["input_squeezing"]["asr"] = metrics["input_squeezing"]["naive_asr"]

    write_json(args.out / "metrics.json", metrics)
    write_json(
        args.out / "run.json",
        {
            "lab": "LAB-11",
            "seed": args.seed,
            "epsilon": EPSILON,
            "steps": STEPS,
            "restarts": RESTARTS,
            "squeeze_levels": LEVELS,
            "environment": environment(),
        },
    )
    (args.out / "report.md").write_text(build_report(metrics), encoding="utf-8", newline="\n")
    write_json(
        args.out / "manifest.json",
        build_manifest(args.out, ["metrics.json", "run.json", "report.md"]),
    )
    for name in ("baseline", "adversarial_training", "input_squeezing"):
        block = metrics[name]
        print(
            f"{name}: clean={block['clean_accuracy']:.4f} "
            f"robust={block['robust_accuracy']:.4f} asr={block['asr']:.4f}"
        )
    print(f"input squeezing adaptive asr={metrics['input_squeezing']['adaptive_asr']:.4f}")
    print(f"artifacts written to {args.out}")


def build_report(metrics):
    squeeze_block = metrics["input_squeezing"]
    lines = [
        "# LAB-11 report — defense evaluation",
        "",
        f"PGD budget epsilon={metrics['epsilon']:.2f}, steps={metrics['attack']['steps']}, "
        f"restarts={metrics['attack']['restarts']}. Success uses each model's clean-correct base set.",
        "",
        "| Model | Clean accuracy | Robust accuracy | ASR | Base set |",
        "|---|---:|---:|---:|---:|",
        f"| Undefended | {metrics['baseline']['clean_accuracy']:.4f} | "
        f"{metrics['baseline']['robust_accuracy']:.4f} | {metrics['baseline']['asr']:.4f} | "
        f"{metrics['baseline']['base_size']} |",
        f"| Adversarial training | {metrics['adversarial_training']['clean_accuracy']:.4f} | "
        f"{metrics['adversarial_training']['robust_accuracy']:.4f} | "
        f"{metrics['adversarial_training']['asr']:.4f} | {metrics['adversarial_training']['base_size']} |",
        f"| Input squeezing | {squeeze_block['clean_accuracy']:.4f} | "
        f"{squeeze_block['robust_accuracy']:.4f} | {squeeze_block['asr']:.4f} | "
        f"{squeeze_block['base_size']} |",
        "",
        "## Adaptive check and stress budget",
        "",
        f"At epsilon={metrics['epsilon']:.2f} the naive attack against squeezing reaches ASR "
        f"{squeeze_block['naive_asr']:.4f}; the straight-through (BPDA) adaptive attack reaches "
        f"{squeeze_block['adaptive_asr']:.4f}.",
        f"At the stress budget epsilon={metrics['stress_epsilon']:.2f}, baseline ASR is "
        f"{metrics['stress']['baseline']['asr']:.4f}, adversarially trained ASR is "
        f"{metrics['stress']['adversarial_training']['asr']:.4f}, and squeezed-model ASR is "
        f"{squeeze_block['stress_naive_asr']:.4f} ({squeeze_block['stress_adaptive_asr']:.4f} adaptive).",
        "",
        "The defense comparison is therefore budget-specific: squeezing looks helpful at the main "
        "budget and loses almost all protection at the stress budget.",
        "",
        "## Limitations",
        "",
        "- One linear model, one split, two budgets, and one attack family.",
        "- Adversarial training here is augmentation with PGD examples, not a full min-max procedure.",
        "- The BPDA attack is a demonstration, not the strongest possible adaptive attack.",
        "- No claim of general robustness outside this threat model is supported.",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    main()
