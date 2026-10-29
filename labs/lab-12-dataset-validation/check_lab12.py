"""Independent checker for LAB-12.

Usage:
    python solution.py --out artifacts
    python check_lab12.py --artifacts artifacts

Exit code 0 means every check passed.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupShuffleSplit, train_test_split

from dataset import ALLOWED, FEATURES, LEAKY_COLUMNS, build_raw, feature_frame

TOL = 0.02


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    if not path.exists():
        fail(f"missing {path}")
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def close(actual: float, expected: float, tol: float, label: str) -> None:
    if abs(float(actual) - expected) > tol:
        fail(f"{label}: {actual:.4f} is not within {tol:.2f} of {expected:.4f}")


def schema_violation_mask(df: pd.DataFrame) -> pd.Series:
    return (
        (df["age"] < 18)
        | (df["age"] > 100)
        | (df["account_age_days"] < 0)
        | (df["monthly_spend"] > 500)
        | (df["plan"].notna() & ~df["plan"].isin(ALLOWED["plan"]))
        | (df["region"].notna() & ~df["region"].isin(ALLOWED["region"]))
    )


def conflict_mask(df: pd.DataFrame) -> pd.Series:
    return df.groupby(FEATURES, dropna=False)["churn"].transform("nunique") > 1


def implausible_mask(df: pd.DataFrame) -> pd.Series:
    return (
        (df["churn"] == 1)
        & (df["support_tickets"] == 0)
        & (df["account_age_days"] <= 120)
    )


def fit_auc(X_train, y_train, X_test, y_test) -> float:
    model = LogisticRegression(max_iter=2000).fit(X_train, y_train)
    return float(roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]))


def main() -> None:
    parser = argparse.ArgumentParser(description="Check LAB-12 artifacts.")
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    root = args.artifacts

    metrics = load_json(root / "metrics.json")
    validation = load_json(root / "validation.json")
    run = load_json(root / "run.json")
    manifest = load_json(root / "manifest.json")
    report = root / "report.md"
    repaired_path = root / "repaired.csv"
    if not report.exists():
        fail("missing report.md")
    if not repaired_path.exists():
        fail("missing repaired.csv")

    required = {"metrics.json", "run.json", "report.md", "validation.json", "repaired.csv"}
    paths = {entry["path"] for entry in manifest.get("files", [])}
    if not required <= paths:
        fail(f"manifest does not cover {sorted(required - paths)}")
    if run.get("lab") != "LAB-12":
        fail("run.json lab is not LAB-12")

    # Rebuild the raw data and recompute the defect counts independently.
    raw = build_raw()
    legacy = {
        "missing_cells": int(raw.isna().sum().sum()),
        "schema_violations": int(schema_violation_mask(raw).sum()),
        "exact_duplicate_rows": int(raw.duplicated().sum()),
        "label_conflict_groups": int(
            (raw.groupby(FEATURES, dropna=False)["churn"].nunique() > 1).sum()
        ),
        "implausible_labels": int(implausible_mask(raw).sum()),
        "duplicate_customer_ids": int(raw["customer_id"].duplicated().sum()),
    }
    train_idx, test_idx = train_test_split(
        np.arange(len(raw)), test_size=0.3, random_state=13
    )
    leaked = set(raw.iloc[train_idx]["customer_id"]) & set(raw.iloc[test_idx]["customer_id"])
    legacy["leaked_customers"] = len(leaked)
    legacy["leaky_columns"] = sum(1 for column in LEAKY_COLUMNS if column in raw.columns)

    expected = {
        "missing_cells": 18,
        "schema_violations": 10,
        "exact_duplicate_rows": 8,
        "label_conflict_groups": 4,
        "implausible_labels": 6,
        "duplicate_customer_ids": 28,
        "leaked_customers": 12,
        "leaky_columns": 1,
    }
    for key, value in expected.items():
        if legacy[key] != value:
            fail(f"generator drift: recomputed {key}={legacy[key]}, expected {value}")
        if int(validation["issue_counts"][key]) != value:
            fail(f"validation.json reports {key}={validation['issue_counts'][key]}, expected {value}")

    if int(validation["missing_total"]) != 18:
        fail("missing_total must be 18")
    if int(validation["schema_violations_total"]) != 10:
        fail("schema_violations_total must be 10")
    if int(validation["label_conflict_rows"]) != 8:
        fail("label_conflict_rows must be 8")
    if validation.get("leaky_columns") != ["exit_survey"]:
        fail("validation.json must name exit_survey as the leaky column")

    repaired = pd.read_csv(repaired_path)
    if len(repaired) != 581:
        fail(f"repaired.csv has {len(repaired)} rows, expected 581")
    expected_columns = ["customer_id", *FEATURES, "churn"]
    if list(repaired.columns) != expected_columns:
        fail(f"repaired.csv columns are {list(repaired.columns)}, expected {expected_columns}")
    if "exit_survey" in repaired.columns:
        fail("repaired.csv still contains exit_survey")
    if int(repaired.isna().sum().sum()) != 0:
        fail("repaired.csv still contains missing values")
    if int(repaired.duplicated().sum()) != 0:
        fail("repaired.csv still contains exact duplicates")
    if int(repaired["customer_id"].duplicated().sum()) != 0:
        fail("repaired.csv still contains duplicate customer ids")
    if bool(schema_violation_mask(repaired).any()):
        fail("repaired.csv still contains schema violations")
    if bool(conflict_mask(repaired).any()):
        fail("repaired.csv still contains label conflicts")
    if bool(implausible_mask(repaired).any()):
        fail("repaired.csv still contains implausible labels")
    if not set(repaired["churn"].unique()) <= {0, 1}:
        fail("repaired.csv churn must be binary")

    evaluation = metrics["evaluation"]
    close(evaluation["leaky_auc"], 0.9584, TOL, "leaky AUC")
    close(evaluation["same_rows_without_survey_auc"], 0.7507, TOL, "same-rows survey-free AUC")
    close(evaluation["clean_auc"], 0.8485, 0.03, "clean AUC")
    close(evaluation["leak_gap"], float(evaluation["leaky_auc"]) - float(evaluation["clean_auc"]), 0.005, "leak gap arithmetic")
    if float(evaluation["leak_gap"]) < 0.08:
        fail("leak gap must be at least 0.08")
    if float(evaluation["leaky_auc"]) < 0.93:
        fail("the leaky pipeline must reach AUC >= 0.93")
    if float(evaluation["clean_auc"]) > 0.90:
        fail("the repaired pipeline must stay at AUC <= 0.90")

    # Recompute the clean AUC from repaired.csv.
    X_clean = feature_frame(repaired)
    y_clean = repaired["churn"].to_numpy()
    splitter = GroupShuffleSplit(n_splits=1, test_size=0.3, random_state=13)
    train_rows, test_rows = next(splitter.split(X_clean, y_clean, groups=repaired["customer_id"]))
    recomputed_clean = fit_auc(
        X_clean.iloc[train_rows], y_clean[train_rows],
        X_clean.iloc[test_rows], y_clean[test_rows],
    )
    close(evaluation["clean_auc"], recomputed_clean, 0.01, "clean AUC recomputation")

    text = report.read_text(encoding="utf-8").lower()
    for phrase in ("schema", "missing", "duplicate", "label", "leak", "auc", "limitations"):
        if phrase not in text:
            fail(f"report is missing '{phrase}'")

    print(f"PASS raw rows={len(raw)} with {sum(expected.values())} planted issue signals")
    print("PASS validation counts match an independent recomputation")
    print(f"PASS repaired data: {len(repaired)} rows, schema-valid, unique customers, no leakage column")
    print(f"PASS leaky AUC={evaluation['leaky_auc']:.4f}, clean AUC={evaluation['clean_auc']:.4f}")
    print(f"PASS clean AUC recomputes from repaired.csv: {recomputed_clean:.4f}")
    print("PASS report contains schema, missing, duplicate, label, leak, AUC, limitations")
    print("LAB-12 CHECK PASSED")


if __name__ == "__main__":
    main()
