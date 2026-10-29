"""LAB-01B starter: audit and repair a leaky churn baseline.

Complete the TODO blocks, then run:
    python starter.py --out artifacts
    python check_lab01b.py --artifacts artifacts

The lab brief is docs/labs/lab-01b.md; the checking guide is CHECKING.md.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

SHARED = Path(__file__).resolve().parents[1] / "shared"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from mlsec_labs.data import FEATURES, make_churn_dataset  # noqa: E402
from mlsec_labs.metrics import binary_metrics  # noqa: E402

TIER = {"A": 0, "B": 1, "C": 2}
REGION = {"N": 0, "S": 1, "E": 2, "W": 3}


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


def audit(df: pd.DataFrame, seed: int = 42) -> dict:
    """TODO 1: return counts and leak diagnostics.

    Required keys: duplicate_rows, missing_monthly_spend, late_fee_agreement,
    late_fee_univariate_auc, random_split_customer_overlap.
    """
    raise NotImplementedError("TODO 1: audit duplicates, missing values, leak, and overlap")


def leaky_baseline(df: pd.DataFrame, seed: int = 42) -> dict:
    """TODO 2: reproduce the dashboard result.

    Use a random 75/25 row split, fit the imputer and scaler on all rows, keep
    late_fee_flag, and return the metrics at 0.5 under key "at_0_5".
    """
    raise NotImplementedError("TODO 2: reproduce the leaky baseline")


def repair(df: pd.DataFrame, seed: int = 42):
    """TODO 3: deduplicate, drop the leaky feature, split by customer, fit a pipeline.

    Return (model, frames, row_indices, threshold, test_metrics, ci, cv).
    Use a 60/20/20 customer-grouped stratified split, choose the threshold on
    validation at the 80th percentile, and evaluate on test.
    """
    raise NotImplementedError("TODO 3: repair the evaluation protocol")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit the LAB-01B churn baseline.")
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    df = make_churn_dataset(seed=args.seed)
    args.out.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out / "data.csv", index=False)

    audit_result = audit(df, args.seed)
    leaky = leaky_baseline(df, args.seed)
    model, frames, row_indices, threshold, test_metrics, ci, cv = repair(df, args.seed)

    print("audit:", audit_result)
    print("leaky AUC:", leaky["at_0_5"]["roc_auc"])
    print("repaired test:", test_metrics)
    print("threshold:", threshold)
    print("bootstrap:", ci)
    print("group CV PR-AUC:", cv)


if __name__ == "__main__":
    main()
