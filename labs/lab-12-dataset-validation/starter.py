"""LAB-12 starter: build a validation and repair pipeline for a dirty dataset.

Run from this directory:
    python starter.py --out artifacts

Three TODO blocks: validate, repair, evaluate. The data generator, schema rules,
split helpers, metric helper, and report template are given; they are part of the
task contract. Complete the TODOs, then run check_lab12.py on your artifacts.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupShuffleSplit, train_test_split

SHARED = Path(__file__).resolve().parents[1] / "shared"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from mlsec_labs.artifacts import build_manifest, environment, write_json  # noqa: E402

from dataset import ALLOWED, FEATURES, LEAKY_COLUMNS, build_raw, feature_frame  # noqa: E402

SEED = 7
TEST_SIZE = 0.3
SPLIT_SEED = 13
IMPLAUSIBLE_RULE = "churn=1 with support_tickets=0 and account_age_days<=120"


def invalid_rows(df: pd.DataFrame) -> pd.Series:
    return (
        (df["age"] < 18)
        | (df["age"] > 100)
        | (df["account_age_days"] < 0)
        | (df["monthly_spend"] > 500)
        | (df["plan"].notna() & ~df["plan"].isin(ALLOWED["plan"]))
        | (df["region"].notna() & ~df["region"].isin(ALLOWED["region"]))
    )


def implausible_mask(df: pd.DataFrame) -> pd.Series:
    return (
        (df["churn"] == 1)
        & (df["support_tickets"] == 0)
        & (df["account_age_days"] <= 120)
    )


def conflict_mask(df: pd.DataFrame) -> pd.Series:
    return df.groupby(FEATURES, dropna=False)["churn"].transform("nunique") > 1


def split_customer_overlap(df: pd.DataFrame) -> list[str]:
    train_idx, test_idx = train_test_split(
        np.arange(len(df)), test_size=TEST_SIZE, random_state=SPLIT_SEED
    )
    train_ids = set(df.iloc[train_idx]["customer_id"])
    test_ids = set(df.iloc[test_idx]["customer_id"])
    return sorted(train_ids & test_ids)


def validate(df: pd.DataFrame) -> dict:
    """TODO 1: build the validation report.

    Count, at minimum:
      - missing cells per column and in total
      - schema violations by rule (age, account age, spend, plan, region) and in total
      - exact duplicate rows (`df.duplicated()`)
      - label-conflict groups and rows (use conflict_mask)
      - implausible labels (use implausible_mask)
      - duplicate customer_id records
      - customers appearing in both sides of the naive split (split_customer_overlap)
      - leaky columns present in the frame
    Return a dict that includes `issue_counts` with the keys used in metrics.json:
    missing_cells, schema_violations, exact_duplicate_rows, label_conflict_groups,
    implausible_labels, duplicate_customer_ids, leaked_customers, leaky_columns.
    Keep the detail keys demonstrated in the reference report.
    """
    raise NotImplementedError("TODO 1: implement validate")


def repair(df: pd.DataFrame, validation: dict) -> pd.DataFrame:
    """TODO 2: return a cleaned dataframe.

    Required properties of the result:
      - no schema-invalid rows
      - no missing values (median for monthly_spend, mode for plan)
      - no exact duplicates
      - no label-conflict rows
      - no implausible-label rows
      - exactly one record per customer_id
      - no leaky columns
      - a fresh RangeIndex
    Order matters: dropping rows before deduplicating changes the row count.
    """
    raise NotImplementedError("TODO 2: implement repair")


def fit_auc(X_train, y_train, X_test, y_test) -> float:
    model = LogisticRegression(max_iter=2000).fit(X_train, y_train)
    return float(roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]))


def evaluate(raw: pd.DataFrame, repaired: pd.DataFrame) -> dict:
    """TODO 3: compare the leaky and repaired evaluations.

    Leaky pipeline: drop schema-invalid and missing rows from raw, remove exact
    duplicates, keep duplicate customers, keep the survey column, split rows at
    random (test_size=TEST_SIZE, random_state=SPLIT_SEED).
    Same-rows ablation: reuse the identical rows and split indices without the
    survey column.
    Clean pipeline: one-hot encode `repaired`, split by customer_id with
    GroupShuffleSplit(test_size=TEST_SIZE, random_state=SPLIT_SEED), fit and score.
    Return leaky_auc, same_rows_without_survey_auc, clean_auc, leak_gap
    (leaky_auc - clean_auc), and the row counts.
    """
    raise NotImplementedError("TODO 3: implement evaluate")


def main() -> None:
    parser = argparse.ArgumentParser(description="Dataset validation and leakage audit.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    raw = build_raw()
    validation = validate(raw)
    repaired = repair(raw, validation)
    evaluation = evaluate(raw, repaired)

    raw.to_csv(args.out / "raw.csv", index=False)
    repaired.to_csv(args.out / "repaired.csv", index=False)
    write_json(args.out / "validation.json", validation)

    metrics = {
        "dataset": "synthetic customer churn (local generator, seed 7)",
        "raw_rows": int(len(raw)),
        "repaired_rows": int(len(repaired)),
        "issue_counts": {
            "missing_cells": validation["missing_total"],
            "schema_violations": validation["schema_violations_total"],
            "exact_duplicate_rows": validation["exact_duplicate_rows"],
            "label_conflict_groups": validation["label_conflict_groups"],
            "implausible_labels": validation["implausible_labels"],
            "duplicate_customer_ids": validation["duplicate_customer_ids"],
            "leaked_customers": validation["leaked_customers"],
            "leaky_columns": len(validation["leaky_columns"]),
        },
        "evaluation": evaluation,
        "repair_actions": [
            f"drop {validation['schema_violations_total']} rows with schema violations",
            f"median-impute monthly_spend ({validation['missing_by_column'].get('monthly_spend', 0)} cells)",
            f"mode-impute plan ({validation['missing_by_column'].get('plan', 0)} cells)",
            f"drop {validation['exact_duplicate_rows']} exact duplicate rows",
            f"quarantine {validation['label_conflict_rows']} rows in {validation['label_conflict_groups']} conflicting label groups",
            "quarantine rows matching the implausible-label rule",
            "keep one record per customer_id",
            f"drop leaky columns: {', '.join(validation['leaky_columns'])}",
        ],
        "leaky_columns_removed": validation["leaky_columns"],
    }

    write_json(args.out / "metrics.json", metrics)
    write_json(
        args.out / "run.json",
        {
            "lab": "LAB-12",
            "seed": SEED,
            "split_seed": SPLIT_SEED,
            "raw_rows": int(len(raw)),
            "repaired_rows": int(len(repaired)),
            "environment": environment(),
        },
    )
    (args.out / "report.md").write_text(build_report(metrics), encoding="utf-8", newline="\n")
    write_json(
        args.out / "manifest.json",
        build_manifest(
            args.out,
            ["raw.csv", "validation.json", "repaired.csv", "metrics.json", "run.json", "report.md"],
        ),
    )

    print(f"raw rows={len(raw)} repaired rows={len(repaired)}")
    print(f"issues={metrics['issue_counts']}")
    print(
        f"leaky AUC={evaluation['leaky_auc']:.4f} "
        f"without survey={evaluation['same_rows_without_survey_auc']:.4f} "
        f"clean={evaluation['clean_auc']:.4f}"
    )
    print(f"artifacts written to {args.out}")


def build_report(metrics: dict) -> str:
    counts = metrics["issue_counts"]
    evaluation = metrics["evaluation"]
    lines = [
        "# LAB-12 report — dataset validation and leakage",
        "",
        f"Raw rows: {metrics['raw_rows']}. Repaired rows: {metrics['repaired_rows']}.",
        "",
        "## Detected issues",
        "",
        "| Issue | Count |",
        "|---|---:|",
        f"| Missing cells | {counts['missing_cells']} |",
        f"| Schema violations | {counts['schema_violations']} |",
        f"| Exact duplicate rows | {counts['exact_duplicate_rows']} |",
        f"| Label-conflict groups | {counts['label_conflict_groups']} |",
        f"| Implausible labels | {counts['implausible_labels']} |",
        f"| Duplicate customer records | {counts['duplicate_customer_ids']} |",
        f"| Customers leaked across the naive split | {counts['leaked_customers']} |",
        f"| Leaky columns | {counts['leaky_columns']} |",
        "",
        "## Repair",
        "",
        "The pipeline drops schema-invalid rows, imputes missing numeric and",
        "categorical values, removes exact duplicates, quarantines label conflicts",
        "and implausible labels, keeps one record per customer, and drops the",
        "post-outcome survey column.",
        "",
        "## Leakage experiment",
        "",
        "| Evaluation | ROC-AUC |",
        "|---|---:|",
        f"| Naive rows, survey included | {evaluation['leaky_auc']:.4f} |",
        f"| Same rows and split, survey removed | {evaluation['same_rows_without_survey_auc']:.4f} |",
        f"| Repaired rows, grouped split, survey removed | {evaluation['clean_auc']:.4f} |",
        "",
        f"The headline gap between the leaky and repaired pipelines is "
        f"{evaluation['leak_gap']:.4f}. The controlled comparison on identical rows "
        f"shows the survey column alone accounts for "
        f"{evaluation['leaky_auc'] - evaluation['same_rows_without_survey_auc']:.4f} "
        "of AUC.",
        "",
        "The repaired AUC is not directly comparable to the same-rows number: repair",
        "also removes contradictory labels and duplicate customers and changes the",
        "split. Only the same-rows ablation isolates the column.",
        "",
        "## Limitations",
        "",
        "- The data is synthetic and the defects were planted deliberately.",
        "- The label rules are heuristics; a real review needs domain owners.",
        "- AUC is one metric and the test split is small.",
        "- Dropping suspicious rows changes class balance and may bias the model.",
        "- Validation catches the defects it was written to catch, not unknown ones.",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    main()
