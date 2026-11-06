# Task 17 — 7-point 3D stencil: surface-to-volume under weak scaling

## Setup
Global grid N³ decomposed over P ranks in a ∛P × ∛P × ∛P process grid; each rank owns an n×n×n block, n = N/P^(1/3).

* Computation per rank per sweep: ~ n³ updates (≈ 8 flops each for the 7-point stencil).
* Communication per rank per sweep: 6 faces × n² points (halo exchange, depth 1) = 6n².
* Communication-to-computation ratio: **R = 6n²/n³ = 6/n**.

## Weak scaling (Gustafson): global volume N³ = P·n³
* Gustafson keeps work per rank fixed ⇒ n fixed ⇒ N = n·P^(1/3).
* Therefore **R_weak = 6/n = constant, independent of P** — it neither improves nor degrades.
  (Neighbour exchange cost is also P-independent: ≤ 6 messages of 8n² bytes.)
* The ratio of the *global* surface to the *global* volume, ∼6/N, does shrink as N grows, but it is irrelevant: only
  inter-rank faces generate traffic, and every rank always has the same 6 faces.

## Strong scaling (Amdahl-like) for contrast: N fixed
n = N/P^(1/3) ⇒ R_strong = 6P^(1/3)/N, which **degrades as P^(1/3)** — the surface-to-volume effect.

| P | N (weak, n=128) | points/rank | halo pts/rank | R weak = 6/n | n (strong, N=1024) | R strong |
|---|---|---|---|---|---|---|
| 1 | 128 | 2,097,152 | 98,304 | 0.0469 | 1,024.0 | 0.0059 |
| 8 | 256 | 2,097,152 | 98,304 | 0.0469 | 512.0 | 0.0117 |
| 64 | 512 | 2,097,152 | 98,304 | 0.0469 | 256.0 | 0.0234 |
| 512 | 1024 | 2,097,152 | 98,304 | 0.0469 | 128.0 | 0.0469 |
| 4096 | 2048 | 2,097,152 | 98,304 | 0.0469 | 64.0 | 0.0937 |

## What does degrade under weak scaling (sources of α(P))
1. **Global reductions** (residual norm / CFL dt): O(log P) latency per step ⇒ α(P) = α₀ + c·log₂P/T_step.
2. **Network contention / distance**: halo messages cross more switch tiers; effective bandwidth per rank drops on tapered fat-trees.
3. **Load imbalance & OS jitter**: the slowest of P ranks sets the pace (the max of P random delays grows ~log P).
4. **I/O**: checkpoint size grows ∝ P while file-system bandwidth does not.

## Conclusion
A 3D stencil is a near-ideal Gustafson workload: with n = 128 the halo traffic is 6/128 ≈ 4.7 % of the update count per rank, constant in P.
Efficiency loss comes only from the O(log P) terms above, not from the surface-to-volume ratio.
