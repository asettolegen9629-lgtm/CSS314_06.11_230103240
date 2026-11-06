# Task 10 — Memory growth vs scaled speedup

## Formulation
* Weak scaling: W(P) = P·W(1); memory M(P) = c·P, i.e. **constant memory per node** M(1) = c.
* 3D grid with N³ points and b bytes per point (all arrays): M_total(N) = b·N³.
* Per-node cap: M_node = 32 GB. Assumption: 32 GB = 32·2³⁰ B = 34,359,738,368 B (GiB; with 10⁹ the numbers shrink by a factor ≈ 0.9966 in N).
* Capacity: b·N³ ≤ P·M_node  ⇒  **N_max(P) = (P·M_node / b)^(1/3) = N_max(1)·P^(1/3)**.
* Interpretation: the *linear* dimension grows only as P^(1/3): 8× nodes → 2× larger N, 64× nodes → 4× N, 512× nodes → 8× N.
  The *volume* (work for an O(N³)-per-sweep solver) grows linearly with P — exactly Gustafson's W(P) = P·W(1).

## Results (b = bytes per grid point; 8 = one fp64 array, 16 = two fp64 arrays u/u_new, 24 = three fp64 arrays)

| b (B/pt) | Nodes P | Max grid points | N_max (real) | N_max (integer, floor) | GiB/node actually used |
|---|---|---|---|---|---|
| 8 | 1 | 4.2950e+09 | 1,625.5 | 1,625 | 31.971 |
| 8 | 64 | 2.7488e+11 | 6,502.0 | 6,501 | 31.985 |
| 8 | 512 | 2.1990e+12 | 13,004.0 | 13,003 | 31.993 |
| 16 | 1 | 2.1475e+09 | 1,290.2 | 1,290 | 31.988 |
| 16 | 64 | 1.3744e+11 | 5,160.6 | 5,160 | 31.988 |
| 16 | 512 | 1.0995e+12 | 10,321.3 | 10,321 | 31.997 |
| 24 | 1 | 1.4317e+09 | 1,127.1 | 1,127 | 31.995 |
| 24 | 64 | 9.1626e+10 | 4,508.2 | 4,508 | 31.995 |
| 24 | 512 | 7.3301e+11 | 9,016.5 | 9,016 | 31.995 |

**Headline answer (b = 16 B/pt, double-buffered fp64 stencil):**
N_max(64) ≈ **5,161**, N_max(512) ≈ **10,321**
(a 5161³ and a 10321³ grid; per-node sub-cube ≈ 1290³).

## Remarks
* In practice reserve 10–20 % of node memory for OS, MPI buffers and halos; N shrinks by ~3–7 %.
* Scaled speedup is then bounded by memory, not by α: once N reaches N_max, further growth needs more nodes (Sun–Ni, Task 11).
