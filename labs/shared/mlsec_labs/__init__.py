"""Shared utilities for ML-Sec Level 1 labs.

The package is intentionally small: only code used by more than one lab lives here.
"""

from .artifacts import build_manifest, environment, sha256_file, write_json
from .data import make_churn_dataset
from .metrics import binary_metrics, bootstrap_ci

__all__ = [
    "binary_metrics",
    "bootstrap_ci",
    "build_manifest",
    "environment",
    "make_churn_dataset",
    "sha256_file",
    "write_json",
]

__version__ = "1.0.0"
