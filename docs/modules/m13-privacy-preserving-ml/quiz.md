---
title: Knowledge Check — QZ-13
---

# Knowledge Check — QZ-13

**Module 13 · 10 items · 15 points · about 20 minutes**

Answer without running LAB-17. For items 2, 3, and 5, show the numbers you use.

---

**1. (1 point)** In row-level differential privacy, two datasets are neighbors when they

A. have the same number of rows but different columns  
B. differ in exactly one row  
C. come from the same distribution  
D. are both synthetic

---

**2. (2 points)** A release computes the mean of 1,000 rows with 6 features. Each feature is clipped to \([-2.5, 2.5]\). Compute the L1 sensitivity of the mean vector, then the Laplace scale for \(\varepsilon = 0.6\).

---

**3. (2 points)** Four sequential count queries each spend \(\varepsilon = 0.2\). A fifth stage runs two independent queries, each \(\varepsilon = 0.3\), on two disjoint datasets. What is the total epsilon under basic sequential and parallel composition?

---

**4. (1 point)** Why is clipping applied before noise is added to a mean?

A. It makes the mean unbiased  
B. It bounds sensitivity, which sets the noise scale  
C. It removes outliers from the released value  
D. It encrypts the data

---

**5. (2 points)** LAB-17 reports accuracy 0.5233 at \(\varepsilon = 0.02\), 0.7833 at \(\varepsilon = 0.5\), and 0.8233 with no noise. The centroid L2 error is 4.3642 at \(\varepsilon = 0.02\) and 0.3257 at \(\varepsilon = 0.5\). Explain what these numbers show about the privacy–utility trade-off.

---

**6. (2 points)** LAB-17's membership AUC is 0.5308 at \(\varepsilon = 0.5\). State what this supports and two things it does not support.

---

**7. (1 point)** In local differential privacy, who adds the noise, and what trust assumption does that change?

---

**8. (1 point)** Does secure aggregation provide differential privacy? Explain in one or two sentences.

---

**9. (1 point)** A paper reports \(\varepsilon = 1.0\) for a mechanism with unbounded sensitivity and no clipping. A vendor reports \(\varepsilon = 1.0\) for a clipped mean. Why can these two numbers not be compared directly?

---

**10. (2 points)** Rewrite this claim as a scoped statement: "Our epsilon 0.5 release is private, so the dashboard is safe to share."

---

*When you have finished, compare your answers with the [answer key](quiz-answers.md).*
