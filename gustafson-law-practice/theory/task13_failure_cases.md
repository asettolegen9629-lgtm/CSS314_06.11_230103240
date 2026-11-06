# Task 13 — When Gustafson's weak-scaling premise fails

Gustafson needs: (i) the problem can be enlarged proportionally to P, (ii) work per processor stays constant, (iii) serial/overhead time stays constant. Two algorithm
classes break (ii)/(iii) structurally.

## Case 1 — Explicit time-stepping PDE solver under a CFL condition (also: iterative solvers whose iteration count grows with N)
* 3D grid, N = n·P^{1/3} points per side, work per step N³. A stable explicit scheme needs Δt ∝ Δx ∝ 1/N, so for a fixed *simulated* time the **number of steps ∝ N**.
* Total work ∝ N⁴ = n⁴·P^{4/3}. With P processors the work per processor is n⁴P^{1/3} — **grows as P^{1/3}**.
* Wall-clock for the *same simulated time*: T(P) = T(1)·P^{1/3} (e.g. P = 4096: ×16; P = 32768: ×32).
* Constant-time premise broken ⇒ "work scales ∝ P at constant time" is impossible; you may only keep the **time per step** fixed. The honest weak-scaling
  metric becomes time per step, and S_G applies to *step throughput*, not to time-to-solution of a fixed physical problem.
* Same flavour: unpreconditioned CG on Poisson: iterations ∝ N ⇒ T ∝ P^{1/3}; multigrid restores O(1) iterations (algorithm change ⇒ Gustafson back).

## Case 2 — Distributed FFT / global sort / any all-to-all-dominated algorithm
* 1D FFT with N = nP points: compute per rank n log₂(nP)/… = n(log₂n + log₂P) → grows (mild, log P).
* The transpose is an **all-to-all**: half of the data crosses the network bisection. Data across bisection ∝ N/2 = nP/2; on a 3D torus the bisection bandwidth is ∝ P^{2/3}.
  Time_comm ≳ (nP/2)/(B·P^{2/3}) ∝ **n·P^{1/3}/B** — grows with P.
* Synchronization contention: all ranks wait for the slowest; message count P(P−1) in pairwise all-to-all (P−1 per rank) → latency term ∝ P·t_lat (or log P with Bruck).
* Result: constant per-rank work does **not** mean constant time; efficiency decays, and once the bisection term dominates, E decays roughly like P^{−1/3}.

## Case 3 (shorter) — Direct all-pairs N-body (see Task 18)
Work N², so N ∝ √P for equal time; but every rank must see all N positions: communication ∝ N ∝ √P per step per rank (allgather) while compute per rank is constant ⇒ comm/comp ∝ √P.

## Why the "constant runtime" premise breaks
1. **Complexity coupling:** the problem's own cost law ties extra resolution to extra *time-steps/iterations* (CFL, conditioning) — cost grows super-linearly in P.
2. **Bisection/contention:** communication volume that scales with *global* problem size crosses a resource (bisection links, shared file system, memory controller) that scales more slowly than P.
3. **Global dependence:** data-dependent global sync (reductions, convergence tests, barriers) adds latency-bound terms growing with P (log P at best, P at worst).
4. **Serial growth:** setup/mesh generation/I/O ∝ N ∝ P (Amdahl reappears with s_eff ∝ P ⇒ α_eff → const·P/T … no speedup beyond a bound).

## Takeaway
Before applying Gustafson, check (a) how the *iteration count* depends on N, (b) the *communication volume per rank* as P grows, (c) whether *serial setup* scales with N.
