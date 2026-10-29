# Lesson 01.1 — Python for Security Work

**Module 01 · 1.5 hours · Python basics recommended**

## Scenario

A model-serving script accepts a batch of predictions from an upstream service. The service occasionally sends a score of `1.4` or a missing field. The script does not validate; it clips the score and continues. Six weeks later, a downstream fraud rule has been silently treating malformed inputs as high risk. No exception was raised, no log line was written, and the model's "accuracy" never changed because the malformed rows were never labelled.

Python will happily do something plausible with almost any input. In security work, "plausible" is the enemy. This lesson rebuilds the Python habits that make failure explicit.

## Learning objectives

By the end of this lesson you will be able to:

1. Write functions with explicit inputs, outputs, and validation.
2. Explain mutable default arguments and avoid the bug they cause.
3. Raise and catch specific exceptions instead of swallowing errors.
4. Structure a small script so its logic can be imported and tested.

## Values, types, and the first silent bug

Python is dynamically typed. A variable's type is a property of the value, not the name, and operations coerce types in ways that are sometimes convenient and sometimes dangerous.

```python
print(7 / 2)
print(7 // 2)
print("3" + "4")
print(3 + 4.0)
print(bool("False"))
```

Expected output:

```text
3.5
3
34
7.0
True
```

The last line is the classic trap: a non-empty string is truthy, including the string `"False"`. If a configuration file supplies `"False"` and your code does `if config["enabled"]:`, the branch runs. Parse booleans explicitly.

### Mutable defaults

```python
def add_label(label, labels=[]):
    labels.append(label)
    return labels

print(add_label("spam"))
print(add_label("ham"))
```

Expected output:

```text
['spam']
['spam', 'ham']
```

The default list is created **once**, when the function is defined, and reused on every call. This is a real source of cross-request state leakage in services. The fix is a sentinel:

```python
def add_label(label, labels=None):
    if labels is None:
        labels = []
    labels.append(label)
    return labels

print(add_label("spam"))
print(add_label("ham"))
```

Expected output:

```text
['spam']
['ham']
```

## Validation as a security control

A validation function should answer three questions:

1. **What is required?** Fields, types, ranges, lengths.
2. **What happens on failure?** A specific exception with enough context to debug, but no sensitive values.
3. **What is the boundary?** Validate once, at the edge, and pass a typed object inward.

### Worked example: validate a prediction batch

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Prediction:
    row_id: int
    score: float


def validate_batch(rows):
    if not rows:
        raise ValueError("empty batch")
    cleaned = []
    for position, row in enumerate(rows):
        missing = {"id", "score"} - set(row)
        if missing:
            raise ValueError(f"row {position}: missing fields {sorted(missing)}")
        row_id, score = row["id"], row["score"]
        if not isinstance(row_id, int) or isinstance(row_id, bool):
            raise TypeError(f"row {position}: id must be int, got {type(row_id).__name__}")
        if not isinstance(score, (int, float)) or isinstance(score, bool):
            raise TypeError(f"row {position}: score must be numeric")
        if not 0.0 <= float(score) <= 1.0:
            raise ValueError(f"row {position}: score {score} outside [0, 1]")
        cleaned.append(Prediction(row_id=row_id, score=float(score)))
    return cleaned


cases = [
    [{"id": 1, "score": 0.2}, {"id": 2, "score": 0.9}],
    [],
    [{"id": 1, "score": 0.2}, {"id": 2, "score": 1.4}],
]
for case in cases:
    try:
        result = validate_batch(case)
        print(f"valid: {len(result)} rows")
    except (TypeError, ValueError) as error:
        print(f"rejected: {error}")
```

Expected output:

```text
valid: 2 rows
rejected: empty batch
rejected: row 1: score 1.4 outside [0, 1]
```

Three details matter:

- The `bool` exclusion is deliberate. In Python, `True == 1`, so `isinstance(True, int)` is true. A boolean identifier would otherwise pass an integer check.
- The error message includes the position and the offending value, but not the whole batch. Logs should be useful without leaking data.
- The function returns immutable `Prediction` objects. Downstream code cannot accidentally mutate the validated result.

### Catching exceptions

Catch only what you can handle. This is wrong:

```python
try:
    score = float(raw)
except Exception:
    pass
```

It converts a parsing bug, a missing field, and a keyboard interrupt into the same silent outcome. Prefer:

```python
try:
    score = float(raw)
except (TypeError, ValueError) as error:
    raise ValueError(f"score is not numeric: {raw!r}") from error
```

The `from error` preserves the cause in the traceback. Do not catch `BaseException`, and do not use a bare `except:`.

## Structuring a script

A small script should expose its logic and guard its entry point:

```python
def summarize(scores):
    if not scores:
        raise ValueError("scores must not be empty")
    return {"n": len(scores), "mean": sum(scores) / len(scores)}


if __name__ == "__main__":
    print(summarize([0.2, 0.8, 0.5]))
```

Expected output:

```text
{'n': 3, 'mean': 0.5}
```

With the guard, a test can `import` the function without running the demo. This is the minimum structure for the labs: pure functions, a `main()` that handles files and paths, and `if __name__ == "__main__": main()`.

## Common mistakes

| Mistake | Example | Consequence | Fix |
|---|---|---|---|
| Mutable default | `def f(x, acc=[])` | State leaks across calls | Use `None` and create inside |
| Truthiness of strings | `if "False":` | Disabled feature runs | Parse with an explicit function |
| `is` for values | `if x is 5:` | Works by accident for small ints, fails later | Use `==` |
| Bare `except` | `except: pass` | Hides bugs and interrupts | Catch specific exceptions |
| Shadowing built-ins | `list = [...]` | Breaks later code and debugging | Rename the variable |
| Float equality | `0.1 + 0.2 == 0.3` | False | Use `math.isclose` |
| Integer division | `7 / 2` vs `7 // 2` | Wrong denominator in a metric | Choose deliberately |

## Troubleshooting

| Error | Likely cause | Fix |
|---|---|---|
| `TypeError: unsupported operand type(s)` | Mixed string and number | Convert at the boundary; validate types |
| `KeyError` | Missing dictionary field | Use `.get` with a default or validate required keys |
| `IndentationError` | Mixed tabs and spaces | Configure the editor to insert spaces |
| `ModuleNotFoundError` | Wrong environment or path | Activate `.venv`; run from the repository root |
| `UnicodeDecodeError` | Wrong file encoding | Specify `encoding="utf-8"` |
| Test passes alone, fails in suite | Shared mutable state | Remove module-level mutable globals |

## Key terms

**Dynamic typing**, **mutable default**, **truthiness**, **exception**, **validation**, **boundary**, **dataclass**, **immutability**, **entry-point guard**.

## Summary

- Python coerces types silently; validate at the boundary and fail loudly.
- Mutable defaults persist across calls; use `None` and create a fresh object.
- Catch specific exceptions and preserve the cause.
- Return immutable, validated objects so downstream code cannot corrupt them.
- Structure code as importable functions plus a guarded `main()`.

## References

| Reference | Use |
|---|---|
| [Python tutorial](https://docs.python.org/3/tutorial/) | Language fundamentals |
| [Python exceptions](https://docs.python.org/3/tutorial/errors.html) | Raising and handling errors |
| [Python `dataclasses`](https://docs.python.org/3/library/dataclasses.html) | Structured records |
| [PEP 8](https://peps.python.org/pep-0008/) | Readable code conventions |

Next: [Lesson 01.2 — NumPy](lesson-2-numpy.md).
