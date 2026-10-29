"""Generate the synthetic churn dataset for LAB-01B.

Run:
    python make_dataset.py --out data

Writes churn.csv inside the output directory. Defaults to ./data.

The data is synthetic. It contains deliberate defects for the audit: duplicate
rows, customers with multiple snapshots, missing values, and a post-outcome field.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SHARED = Path(__file__).resolve().parents[1] / "shared"
if str(SHARED) not in sys.path:
    sys.path.insert(0, str(SHARED))

from mlsec_labs.artifacts import sha256_file  # noqa: E402
from mlsec_labs.data import make_churn_dataset  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the LAB-01B churn dataset.")
    parser.add_argument("--out", type=Path, default=Path("data"), help="directory for churn.csv")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    frame = make_churn_dataset(seed=args.seed)
    args.out.mkdir(parents=True, exist_ok=True)
    out_path = args.out / "churn.csv"
    frame.to_csv(out_path, index=False)
    print(f"rows={len(frame)} customers={frame['customer_id'].nunique()}")
    print(f"churn_rate={frame['churned'].mean():.4f} duplicate_rows={frame.duplicated().sum()}")
    print(f"wrote {out_path}")
    print(f"sha256={sha256_file(out_path)}")


if __name__ == "__main__":
    main()
