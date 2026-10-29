"""Builds the toy project audited in LAB-13.

The project is deliberately weak, not malicious:

- unpinned requirements
- a loader that calls joblib.load on an artifact
- a stale manifest hash
- no signature and no SBOM
- a benign canary pickle whose only action, if ever loaded, is to print a
  marker string. Nothing in the lab loads it; the audit reads its bytes with
  `pickletools.genops` and never calls `pickle.load`.

Everything is written under the caller-supplied directory.
"""

from __future__ import annotations

import hashlib
import json
import pickle
from pathlib import Path

import numpy as np

PINNED = {
    "numpy": "2.5.2",
    "pandas": "3.0.5",
    "scikit-learn": "1.9.0",
    "joblib": "1.5.3",
    "PyYAML": "6.0.3",
}

UNPINNED_REQUIREMENTS = ["numpy", "pandas", "scikit-learn", "joblib", "PyYAML"]

TRAIN_SOURCE = '''"""Toy training script: fit a tiny linear model and save weights."""

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_digits

X, y = load_digits(return_X_y=True)
X = X.astype(np.float64) / 16.0
model = LogisticRegression(max_iter=200).fit(X, y)
np.savez("model.npz", coef=model.coef_, intercept=model.intercept_,
         classes=model.classes_)
'''

UNSAFE_LOADER_SOURCE = '''"""Toy inference loader (deliberately unsafe)."""

import joblib


def load_model(path="model.pkl"):
    return joblib.load(path)
'''

SAFE_LOADER_SOURCE = '''"""Hardened inference loader: no pickle, explicit shape checks."""

import numpy as np


def load_model(path="model.npz"):
    with np.load(path, allow_pickle=False) as data:
        coef = data["coef"]
        intercept = data["intercept"]
        classes = data["classes"]
    if coef.ndim != 2 or intercept.ndim != 1 or classes.ndim != 1:
        raise ValueError("unexpected model array shapes")
    return coef, intercept, classes
'''


class Canary:
    """Benign marker. Loading this pickle would only print a fixed string."""

    def __reduce__(self):
        return (print, ("LAB-13 CANARY: pickle executed; never load untrusted artifacts.",))


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def build_project(project_dir: str | Path) -> Path:
    root = Path(project_dir)
    root.mkdir(parents=True, exist_ok=True)

    (root / "requirements.txt").write_text(
        "".join(f"{name}\n" for name in UNPINNED_REQUIREMENTS), encoding="utf-8", newline="\n"
    )
    (root / "train.py").write_text(TRAIN_SOURCE, encoding="utf-8", newline="\n")
    (root / "load_model.py").write_text(UNSAFE_LOADER_SOURCE, encoding="utf-8", newline="\n")

    coef = np.array([[0.5, -0.25], [0.1, 0.3]], dtype=np.float64)
    intercept = np.array([0.05, -0.1], dtype=np.float64)
    classes = np.array([0, 1], dtype=np.int64)
    np.savez(root / "model.npz", coef=coef, intercept=intercept, classes=classes)

    benign = {
        "coef": coef.tolist(),
        "intercept": intercept.tolist(),
        "classes": classes.tolist(),
    }
    (root / "model.pkl").write_bytes(pickle.dumps(benign, protocol=4))
    (root / "canary.pkl").write_bytes(pickle.dumps(Canary(), protocol=4))

    (root / "manifest.json").write_text(
        json.dumps(
            {
                "algorithm": "sha256",
                "files": [
                    {
                        "path": "model.npz",
                        "sha256": "0" * 64,
                        "bytes": int((root / "model.npz").stat().st_size),
                    }
                ],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return root
