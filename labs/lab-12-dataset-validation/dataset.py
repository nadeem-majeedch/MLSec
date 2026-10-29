"""Synthetic dataset with planted integrity defects for LAB-12.

`build_raw()` is deterministic. It returns a customer-churn table with:

- 18 missing cells (12 monthly_spend, 6 plan)
- 10 schema violations (3 age, 2 account_age_days, 2 monthly_spend, 3 plan)
- 8 exact duplicate rows
- 4 contradictory label pairs (identical features, opposite labels)
- 5 implausible churn labels (no tickets, very new account)
- 20 duplicate-customer records with jittered values
- one post-outcome leaky column, `exit_survey`

Nothing here is real data. Customer ids are sequential placeholders.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

SEED = 7
N_BASE = 600
N_ROWS = 632
N_REPAIRED = 581

FEATURES = ["age", "account_age_days", "monthly_spend", "support_tickets", "plan", "region"]
ALLOWED = {"plan": ["basic", "plus", "pro"], "region": ["north", "south", "east", "west"]}
LEAKY_COLUMNS = ["exit_survey"]

MISSING_SPEND = [17, 44, 91, 133, 210, 287, 355, 401, 470, 512, 560, 591]
MISSING_PLAN = [23, 76, 158, 244, 333, 488]
BAD_AGE = [31, 205, 377]
BAD_ACCOUNT = [58, 412]
BAD_SPEND = [99, 266]
BAD_PLAN = [140, 301, 455]
CONFLICT_ROWS = [5, 120, 260, 410]
DUPLICATE_ROWS = [40, 150, 230, 340, 420, 480, 540, 580]
JITTER_ROWS = [25, 60, 85, 110, 165, 190, 250, 285, 320, 370,
               395, 430, 445, 490, 505, 520, 550, 565, 575, 595]


def build_raw() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    n = N_BASE
    age = rng.integers(18, 75, n)
    account_age_days = rng.integers(10, 2200, n)
    monthly_spend = np.round(rng.gamma(2.0, 25.0, n) + 15.0, 2)
    support_tickets = rng.poisson(1.1, n)
    plan = rng.choice(["basic", "plus", "pro"], size=n, p=[0.5, 0.3, 0.2])
    region = rng.choice(["north", "south", "east", "west"], size=n)
    region = np.array([str(value) for value in region], dtype=object)

    logit = (
        -0.95
        + 0.9 * (support_tickets >= 3)
        + 1.1 * (plan == "basic")
        - 0.8 * (account_age_days > 900)
        + 0.6 * (monthly_spend > 80)
        + rng.normal(0.0, 0.9, n)
    )
    churn = (logit > 0).astype(int)
    exit_survey = np.where(
        churn == 1, rng.random(n) < 0.95, rng.random(n) < 0.05
    ).astype(int)

    df = pd.DataFrame(
        {
            "customer_id": [f"C{i:04d}" for i in range(n)],
            "age": age,
            "account_age_days": account_age_days,
            "monthly_spend": monthly_spend,
            "support_tickets": support_tickets,
            "plan": plan,
            "region": region,
            "exit_survey": exit_survey,
            "churn": churn,
        }
    )

    df.loc[MISSING_SPEND, "monthly_spend"] = np.nan
    df.loc[MISSING_PLAN, "plan"] = np.nan

    df.loc[BAD_AGE, "age"] = 150
    df.loc[BAD_ACCOUNT, "account_age_days"] = -5
    df.loc[BAD_SPEND, "monthly_spend"] = 99999.0
    df.loc[BAD_PLAN, "plan"] = "premium"

    for row in CONFLICT_ROWS:
        df.loc[row, "support_tickets"] = max(int(df.loc[row, "support_tickets"]), 2)
        df.loc[row, "account_age_days"] = max(int(df.loc[row, "account_age_days"]), 300)

    twins = []
    for offset, row in enumerate(CONFLICT_ROWS):
        twin = df.iloc[row].copy()
        twin["customer_id"] = f"D{offset:04d}"
        twin["churn"] = 1 - int(df.iloc[row]["churn"])
        twins.append(twin)

    planted = (
        MISSING_SPEND
        + MISSING_PLAN
        + BAD_AGE
        + BAD_ACCOUNT
        + BAD_SPEND
        + BAD_PLAN
        + CONFLICT_ROWS
        + DUPLICATE_ROWS
        + JITTER_ROWS
    )
    implausible = df.index[
        (df["churn"] == 0)
        & (df["support_tickets"] == 0)
        & (df["account_age_days"] <= 120)
        & (~df.index.isin(planted))
    ][:5]
    df.loc[implausible, "churn"] = 1

    duplicates = df.iloc[DUPLICATE_ROWS].copy()
    df = pd.concat([df, pd.DataFrame(twins), duplicates], ignore_index=True)

    extra_rows = []
    for row in JITTER_ROWS:
        twin = df.iloc[row].copy()
        twin["monthly_spend"] = round(float(twin["monthly_spend"]) + 5.0, 2)
        twin["support_tickets"] = int(twin["support_tickets"]) + 1
        twin["account_age_days"] = int(twin["account_age_days"]) + 30
        extra_rows.append(twin)
    df = pd.concat([df, pd.DataFrame(extra_rows)], ignore_index=True)

    return df.sample(frac=1.0, random_state=SEED).reset_index(drop=True)


def feature_frame(df: pd.DataFrame) -> pd.DataFrame:
    """One-hot encode categorical features at a fixed category set."""
    encoded = df[FEATURES].copy()
    for column, allowed in ALLOWED.items():
        encoded[column] = pd.Categorical(encoded[column], categories=allowed)
    return pd.get_dummies(encoded, columns=list(ALLOWED), dtype=float)
