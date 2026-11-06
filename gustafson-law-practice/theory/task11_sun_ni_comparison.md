# Task 11 — Gustafson vs Sun–Ni memory-bounded speedup

## 1. Unified formulation
Let s = serial fraction, p = 1 − s, and let G(P) be the factor by which the **parallel** workload grows when P processors (and P× the memory) are used.

  **S_SN(P) = (s + p·G(P)) / (s + p·G(P)/P)**

| Choice of G(P) | Model |
|---|---|
| G(P) = 1 | Amdahl: S = 1/(s + p/P) (fixed size) |
| G(P) = P | Gustafson: S = (s + pP)/(s + p) = s + pP (fixed time) |
| G(P) = memory-driven growth, e.g. P^{3/2} | Sun–Ni (memory-bounded) |

How G arises: memory M ∝ P ⇒ problem *size* N^{a} ∝ P (a = memory exponent, e.g. 2 for N×N matrices); work ∝ N^{b} ⇒ G(P) = P^{b/a}.
* Dense GEMM: memory N², work N³ ⇒ G = P^{3/2}.
* 3D stencil / explicit grid: memory N³, work N³ per sweep ⇒ G = P (Gustafson is exact).
* FFT / sort: memory N, work N log N ⇒ G = P·(1 + log P/log N₁) slightly above P.
* Sparse/graph kernels with fixed work per edge: G ≈ P (memory-bound but no superlinear work).

## 2. Worked example (s = 0.04, P = 1024)

| Model | G | S |
|---|---|---|
| Amdahl | 1 | 24.43 |
| Sun–Ni, work grows slower (G = P^0.8 = 256) | 256 | 878.0 |
| Gustafson | 1024 | 983.08 |
| Sun–Ni, GEMM-like (G = P^1.5 = 32768) | 32768 | 1022.7 |

(S_SN for G=32768: (0.04+0.96·32768)/(0.04+0.96·32) = 31457.32/30.76 = 1022.7. Check G=P=1024: (0.04+983.04)/(0.04+0.96) = 983.08 ✓.)

## 3. When does Gustafson mis-estimate?
**Overestimates** (reality below S_G):
1. **Memory-/capacity-limited scaling where work cannot grow ∝ P** (G < P): input data size is capped, or the algorithm's work per byte of memory is sublinear
   (e.g. work grows slower than memory when the extra memory goes to ghost/replicated data, indices, buffers). Example above: S = 878 < 983.
2. When the **parallel runtime is not constant**: communication, contention or algorithmic complexity make T_P grow (Tasks 12, 13, 18). Gustafson's premise
   (equal time) is violated, so its S is an upper bound.
3. When memory per node is **replicated** (e.g. a fully replicated lookup table), the usable problem grows slower than P.

**Underestimates** (reality above S_G, measured by work done per time):
1. **Superlinear-work algorithms bounded by memory, not time** (G > P): GEMM/LU/Cholesky/dense eigensolvers. Using all memory yields a larger
   problem and more useful flops per second, at the price of a longer run time T·G/P. Sun–Ni: 1022.7 vs 983.1.
2. **Cache effects**: bigger aggregate cache holds the working set ⇒ super-linear per-core speed-up (not in either law).
3. When the serial fraction **shrinks** with problem size (a fixed setup against an ever-bigger parallel part), α falls and S_G with constant α underestimates.

## 3b. Summary
Sun–Ni = Gustafson with the *right* workload growth law. Gustafson ⇔ memory-bounded and time-bounded coincide (G = P). They differ exactly where an
algorithm's computation/memory ratio is not constant. Note also: S_SN → P as G → ∞ (the serial part vanishes in relative terms).
