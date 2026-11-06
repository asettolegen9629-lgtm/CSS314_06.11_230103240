# Task 05 — Historical case: 1024-processor nCUBE/ten and "Amdahl's pessimism"

> **Source-verification note.** The qualitative story below is standard. Before submitting, check the exact figures against the primary sources:
> J. L. Gustafson, "Reevaluating Amdahl's Law," *Commun. ACM* 31(5), 532–533 (1988); and Gustafson, Montry, Benner,
> "Development of Parallel Methods for a 1024-Processor Hypercube," *SIAM J. Sci. Stat. Comput.* 9(4), 609–638 (1988).
> Numbers I am less than fully sure of are marked (≈/verify).

## 1. Scenario
* **Where/who:** Sandia National Laboratories; Gustafson, Montry, Benner; an nCUBE 10 hypercube with 1024 processors (10-dimensional hypercube, each node with a
  small local memory — hundreds of KB, verify).
* **Applications (real engineering problems):** structural-beam strain analysis, surface-wave (baffled) simulation, unstable fluid-flow (vortex) — all
  grid-based, with a parallel kernel and a small sequential part (setup, I/O, global control).
* **Result:** scaled speedups on the order of **1020×** on 1024 processors (reported ≈ 1016–1021 across the three codes, verify), i.e. ≈ 99 % efficiency,
  **measured on the parallel machine**.
* **Why it looked impossible:** the community's reading of Amdahl said "with a serial fraction of 0.4 %, speedup ≤ 1/0.004 = 250".
  Exact Amdahl value for s = 0.004 on 1024 processors: S = 1/(0.004 + 0.996/1024) = **201**. Observed ≈ 1020 is **5× above** that.
  (Quoted serial fractions in the paper: ≈ 0.4–0.8 %.)

## 2. How problem expansion dismantled the ceiling
1. A single node could only hold a small problem; the full machine let the researchers use a ~1024× larger mesh *in the same run time*.
2. In the enlarged run the parallel section grew ≈ ×1024 while the sequential section (setup, I/O, control) stayed ~constant in absolute time.
3. Observed on the parallel machine: serial fraction s′ ≈ 0.4–0.8 % of the **parallel** wall-clock. Scaled speedup
   S = P − (P−1)s′ = 1024 − 1023·0.004 = **1019.9**, and for s′ = 0.008: **1015.8** — matches the reported 1016–1021 range.
   Reverse engineering the reported speedups gives s′ = (1024−S)/1023 = 0.29 % (S=1021) … 0.78 % (S=1016).
4. Amdahl's s was implicitly taken as a constant of the *program*; in these codes it was a property of the *(problem size, P)* pair and the 1-processor
   fraction of the enlarged problem was ≈ s′/(s′ + (1−s′)·1024) ≈ 4·10⁻⁶ (see Task 03) — far from 0.4 %.

## 3. Methodological point: scaled speedup cannot be measured against 1 processor
The enlarged problem did not fit in one node. So the uniprocessor time had to be **estimated** from the parallel run:
T₁ ≈ (s′ + p′·P)·T_P. This is why Gustafson insisted on measuring the serial fraction on the parallel machine (Task 03).
A modern analogue: weak-scaling studies in Task 22–24 compute S from T(1) of a per-node-sized problem, not from a time-to-solution of the whole.

## 4. Lessons
* Amdahl's ceiling is a statement about fixed-size problems; it never said massively parallel machines are useless.
* The paper shifted benchmarking practice towards *scaled* metrics (e.g. LINPACK HPL grows N to fill memory; Top500 runs).
* Limits remain (Tasks 11–13): memory, communication and algorithmic complexity may prevent constant-time scaling.
