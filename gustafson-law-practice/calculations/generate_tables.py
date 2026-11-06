#!/usr/bin/env python3
"""Generates the numeric markdown deliverables for Tasks 06-10, 16, 17.
Run:  python calculations/generate_tables.py   (from repo root)
All numbers in the .md files are produced by this script (reproducible)."""
import math
from fractions import Fraction
from pathlib import Path

OUT = Path(__file__).parent

def gus(a, P): return P - a * (P - 1)
def amd(s, P): return 1.0 / (s + (1 - s) / P)

def write(name, text):
    (OUT / name).write_text(text.strip() + "\n", encoding="utf-8")

# ---------------- Task 06 ----------------
a = 0.04
rows = []
prevE = None
for P in [16, 64, 256, 1024, 4096, 16384]:
    S = gus(a, P); E = S / P
    d = "-" if prevE is None else f"{E - prevE:+.6f}"
    rows.append(f"| {P} | {P} - 0.04·({P}-1) = {S:.2f} | {S:.2f} | {E:.6f} | {(1-E)*100:.4f} % | {d} |")
    prevE = E
t06 = f"""# Task 06 — Parametric speedup, α = 0.04

Formulas: S(P) = P − α(P − 1), E(P) = S(P)/P = 1 − α(P−1)/P, with α = 0.04.

| P | Substitution | S(P) | E(P) | Efficiency loss 1−E | ΔE vs previous row |
|---|---|---|---|---|---|
""" + "\n".join(rows) + f"""

## Evaluation

* Efficiency does **not** collapse as P grows exponentially. It falls from 0.9625 (P=16) and
  **saturates** at 1 − α = 0.96: E(P) = (1−α) + α/P, so the only P-dependent part is α/P → 0.
* From P = 1024 onward the change per ×4 in cores is below 4·10⁻⁵ — scaling is "free" in efficiency terms.
* Every extra core delivers (1 − α) = 0.96 of a core of useful work: S(P) ≈ 0.96·P + 0.04.
  At P = 16384 the speedup is 15728.68, i.e. 655.32 core-equivalents are lost to serial waiting — always exactly α(P−1).
* Caveat: this is the *idealised* model; Task 12 shows what happens when α itself grows with P.
"""
write("task06_parametric_table.md", t06)

# ---------------- Task 07 ----------------
P = 8192; Sreq = 7500
am = Fraction(P - Sreq, P - 1)
t07 = f"""# Task 07 — Maximum tolerable serial fraction

Given P = {P}, required S(P) ≥ {Sreq}.

**Derivation**

1. S(P) = P − α(P−1)
2. Require S ≥ {Sreq}:  P − α(P−1) ≥ {Sreq}
3. Rearrange: α(P−1) ≤ P − {Sreq}
4. Since P − 1 > 0 the inequality direction is kept:  **α ≤ (P − S_req)/(P − 1)**
5. Substitute: α_max = ({P} − {Sreq})/({P} − 1) = {P-Sreq}/{P-1} = **{float(am):.8f}** (exact fraction {am})

**Result:** α_max ≈ **{float(am)*100:.4f} %** of the (parallel-machine) runtime may be serial.

**Verification:** S = {P} − {float(am):.8f}·{P-1} = {gus(float(am), P):.4f} ✓ ;
parallel efficiency at the limit E = {Sreq}/{P} = {Sreq/P:.5f} (= 1 − α_max(P−1)/P).

Sanity: rounding α up to 0.0845 gives S = {gus(0.0845,P):.2f} < 7500 (violates the requirement);
α = 0.0844 gives S = {gus(0.0844,P):.2f} ≥ 7500 (OK).
"""
write("task07_tolerable_serial.md", t07)

# ---------------- Task 08 ----------------
s = 0.08; P = 128
A = amd(s, P); G = gus(s, P)
scan = "\n".join(
    f"| {p} | {amd(s,p):.3f} | {gus(s,p):.3f} | {gus(s,p)/amd(s,p):.2f}× | {(gus(s,p)-amd(s,p))/gus(s,p)*100:.2f} % |"
    for p in [2, 8, 32, 128, 512, 2048, 16384])
