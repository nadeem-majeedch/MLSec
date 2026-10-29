# Lesson 01.2 — NumPy: Arrays, Shapes, and Reproducibility

**Module 01 · 1.5 hours · Complete Lesson 01.1 first**

## Scenario

A student computes attack success rate with this line:

```python
success = np.mean(predicted != true_labels, axis=0)
```

The test set has 1,000 examples and 10 classes. `predicted` and `true_labels` are both shape `(1000,)`. The code runs. The result is a single number, so the student reports "attack success rate: 0.42." Later, a reviewer notices that the model's predictions were shape `(1000, 10)` one-hot vectors. The comparison broadcast a `(1000, 10)` array against `(1000,)`, and the "success rate" was computed over the wrong axis. The attack may have worked; the report is still wrong.

NumPy is fast because it reasons about shapes and types mechanically. That is also why it lets a shape bug produce a plausible number instead of an error. This lesson teaches you to check the four properties that matter: **shape, dtype, axis, and generator**.

## Learning objectives

By the end of this lesson you will be able to:

1. Inspect an array's shape, dtype, dimensionality, and size.
2. Apply broadcasting deliberately and predict the result shape.
3. Compute reductions along a stated axis and explain what the result means.
4. Generate reproducible random numbers with `default_rng` and a recorded seed.
5. Compute an L-infinity budget and clip a perturbation to a valid range.

## Arrays are not lists

```python
import numpy as np

x = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32)
print(x.shape, x.dtype, x.ndim, x.size)
print(x.sum(axis=0))
print(x.sum(axis=1, keepdims=True))
```

Expected output:

```text
(2, 3) float32 2 6
[5. 7. 9.]
[[ 6.]
 [15.]]
```

- `shape` is `(rows, columns)`.
- `dtype` is the element type. A float array and an integer array behave differently under division, overflow, and serialization.
- `axis=0` reduces over rows, producing one value per column. `axis=1` reduces over columns, producing one value per row.
- `keepdims=True` preserves the reduced dimension as length 1, which makes later broadcasting unambiguous.

A list of lists is not an array. `[[1,2],[3,4]] + [[5,6],[7,8]]` concatenates lists; `np.array(...) + np.array(...)` adds elementwise. Convert at the boundary and keep arrays homogeneous.

## dtypes: silent wrap-around

```python
a = np.array([200], dtype=np.uint8)
b = np.array([100], dtype=np.uint8)
print(a + b, (a + b).dtype)
```

Expected output:

```text
[44] uint8
```

`uint8` holds values from 0 to 255. The sum 300 wraps to 44. In a security context, this can corrupt counts, pixel values, or feature bins without raising an exception. Check the dtype before arithmetic that can exceed its range, and cast deliberately:

```python
print(a.astype(np.int64) + b.astype(np.int64))
```

Expected output:

```text
[300]
```

Integer overflow is not only a numerical curiosity. A metric computed in `uint8` can saturate; a perturbation stored in `uint8` can wrap and change sign. The rule is: use floating point for model inputs and metrics unless you have a specific reason not to.

## Broadcasting

Broadcasting lets NumPy combine arrays of different shapes when their dimensions are compatible. Two dimensions are compatible when they are equal or one of them is 1. The smaller array is conceptually stretched, without copying.

```python
X = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
mean = X.mean(axis=0)
std = X.std(axis=0)
Z = (X - mean) / std
print(mean)
print(std)
print(np.round(Z, 3))
```

Expected output:

```text
[3. 4.]
[1.63299316 1.63299316]
[[-1.225 -1.225]
 [ 0.     0.   ]
 [ 1.225  1.225]]
```

`X` has shape `(3, 2)`, `mean` has shape `(2,)`. Broadcasting aligns the trailing dimension, so each column is standardized by its own mean and standard deviation. This is the correct way to standardize features. It is also the mechanism behind the one-hot bug in the scenario: a `(1000, 10)` array and a `(1000,)` array broadcast to `(1000, 1000)` or fail, depending on the order, and the reduction then means something different.

Before any broadcast, write down the two shapes and the expected output shape. If you cannot, do not run the line.

## Reproducible randomness

