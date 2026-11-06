# Task 18 — N-body: direct O(N²) vs Barnes–Hut O(N log N) under weak scaling

Goal: keep the time per iteration constant ⇒ work per processor constant: W(N)/P = const.

## 1. Required particle count N(P)
* **Direct all-pairs:** N²/P = N₁² ⇒ **N(P) = N₁·√P**.
* **Barnes–Hut:** N log N / P = N₁ log N₁ ⇒ N(P) ≈ P·N₁·(log N₁ / log N) — *almost* linear, a little below P·N₁ because log N grows.
  (Lambert-W: N ≈ P N₁ log N₁/ log N.)

Numerical (N₁ = 10⁵ particles on one processor, log base 2):

| P | N direct = N₁√P | N Barnes–Hut (solves N log₂N = P·N₁log₂N₁) | BH / (P·N₁) |
|---|---|---|---|
| 1 | 100 000 | 100 000 | 1.000 |
| 16 | 400 000 | 1 307 920 | 0.817 |
| 256 | 1 600 000 | 17 662 362 | 0.690 |
| 4096 | 6 400 000 | 244 167 412 | 0.596 |

Barnes–Hut weak-scales to ≈ 38× more particles than the direct method at P = 4096 for the same time per step.

## 2. How the serial/parallel ratio shifts
Let the serial part of an iteration (reading/writing N particles, global bookkeeping, sequential tree-top construction) cost σ·N, σ = per-particle serial cost, while the
parallel force computation takes a fixed T_par = T (constant by construction). Then

  α(P) = σN(P) / (σN(P) + T).

* **Direct:** N = N₁√P ⇒ serial time ∝ √P ⇒ α(P) ≈ σN₁√P/T grows as **P^{1/2}**.
* **Barnes–Hut:** N ≈ P·N₁/log-factor ⇒ serial time ∝ P/ log ⇒ α(P) grows nearly **linearly in P**. The *better* algorithm lets the problem grow faster, so
  every O(N) serial section (I/O, tree-top, diagnostics) weighs more on the constant-time budget: it hits the Amdahl wall sooner.

**Communication ratio (per rank, per step):**
* Direct: each rank needs (almost) all N positions: allgather volume ∝ N = N₁√P bytes vs constant compute ⇒ **comm/comp ∝ √P** (degrades).
* Barnes–Hut: locally-essential tree ≈ n_local^{2/3}-ish surface terms + O(log P) tree top ⇒ comm/comp grows only slowly (≈ log P); load-balance (space-filling-curve partitioning,
  costzones) is the larger risk since work per particle is data-dependent.

## 3. Conclusions
1. Direct method: Gustafson's law is not close to attainable — the comm term ∝ √P grows faster than a constant fraction (see Task 12 form C = c√P).
2. Barnes–Hut: near-ideal weak scaling *of the force kernel*, but α(P) increases because O(N) serial/replicated components dominate at large N. Fixes: parallel I/O, distributed tree construction, asynchronous
   diagnostics.
3. Choose scaling law by algorithm: N ∝ P^{1/2} (direct), N ∝ P/log P (tree/FMM) — **the weak-scaling dimension is a property of the algorithm's complexity**, not just of P.
