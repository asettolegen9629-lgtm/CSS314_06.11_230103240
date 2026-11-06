# Task 12 — Gustafson with a communication-overhead term C(P)

## 1. Model
Normalize the ideal weak-scaled run to s + p = 1. Add a communication/synchronization time C(P) ≥ 0, **normalized to that same unit** (C = t_comm/T_ideal), that
grows with P and is not overlapped with compute:

  T_P = s + p + C(P) = 1 + C(P)             (wall clock of the scaled problem)
  T₁ = s + pP                              (equivalent serial work; one processor has no inter-node communication)

  **S_C(P) = (s + pP) / (1 + C(P))**, E_C(P) = S_C/P = (s/P + p) / (1 + C(P)).   (modified Gustafson)

For C ≡ 0 this reduces to Gustafson's s + pP ✓ (derivation: same as Task 02 with the extra term in the denominator).

**Effective serial fraction.** Equating S_C = P − α_eff(P−1) gives α_eff(P) = (P − S_C)/(P − 1), which *rises* with P — the “constant α” assumption broken.
Equivalent alternative: treat C as extra serial time, S = (s + C + pP)/(1) — this version (C inside the numerator’s serial part at constant time T) models
"communication that can be hidden by shrinking the compute block" and is more optimistic; the version above is the conservative one.

## 2. Standard growth laws
* Tree reductions / barriers / latency-bound collectives: **C(P) = c·log₂P**
* 2D/3D mesh distance, all-to-all on a mesh, bisection-limited: **C(P) = c·√P** (2D) or c·P^{1/3}·(…) in 3D (generalize: c·P^β, 0<β<1).
* Neighbour-only halo exchange: C = c (constant) — folded into α.

## 3. Asymptotics
* C = c log₂P: S_C ≈ pP/(c log₂P) ⇒ **E_C ≈ p/(c log₂P) → 0** (very slowly).
* C = c·P^β: E_C ≈ p/(c P^β) → 0 as P^{−β}.
* The efficiency drops to ½ at 1 + C(P_{1/2}) = 2p: for α = 0.04 and C = 0.005 log₂P this needs log₂P ≈ 184 — never in practice; for C = 0.0005√P: P_{1/2} ≈ 3.4·10⁶.

## 4. Numerical illustration (α = 0.04; c_log = 0.005 per tree level; c_sqrt = 0.0005)

| P | S ideal (C=0) | C_log | S (log) | E (log) | C_sqrt | S (√) | E (√) |
|---|---|---|---|---|---|---|---|
| 16 | 15.40 | 0.020 | 15.10 | 0.9436 | 0.002 | 15.37 | 0.9606 |
| 256 | 245.80 | 0.040 | 236.35 | 0.9232 | 0.008 | 243.85 | 0.9525 |
| 4096 | 3932.20 | 0.060 | 3709.62 | 0.9057 | 0.032 | 3810.27 | 0.9302 |
| 65536 | 62914.60 | 0.080 | 58254.26 | 0.8889 | 0.128 | 55775.35 | 0.8511 |

(S = (0.04 + 0.96P)/(1 + C(P)). Note the crossing: √P overhead looks gentler at small P and is worse beyond ≈ 10⁴.)

## 5. Design implications
Overlap comm/compute (non-blocking collectives), use hierarchical/topology-aware collectives, reduce the *number* of global syncs per step (communication-avoiding
algorithms), and grow per-rank work (larger k) so C(P)/T_step shrinks: C is *normalized by the step time*.
