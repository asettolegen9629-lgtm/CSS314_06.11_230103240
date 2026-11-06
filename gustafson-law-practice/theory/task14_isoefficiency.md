# Task 14 — Isoefficiency view of Gustafson scaling

## 1. Definitions (Grama–Gupta–Kumar)
W = problem size (serial work, T₁ = W·t_c); total overhead T_o(W,P) = P·T_P − W; efficiency E = W/(W + T_o) = 1/(1 + T_o/W).
Constant E requires **T_o/W = (1−E)/E**, i.e. **W = K·T_o(W,P)** with K = E/(1−E). The isoefficiency function f(P) is the slowest growth of W with P
that keeps E constant (the solution of this equation).

## 2. Gustafson-compliant program
Parallel run: time T = s + p = 1 per processor; processors are busy for p (parallel) and 1 processor for s: total processor-time P·T_P = P(s+p) = P.
Work W = s + pP. Hence

  T_o = P·T_P − W = P − (s + pP) = P(1 − p) − s = Ps − s = **s(P − 1) = α(P−1)**.

Efficiency E = W/(W+T_o) = (s+pP)/(s + pP + sP − s) = (s + pP)/(P(s+p)) = (s+pP)/P ✓ (= S/P, matches Task 04).

## 3. Isoefficiency function
Impose E = const = E₀. Solve E = W/(W + s(P−1)) = E₀ ⇒ W = [E₀/(1−E₀)]·s(P−1) ⇒ **W(P) = Θ(P)**; Precisely: for the Gustafson workload W(P) = s + pP ⇒ T_o/W = s(P−1)/(s+pP) → s/p, a constant ⇒ E → p = 1−α. So:

  **isoefficiency function of a Gustafson-compliant program: f(P) = Θ(P)** (linear in P) — the best (smallest) possible.

## 4. Critique
* Θ(P) is also the **lower bound** for any algorithm: to keep P processors busy at least Ω(P) work is needed (each needs a unit). So Gustafson scaling is, by
  construction, *perfectly scalable*; it is a statement about the *ideal point* of the isoefficiency spectrum.
* Real overhead is T_o = α(P−1) + C(P) + …: communication terms add P·C(P) ⇒ e.g. C = c log P gives T_o = Θ(P log P) ⇒ **f(P) = Θ(P log P)** (reduction-based programs, Task 12),
  C = c√P gives f(P) = Θ(P^{3/2}). For 2D-decomposed GEMM: T_o ≈ P·N²/√P = N²√P, so W = N³ ≥ K·N²√P ⇒ N = Ω(√P) ⇒ f(P) = Θ(P^{3/2}) in work (cf. Task 16, where fixed time needs only N ∝ P^{1/3}: the 2D algorithm cannot keep constant efficiency at constant time).
* If f(P) grows faster than the *memory-limited* growth of W (W ∝ P for memory-bounded Gustafson), efficiency cannot be maintained: need f(P) = O(P) (Sun–Ni memory function G(P)·W₁ ≥ f(P)).
* Gustafson's law is thus the *definition* of "scalable" in isoefficiency terms: a program whose isoefficiency is Θ(P) *is* a Gustafson-compliant program.