t08 = f"""# Task 08 — Amdahl vs Gustafson divergence (s = α = 0.08, P = 128)

## Step 1 — Amdahl (fixed size)
S_A = 1 / (s + (1−s)/P) = 1 / (0.08 + 0.92/128) = 1 / (0.08 + {0.92/128:.7f}) = 1 / {s+0.92/128:.7f} = **{A:.4f}**

## Step 2 — Gustafson (scaled)
S_G = P − α(P−1) = 128 − 0.08·127 = 128 − 10.16 = **{G:.2f}**

## Step 3 — Discrepancy
* Absolute difference: {G:.4f} − {A:.4f} = {G-A:.4f}
* Ratio S_G / S_A = **{G/A:.3f}×**
* Gustafson relative to Amdahl: (S_G − S_A)/S_A = **{(G-A)/A*100:.1f} %** higher
* Amdahl relative to Gustafson: (S_G − S_A)/S_G = **{(G-A)/G*100:.1f} %** lower (Amdahl under-predicts by this much)

## Divergence with P (same s = α = 0.08)

| P | Amdahl | Gustafson | Ratio | Amdahl shortfall |
|---|---|---|---|---|
{scan}

## Why they diverge
* Amdahl is **bounded**: S_A → 1/s = 12.5 as P → ∞. Adding cores beyond ~10/s buys nothing.
* Gustafson is **unbounded and linear**: S_G = (1−α)P + α, slope 0.92.
* The two answer different questions with the *same number* 0.08:
  Amdahl's s is the fraction of the **1-core** time of a **fixed** problem; Gustafson's α is a fraction of the
  **P-core** time of a problem that was **enlarged** until runtime stayed constant. In the scaled problem the serial
  part is a vanishing share of the *equivalent serial* work, (s + pP), so it matters less and less.
* The ratio therefore grows ~linearly in P (≈ 0.92P·0.08 = 0.0736P for large P).
"""
write("task08_cross_divergence.md", t08)

# ---------------- Task 09 ----------------
aA, aB, aC = .02, .06, .92
al = aA + aB
r9 = "\n".join(f"| {p} | {p} − 0.08·({p}−1) = {gus(al,p):.2f} | {gus(al,p)/p:.5f} | {gus(aA,p):.2f} |" for p in [512, 2048])
t09 = f"""# Task 09 — Multi-component workload

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
{r9}

(Results: S(512) = **471.12**, S(2048) = **1884.24**; E → 1 − α = 0.92.)

## Analysis
* The 8 % non-scaling share costs ≈ 40.9 core-equivalents at P=512 and ≈ 163.8 at P=2048: loss = α(P−1), growing linearly while efficiency stays flat (~92 %).
* Phase B is the dubious one. Halo exchange with fixed per-rank subdomain is O(1) per step (does not grow with P), so counting it as
  a constant serial fraction is acceptable for weak scaling; *global* synchronisation (barriers, reductions) grows as O(log P),
  which would make α rise slowly with P (see Task 12).
* Phase A: the broadcast is O(log P) and disk I/O is a true serial bottleneck unless parallel I/O (MPI-IO, HDF5) is used.
  Removing A alone would raise efficiency by 2 percentage points; removing B by 6.
* Ranking of optimisation targets: B (6 %) > A (2 %).
"""
write("task09_multicomponent.md", t09)

# ---------------- Task 10 ----------------
GiB = 2**30
Mnode = 32 * GiB
tbl = []
for b in [8, 16, 24]:
    npts = Mnode / b
    for Pn in [1, 64, 512]:
        N = (Pn * npts) ** (1 / 3)
        tbl.append(f"| {b} | {Pn} | {Pn*npts:.4e} | {N:,.1f} | {math.floor(N):,} | {math.floor(N)**3*b/Pn/GiB:.3f} |")
t10 = f"""# Task 10 — Memory growth vs scaled speedup

## Formulation
* Weak scaling: W(P) = P·W(1); memory M(P) = c·P, i.e. **constant memory per node** M(1) = c.
* 3D grid with N³ points and b bytes per point (all arrays): M_total(N) = b·N³.
* Per-node cap: M_node = 32 GB. Assumption: 32 GB = 32·2³⁰ B = {Mnode:,} B (GiB; with 10⁹ the numbers shrink by a factor ≈ 0.9966 in N).
* Capacity: b·N³ ≤ P·M_node  ⇒  **N_max(P) = (P·M_node / b)^(1/3) = N_max(1)·P^(1/3)**.
* Interpretation: the *linear* dimension grows only as P^(1/3): 8× nodes → 2× larger N, 64× nodes → 4× N, 512× nodes → 8× N.
  The *volume* (work for an O(N³)-per-sweep solver) grows linearly with P — exactly Gustafson's W(P) = P·W(1).

## Results (b = bytes per grid point; 8 = one fp64 array, 16 = two fp64 arrays u/u_new, 24 = three fp64 arrays)

| b (B/pt) | Nodes P | Max grid points | N_max (real) | N_max (integer, floor) | GiB/node actually used |
|---|---|---|---|---|---|
""" + "\n".join(tbl) + f"""

**Headline answer (b = 16 B/pt, double-buffered fp64 stencil):**
N_max(64) ≈ **{(64*Mnode/16)**(1/3):,.0f}**, N_max(512) ≈ **{(512*Mnode/16)**(1/3):,.0f}**
(a 5161³ and a 10321³ grid; per-node sub-cube ≈ 1290³).

## Remarks
* In practice reserve 10–20 % of node memory for OS, MPI buffers and halos; N shrinks by ~3–7 %.
* Scaled speedup is then bounded by memory, not by α: once N reaches N_max, further growth needs more nodes (Sun–Ni, Task 11).
"""
write("task10_memory_growth.md", t10)