Use `np.random.default_rng(seed)` rather than the legacy global `np.random.seed`. A generator object carries its own state, so two experiments cannot accidentally share it.

```python
rng = np.random.default_rng(42)
print(rng.integers(0, 10, size=5))

rng2 = np.random.default_rng(42)
print(rng2.integers(0, 10, size=5))
```

Expected output:

```text
[0 7 6 4 4]
[0 7 6 4 4]
```

The sequences match because both generators start from the same seed. This is reproducibility, not security: a pseudorandom sequence is predictable if the seed is known. Do not use `numpy` randomness for passwords, keys, or tokens; use `secrets` for those.

## Security-relevant arithmetic: budgets and clipping

An L-infinity perturbation budget is the maximum absolute change to any feature. It is one line in NumPy:

```python
delta = np.array([0.02, -0.5, 0.1])
print(np.max(np.abs(delta)))
```

Expected output:

```text
0.5
```

A valid image or feature vector often has a range, such as `[0, 1]`. After adding a perturbation, clip:

```python
x = np.array([0.0, 0.5, 1.0])
print(np.clip(x + delta, 0, 1))
```

Expected output:

```text
[0.02 0.   1.  ]
```

The second element was `-0.4` before clipping and became `0.0`; the third was `1.1` and became `1.0`. The resulting perturbation is no longer exactly `delta`, which matters when you report the achieved L-infinity norm. Always compute the norm of the **final** perturbed input, not the norm of the intended step.

## Vectorization and readability

Vectorized code is faster and usually clearer, but it hides loops. When a result is wrong, rewrite the operation with an explicit loop on a tiny example and compare. A three-element array is enough to expose an axis error.

```python
scores = np.array([0.2, 0.8, 0.5, 0.9])
threshold = 0.7
print((scores >= threshold).astype(int))
print((scores >= threshold).mean())
```

Expected output:

```text
[0 1 0 1]
0.5
```

The comparison produces booleans; `.mean()` treats `True` as 1. The denominator is the number of scores, which is the correct base set here. If some rows were excluded, the denominator would be wrong.

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Reducing on the wrong axis | Scalar where a per-class vector was expected | Print shapes; state the axis in a comment |
| Broadcasting `(n, k)` with `(n,)` | Unexpected `(n, n)` array or error | Reshape to `(n, 1)` or use `axis=1` |
| Comparing float arrays with `==` | Tiny differences produce false | Use `np.allclose` or a tolerance |
| Using `np.random.seed` globally | Experiments interfere | Use `default_rng` per experiment |
| Assuming integer arithmetic is safe | Overflow or wrap-around | Cast to float or a wider integer |
| Clipping before computing the norm | Reported perturbation is too small | Compute the norm after clipping |

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `operands could not be broadcast together` | Incompatible trailing dimensions | Align shapes; reshape explicitly |
| `IndexError: too many indices` | Array has fewer dimensions than assumed | Check `ndim` and `shape` |
| `TypeError: only size-1 arrays can be converted` | Passing an array where a scalar is required | Reduce explicitly |
| Results differ between runs | Unseeded randomness or unordered operations | Use a generator and fix the seed |
| NaN in a metric | Division by zero or invalid value | Check denominators and use `np.errstate` deliberately |

## Key terms

**ndarray**, **shape**, **dtype**, **axis**, **broadcasting**, **reduction**, **vectorization**, **generator**, **seed**, **L-infinity norm**, **clipping**, **overflow**.

## Summary

- Check **shape, dtype, axis, and generator** before trusting a NumPy result.
- Broadcasting is powerful and silent; predict the output shape first.
- Integer dtypes wrap; use floating point for model inputs and metrics.
- Use `default_rng` with a recorded seed; randomness is reproducible, not secret.
- Compute perturbation norms after clipping, on the final input.

## References

| Reference | Use |
|---|---|
| [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html) | Array basics |
| [NumPy broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html) | Shape compatibility rules |
| [NumPy random generator](https://numpy.org/doc/stable/reference/random/generator.html) | `default_rng` and distributions |
| [NumPy dtypes](https://numpy.org/doc/stable/reference/arrays.dtypes.html) | Type promotion and overflow |

Next: [Lesson 01.3 — pandas](lesson-3-pandas.md).
