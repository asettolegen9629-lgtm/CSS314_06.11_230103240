# Task 09 — Multi-component workload

| Phase | Description | Share of P-core runtime | Scales with P? |
|---|---|---|---|
| A | Initial disk I/O + parameter broadcast | 2 % | No (serial) |
| B | Boundary message-passing synchronization | 6 % | Treated as non-scaling (serial) |
| C | Core domain flux computation | 92 % | Yes (parallel) |

Check: 2 + 6 + 92 = 100 %.

## Aggregate serial fraction
α = A + B = 0.02 + 0.06 = **0.08** (p = 0.92)

## Scaled speedup  S(P) = P − α(P−1)

| P | S(P) (α = 0.08) | E(P) | S(P) if B were fully overlapped (α = 0.02) |
|---|---|---|---|
| 512 | 512 − 0.08·(512−1) = 471.12 | 0.92016 | 501.78 |
| 2048 | 2048 − 0.08·(2048−1) = 1884.24 | 0.92004 | 2007.06 |

(Results: S(512) = **471.12**, S(2048) = **1884.24**; E → 1 − α = 0.92.)

## Analysis
* The 8 % non-scaling share costs ≈ 40.9 core-equivalents at P=512 and ≈ 163.8 at P=2048: loss = α(P−1), growing linearly while efficiency stays flat (~92 %).
* Phase B is the dubious one. Halo exchange with fixed per-rank subdomain is O(1) per step (does not grow with P), so counting it as
  a constant serial fraction is acceptable for weak scaling; *global* synchronisation (barriers, reductions) grows as O(log P),
  which would make α rise slowly with P (see Task 12).
* Phase A: the broadcast is O(log P) and disk I/O is a true serial bottleneck unless parallel I/O (MPI-IO, HDF5) is used.
  Removing A alone would raise efficiency by 2 percentage points; removing B by 6.
* Ranking of optimisation targets: B (6 %) > A (2 %).