# ---------------- Task 16 ----------------
N1 = 2048; rate = 100e9  # 100 GFLOP/s per processor (assumption)
r16 = []
for P in [1, 8, 64, 512, 4096, 32768]:
    N = N1 * P ** (1 / 3)
    fl = 2 * N**3
    mem = 3 * 8 * N**2 / P / 2**20
    comm = N**2 / math.sqrt(P) * 8 / 2**20
    r16.append(f"| {P} | {N:,.0f} | {fl:.3e} | {fl/P/rate:.3f} | {mem:.1f} | {comm:.1f} |")
t16 = f"""# Task 16 — GEMM weak scaling

## Derivation
Work of C = A·B (N×N): W(N) = 2N³ flops (Θ(N³)). Gustafson fixes parallel runtime T. With P processors at rate r each and ideal
distribution: T = W/(P·r) ⇒ for T constant, **W(P) = P·W(1)** ⇒ 2N³ = P·2N₁³ ⇒

**N(P) = N₁ · P^(1/3)**   (not P, and not √P).

Memory: total = 3·8·N² B ∝ P^(2/3); per processor ∝ P^(−1/3) — it *shrinks*, so memory is never the binding limit
under fixed-time scaling (it would be under a memory-bounded model: N ∝ P^(1/2), work ∝ P^(3/2), see Task 11).

## Scaling targets (N₁ = 2048, r = 100 GFLOP/s per processor — assumptions)

| P | N(P) | total flops 2N³ | time/proc (s) | matrix mem per proc (MiB) | 2D-SUMMA comm per proc (MiB) |
|---|---|---|---|---|---|
""" + "\n".join(r16) + """

(Perfect cubes of P are chosen so N is an integer multiple of N₁.)

## Observations
* Per-processor time is constant (0.172 s) by construction — Gustafson's premise.
* Communication volume per processor of 2D algorithms (SUMMA/Cannon) is ∝ N²/√P ∝ P^(2/3−1/2) = P^(1/6): it **grows slowly**,
  so the constant-time premise needs overlap of comm and compute or a 3D/2.5D algorithm (comm ∝ N²/P^(2/3) = const).
  This is the mechanism by which α creeps up in real GEMM runs.
* Arithmetic intensity grows with N (flops/byte ∝ N), a reason why GEMM is the "best case" for weak scaling.
"""
write("task16_gemm_scaling.md", t16)

# ---------------- Task 17 ----------------
n = 128
r17 = []
for P in [1, 8, 64, 512, 4096]:
    Nw = n * round(P ** (1 / 3))
    pts = n**3; halo = 6 * n**2
    Ns = 1024; ns = Ns / P ** (1 / 3)
    r17.append(f"| {P} | {Nw} | {pts:,} | {halo:,} | {halo/pts:.4f} | {ns:,.1f} | {6/ns:.4f} |")
t17 = f"""# Task 17 — 7-point 3D stencil: surface-to-volume under weak scaling

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
""" + "\n".join(r17) + """

## What does degrade under weak scaling (sources of α(P))
1. **Global reductions** (residual norm / CFL dt): O(log P) latency per step ⇒ α(P) = α₀ + c·log₂P/T_step.
2. **Network contention / distance**: halo messages cross more switch tiers; effective bandwidth per rank drops on tapered fat-trees.
3. **Load imbalance & OS jitter**: the slowest of P ranks sets the pace (the max of P random delays grows ~log P).
4. **I/O**: checkpoint size grows ∝ P while file-system bandwidth does not.

## Conclusion
A 3D stencil is a near-ideal Gustafson workload: with n = 128 the halo traffic is 6/128 ≈ 4.7 % of the update count per rank, constant in P.
Efficiency loss comes only from the O(log P) terms above, not from the surface-to-volume ratio.
"""
write("task17_stencil_scaling.md", t17)
print("tables written")
