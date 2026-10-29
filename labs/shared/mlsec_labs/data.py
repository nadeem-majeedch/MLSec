"""Deterministic synthetic data for Level 1 labs.

No personal data is used. The churn dataset is generated from a fixed seed and
contains deliberate defects (duplicate rows, repeated customers, missing values,
and a post-outcome field) for the evaluation-audit lab.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

FEATURES = [
    "tenure_months",
    "monthly_spend",
    "logins_30d",
    "support_tickets_90d",
    "plan_tier",
    "payment_failures_90d",
    "avg_session_minutes",
    "days_since_last_login",
    "autopay",
    "region",
    "contract_months",
    "late_fee_flag",
]


def _sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-z))


def make_churn_dataset(
    n_customers: int = 1700,
    extra_snapshots: int = 300,
    exact_duplicates: int = 40,
    missing_spend: int = 80,
    seed: int = 42,
) -> pd.DataFrame:
    """Return a churn table with 2,000+ rows at customer and snapshot grain.

    Columns
    -------
    customer_id : repeated for customers with a second snapshot
    tenure_months, monthly_spend, logins_30d, support_tickets_90d, plan_tier,
    payment_failures_90d, avg_session_minutes, days_since_last_login, autopay,
    region, contract_months, late_fee_flag : features
    churned : label, constant within a customer

    ``late_fee_flag`` is written when an account closes and is therefore leakage
    for a model scored before renewal.
    """
    rng = np.random.default_rng(seed)

    tenure = rng.integers(1, 73, n_customers)
    spend = np.round(rng.gamma(4.0, 18.0, n_customers), 2)
    logins = rng.poisson(14, n_customers)
    tickets = rng.poisson(0.9, n_customers)
    tier = rng.choice(["A", "B", "C"], size=n_customers, p=[0.50, 0.30, 0.20])
    failures = rng.poisson(0.35, n_customers)
    session = np.round(rng.gamma(2.0, 4.0, n_customers), 1)
    days = rng.integers(0, 60, n_customers)
    autopay = rng.integers(0, 2, n_customers)
    region = rng.choice(["N", "S", "E", "W"], size=n_customers)
    contract = rng.choice([12, 24, 36], size=n_customers, p=[0.50, 0.30, 0.20])

    z = (
        0.15
        - 0.035 * tenure
        + 0.42 * tickets
        + 0.85 * failures
        - 0.055 * logins
        + 0.45 * (tier == "C")
        - 0.25 * autopay
        - 0.015 * days
        + rng.normal(0, 0.9, n_customers)
    )
    churned = (rng.random(n_customers) < _sigmoid(z)).astype(int)

    late_fee = np.where(rng.random(n_customers) < 0.10, 1 - churned, churned)

    customers = pd.DataFrame(
        {
            "customer_id": [f"C{i:04d}" for i in range(n_customers)],
            "tenure_months": tenure,
            "monthly_spend": spend,
            "logins_30d": logins,
            "support_tickets_90d": tickets,
            "plan_tier": tier,
            "payment_failures_90d": failures,
            "avg_session_minutes": session,
            "days_since_last_login": days,
            "autopay": autopay,
            "region": region,
            "contract_months": contract,
            "late_fee_flag": late_fee,
            "churned": churned,
        }
    )

    idx = np.arange(n_customers)
    extra_idx = rng.choice(n_customers, size=extra_snapshots, replace=False)
    rows = customers.iloc[np.concatenate([idx, extra_idx])].reset_index(drop=True)

    second = np.arange(n_customers, len(rows))
    rows.loc[second, "monthly_spend"] = np.clip(
        rows.loc[second, "monthly_spend"] + rng.normal(0, 3.0, len(second)), 5, None
    ).round(2)
    rows.loc[second, "logins_30d"] = np.clip(
        rows.loc[second, "logins_30d"] + rng.integers(-2, 3, len(second)), 0, None
    )
    rows.loc[second, "days_since_last_login"] = np.clip(
        rows.loc[second, "days_since_last_login"] + rng.integers(0, 15, len(second)), 0, None
    )
    rows.loc[second, "avg_session_minutes"] = np.clip(
        rows.loc[second, "avg_session_minutes"] + rng.normal(0, 1.5, len(second)), 0.2, None
    ).round(1)

    dup_idx = rng.choice(len(rows), size=exact_duplicates, replace=False)
    rows = pd.concat([rows, rows.iloc[dup_idx]], ignore_index=True)

    miss_idx = rng.choice(len(rows), size=missing_spend, replace=False)
    rows.loc[miss_idx, "monthly_spend"] = np.nan

    rows = rows.sample(frac=1.0, random_state=seed).reset_index(drop=True)
    return rows[["customer_id", *FEATURES, "churned"]]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the synthetic churn dataset.")
    parser.add_argument("--out", type=Path, default=Path("data/churn.csv"))
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    frame = make_churn_dataset(seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(args.out, index=False)
    print(f"wrote {args.out} rows={len(frame)} customers={frame['customer_id'].nunique()}")
    print(f"churn rate={frame['churned'].mean():.4f} duplicate rows={frame.duplicated().sum()}")


if __name__ == "__main__":
    main()
