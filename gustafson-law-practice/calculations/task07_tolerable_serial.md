# Task 07 — Maximum tolerable serial fraction

Given P = 8192, required S(P) ≥ 7500.

**Derivation**

1. S(P) = P − α(P−1)
2. Require S ≥ 7500:  P − α(P−1) ≥ 7500
3. Rearrange: α(P−1) ≤ P − 7500
4. Since P − 1 > 0 the inequality direction is kept:  **α ≤ (P − S_req)/(P − 1)**
5. Substitute: α_max = (8192 − 7500)/(8192 − 1) = 692/8191 = **0.08448297** (exact fraction 692/8191)

**Result:** α_max ≈ **8.4483 %** of the (parallel-machine) runtime may be serial.

**Verification:** S = 8192 − 0.08448297·8191 = 7500.0000 ✓ ;
parallel efficiency at the limit E = 7500/8192 = 0.91553 (= 1 − α_max(P−1)/P).

Sanity: rounding α up to 0.0845 gives S = 7499.86 < 7500 (violates the requirement);
α = 0.0844 gives S = 7500.68 ≥ 7500 (OK).
