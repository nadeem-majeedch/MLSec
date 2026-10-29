"""LAB-01B reference solution: audit and repair a leaky churn baseline.

Run from this directory:
    python solution.py --out artifacts

Artifacts: data.csv, model.joblib, splits.npz, metrics.json, run.json,
manifest.json, report.md.
"""

from __future__ import annotations

import argparse
import json
import sys
from functools import partial
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score
from sklearn.model_selection import GroupKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

SHARED = Path(__file__).resolve().parents[1] / "shared"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from mlsec_labs.artifacts import build_manifest, environment, sha256_file, write_json  # noqa: E402
from mlsec_labs.data import FEATURES, make_churn_dataset  # noqa: E402
from mlsec_labs.metrics import binary_metrics, bootstrap_ci  # noqa: E402

TIER = {"A": 0, "B": 1, "C": 2}
REGION = {"N": 0, "S": 1, "E": 2, "W": 3}
LEAKY_FEATURE = "late_fee_flag"


def encode(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    out["plan_tier"] = out["plan_tier"].map(TIER)
    out["region"] = out["region"].map(REGION)
    return out


def model_pipeline(seed: int = 42) -> Pipeline:
    return Pipeline(
        [
            ("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
            ("clf", LogisticRegression(max_iter=1000, random_state=seed)),
        ]
    )


def clean_metrics(metrics: dict) -> dict:
    """Convert numpy scalars to JSON-native numbers."""
    cleaned = {}
    for key, value in metrics.items():
        if isinstance(value, (np.integer,)):
            cleaned[key] = int(value)
        elif isinstance(value, (np.floating,)):
            cleaned[key] = float(value)
        else:
            cleaned[key] = value
    return cleaned


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit the LAB-01B churn baseline.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    out = args.out
    out.mkdir(parents=True, exist_ok=True)

    df = make_churn_dataset(seed=args.seed)
    data_path = out / "data.csv"
    df.to_csv(data_path, index=False)

    # ---------- Audit ----------
    duplicate_rows = int(df.duplicated().sum())
    today = encode(df)
    univariate_auc = float(binary_metrics(df["churned"], df[LEAKY_FEATURE], 0.5)["roc_auc"])

    random_idx_tr, random_idx_te = train_test_split(
        np.arange(len(df)), test_size=0.25, random_state=args.seed, stratify=df["churned"]
    )
    random_overlap = len(
        set(df["customer_id"].iloc[random_idx_tr]) & set(df["customer_id"].iloc[random_idx_te])
    )

    # ---------- Leaky baseline: random split, preprocessing fitted on all rows ----------
    X_leaky = today[FEATURES]
    imputer_all = SimpleImputer(strategy="mean").fit(X_leaky)
    scaler_all = StandardScaler().fit(imputer_all.transform(X_leaky))
    X_leaky_scaled = scaler_all.transform(imputer_all.transform(X_leaky))
    leaky_model = LogisticRegression(max_iter=1000, random_state=args.seed).fit(
        X_leaky_scaled[random_idx_tr], df["churned"].iloc[random_idx_tr]
    )
    leaky_proba = leaky_model.predict_proba(X_leaky_scaled[random_idx_te])[:, 1]
    leaky_y = df["churned"].iloc[random_idx_te].to_numpy()
    leaky_metrics = clean_metrics(binary_metrics(leaky_y, leaky_proba, 0.5))
    leaky_threshold = float(np.quantile(leaky_proba, 0.80))
    leaky_at20 = clean_metrics(binary_metrics(leaky_y, leaky_proba, leaky_threshold))

    # ---------- Repair: deduplicate, group split by customer, honest features ----------
    clean = df.drop_duplicates().reset_index(drop=True)
    customers = clean.drop_duplicates("customer_id")[["customer_id", "churned"]]
    train_ids, rest_ids = train_test_split(
        customers, test_size=0.40, stratify=customers["churned"], random_state=args.seed
    )
    val_ids, test_ids = train_test_split(
        rest_ids, test_size=0.50, stratify=rest_ids["churned"], random_state=args.seed
    )

    frames = {}
    row_indices = {}
    for name, ids in [("train", train_ids), ("val", val_ids), ("test", test_ids)]:
        mask = clean["customer_id"].isin(ids["customer_id"])
        frames[name] = clean[mask].reset_index(drop=True)
        row_indices[name] = np.flatnonzero(mask.to_numpy())

    features = [name for name in FEATURES if name != LEAKY_FEATURE]
    model = model_pipeline(args.seed)
    model.fit(encode(frames["train"])[features], frames["train"]["churned"])

    val_proba = model.predict_proba(encode(frames["val"])[features])[:, 1]
    threshold = float(np.quantile(val_proba, 0.80))
    test_proba = model.predict_proba(encode(frames["test"])[features])[:, 1]
    test_y = frames["test"]["churned"].to_numpy()

    test_metrics = clean_metrics(binary_metrics(test_y, test_proba, threshold))
    val_metrics = clean_metrics(binary_metrics(
        frames["val"]["churned"].to_numpy(), val_proba, threshold
    ))

    precision_ci = bootstrap_ci(
        test_y, test_proba, partial(precision_score, zero_division=0), threshold, seed=args.seed
    )
    recall_ci = bootstrap_ci(
        test_y, test_proba, partial(recall_score, zero_division=0), threshold, seed=args.seed
    )

    group_cv = cross_val_score(
        model_pipeline(args.seed),
        encode(clean)[features],
        clean["churned"],
        groups=clean["customer_id"],
        cv=GroupKFold(n_splits=5),
        scoring="average_precision",
    )

    # ---------- Artifacts ----------
    joblib.dump(model, out / "model.joblib")
    np.savez_compressed(
        out / "splits.npz",
        train_rows=row_indices["train"],
        val_rows=row_indices["val"],
        test_rows=row_indices["test"],
        train_customers=train_ids["customer_id"].to_numpy(dtype="U8"),
        val_customers=val_ids["customer_id"].to_numpy(dtype="U8"),
        test_customers=test_ids["customer_id"].to_numpy(dtype="U8"),
    )

    metrics = {
        "dataset": {
            "name": "synthetic churn (mlsec_labs.make_churn_dataset)",
            "rows": int(len(df)),
            "customers": int(df["customer_id"].nunique()),
            "churn_rate": float(df["churned"].mean()),
            "sha256": sha256_file(data_path),
        },
        "audit": {
            "duplicate_rows": duplicate_rows,
            "missing_monthly_spend": int(df["monthly_spend"].isna().sum()),
            "late_fee_univariate_auc": univariate_auc,
            "late_fee_agreement": float((df[LEAKY_FEATURE] == df["churned"]).mean()),
            "random_split_customer_overlap": int(random_overlap),
        },
        "leaky_baseline": {
            "protocol": "random row split 75/25; imputer and scaler fitted on all rows; includes late_fee_flag",
            "at_0_5": leaky_metrics,
            "at_top_20_percent": leaky_at20,
        },
        "repaired": {
            "protocol": "deduplicated; customer-grouped 60/20/20; imputer and scaler fitted on train only",
            "features": features,
            "threshold": threshold,
            "split": {
                "train_rows": int(len(frames["train"])),
                "val_rows": int(len(frames["val"])),
                "test_rows": int(len(frames["test"])),
                "train_customers": int(frames["train"]["customer_id"].nunique()),
                "val_customers": int(frames["val"]["customer_id"].nunique()),
                "test_customers": int(frames["test"]["customer_id"].nunique()),
            },
            "validation": val_metrics,
            "test": test_metrics,
            "bootstrap_95": {"precision": precision_ci, "recall": recall_ci},
            "group_cv_pr_auc": {
                "folds": [float(v) for v in group_cv],
                "mean": float(group_cv.mean()),
                "std": float(group_cv.std()),
            },
        },
    }

    write_json(out / "metrics.json", metrics)
    write_json(
        out / "run.json",
        {
            "command": "python solution.py",
            "seed": args.seed,
            "environment": environment(),
            "dataset": metrics["dataset"],
            "features": features,
        },
    )
    write_json(
        out / "manifest.json",
        build_manifest(out, ["data.csv", "model.joblib", "splits.npz", "metrics.json", "run.json"]),
    )

    rep = metrics["repaired"]["test"]
    report = f"""# LAB-01B Report

## Threat model
The asset is the integrity of the reported churn metric and the decision it informs. The adversary is not a remote attacker but a validity failure: a post-outcome feature, repeated customers across a random split, and preprocessing fitted on evaluation data. Success means a repaired estimate that a second person can reproduce and that does not depend on leakage.

## Data audit
- {metrics['dataset']['rows']} rows, {metrics['dataset']['customers']} unique customers, churn rate {metrics['dataset']['churn_rate']:.3f}.
- {duplicate_rows} exact duplicate rows and {metrics['audit']['missing_monthly_spend']} missing `monthly_spend` values.
- `late_fee_flag` agrees with the label on {metrics['audit']['late_fee_agreement']:.3f} of rows and has univariate ROC-AUC {univariate_auc:.3f}. It is written when an account closes, so it is unavailable at scoring time.
- A random row split puts {random_overlap} customers on both sides.

## Results
Leaky baseline (random split, preprocessing on all rows, leak included): accuracy {leaky_metrics['accuracy']:.4f}, ROC-AUC {leaky_metrics['roc_auc']:.4f}, recall {leaky_metrics['recall']:.4f} at 0.5.

Repaired model (deduplicated, customer-grouped 60/20/20, leak removed, pipeline fitted on train): test accuracy {test_metrics['accuracy']:.4f}, precision {test_metrics['precision']:.4f}, recall {test_metrics['recall']:.4f}, F1 {test_metrics['f1']:.4f}, ROC-AUC {test_metrics['roc_auc']:.4f}, PR-AUC {test_metrics['pr_auc']:.4f} at threshold {threshold:.4f} (about 20% of customers flagged).

Bootstrap 95% intervals: recall [{recall_ci['low']:.3f}, {recall_ci['high']:.3f}], precision [{precision_ci['low']:.3f}, {precision_ci['high']:.3f}]. Grouped 5-fold PR-AUC: {group_cv.mean():.3f} ± {group_cv.std():.3f}.

## Limitations
The data is synthetic and the effects are controlled. The repaired model is a baseline, not a deployment candidate. A single group holdout cannot capture temporal drift, and the threshold reflects an assumed 20% review capacity. The dataset contains no dates, so temporal leakage is discussed but cannot be measured here.

## Reproduction
Run `python solution.py --out artifacts`, then `python check_lab01b.py --artifacts artifacts`. The manifest records the dataset, model, splits, metrics, and run configuration hashes.
"""
    (out / "report.md").write_text(report, encoding="utf-8", newline="\n")

    print(
        f"leaky auc={leaky_metrics['roc_auc']:.4f} -> repaired auc={test_metrics['roc_auc']:.4f}, "
        f"pr_auc={test_metrics['pr_auc']:.4f}"
    )
    print(f"threshold={threshold:.4f} artifacts written to {out}")


if __name__ == "__main__":
    main()
