# gustafson-law-practice — Gustafson's Law & Weak Scaling (Parallel & Distributed Computing Architecture)

Practice repository for the ungraded task sheet *Gustafson's Law & Weak Scaling* (instructor: Sufyan bin Uzayr). 25 tasks: theory, calculations, analysis, benchmarks.

## Table of contents
1. [Executive technical guide](#1-executive-technical-guide)
2. [Core mathematical rules](#2-core-mathematical-rules)
3. [When to design around Gustafson weak scaling](#3-when-to-design-around-gustafson-weak-scaling)
4. [Execution commands](#4-execution-commands)
5. [Artifact index (Tasks 01–25)](#5-artifact-index)
6. [Data status / what must be re-run on your machine](#6-data-status)

## 1. Executive technical guide
* **Amdahl** answers "how much faster can this fixed problem go?" and gives the ceiling 1/s. **Gustafson** answers "how much bigger a problem can I solve in the same time?"
  and gives S = P − α(P−1), unbounded and linear, with efficiency floor 1−α (Tasks 01, 02, 04).
* They are one law in two frames: Gustafson = Amdahl on the P-times-larger problem, whose uniprocessor serial fraction is s₁ = α/(α+(1−α)P) (Task 03).
  The 1988 nCUBE result (≈1020× on 1024 processors) is the canonical demonstration (Task 05).
* Gustafson is an **upper bound**. It breaks when: serial work grows with N (Task 18), communication grows with P (Task 12), iteration counts grow with N (Task 13: CFL, CG), the machine's
  shared resources (bisection bandwidth, memory channels, file system) scale slower than P (Tasks 13, 20, 24), or memory, not time, is the binding limit (Sun–Ni, Tasks 10, 11).
* Dense GEMM (N ∝ P^{1/3} at fixed time, Task 16), 3D stencils (constant comm/comp = 6/n, Task 17) and Monte Carlo (α dominated by O(P) serial steps, Task 19) are near-ideal weak-scaling
  workloads; graph analytics (Task 20) and all-to-all algorithms are the hard cases.
* In isoefficiency terms Gustafson scaling is exactly Θ(P) — the best possible (Task 14); weak scaling is also energy-friendly: waste = α(P−1)·P_idle·T (Task 15).

## 2. Core mathematical rules
| Rule | Formula |
|---|---|
| Amdahl (fixed size) | S_A = 1/(s + (1−s)/P) ≤ 1/s |
| Gustafson (fixed time) | S = P − α(P−1) = s + pP |
| Efficiency | E = 1 − α(P−1)/P → 1 − α; Amdahl E_A = 1/(sP + 1 − s) → 0 |
| Max tolerable α | α_max = (P − S_req)/(P − 1) (Task 07: 0.0845 for P=8192, S≥7500) |
| Frame conversion | s₁(P) = α/(α + (1−α)P); α_P = s₁/(s₁ + (1−s₁)/P) |
| Sun–Ni | S = (s + pG(P))/(s + pG(P)/P); G=1 Amdahl, G=P Gustafson |
| With comm overhead | S_C = (s + pP)/(1 + C(P)); C = c·log P or c·√P ⇒ E → 0 slowly |
| Isoefficiency | T_o = α(P−1) ⇒ W = Θ(P) |
| Energy | ΔE = P_idle·T·α(P−1) |
| Fixed-time problem growth | N ∝ P^{1/d} (work N^d): GEMM N ∝ P^{1/3}; direct N-body N ∝ P^{1/2} |

## 3. When to design around Gustafson weak scaling
Use it when (1) a **bigger answer** (resolution, ensemble size, particles, batch) is valuable and the time budget is fixed; (2) per-rank work scales linearly with a size knob you control;
(3) serial/setup work is O(1) or parallelizable and communication is neighbour-local or O(log P); (4) memory per node is the natural capacity unit (design to fill memory — Task 10).
Do **not** rely on it when latency matters (fixed-size, real-time), when the work law couples size to time steps/iterations, or when the algorithm is all-to-all/irregular. Always validate with a measured α(P), not a single α.

## 4. Execution commands
```bash
pip install -r requirements.txt
python calculations/generate_tables.py                       # Tasks 06-10, 16, 17 (regenerates the .md tables)
python benchmarks/simulator.py --outdir plots                # Task 21 (CSV + overlay plots)
cd benchmarks/weak_scale_bench
python weak_bench.py --out ../results.csv                    # Task 22/23 (run on YOUR machine; --threads 1 2 4 8 12 16 for 8C/16T)
cd .. && python fit_gustafson.py                             # Task 23: summary.csv + fit_results.json (alpha_observed)
python plot_scaling.py --title "Ryzen 7 5825U"               # Task 24: ../plots/scaling_comparison.(png|pdf)
python collect_hw.py                                         # Task 24: analysis/hardware_snapshot.txt
```
Suggested git flow (atomic commits): `git add theory/task01* && git commit -m "feat: complete task 01 scaling models"` … one commit per task.

## 5. Artifact index
| Task | Topic | File |
|---|---|---|
| 01 | Amdahl vs Gustafson assumptions | [theory/task01_scaling_models.md](theory/task01_scaling_models.md) |
| 02 | Derivation of scaled speedup | [theory/task02_derivation.md](theory/task02_derivation.md) |
| 03 | Serial-fraction frame of reference | [theory/task03_serial_invariance.md](theory/task03_serial_invariance.md) |
| 04 | Asymptotic efficiency | [theory/task04_asymptotic_limits.md](theory/task04_asymptotic_limits.md) |
| 05 | nCUBE historical case | [theory/task05_historical_ncube.md](theory/task05_historical_ncube.md) |
| 06 | α = 0.04 parametric table | [calculations/task06_parametric_table.md](calculations/task06_parametric_table.md) |
| 07 | Max tolerable α | [calculations/task07_tolerable_serial.md](calculations/task07_tolerable_serial.md) |
| 08 | Amdahl vs Gustafson divergence | [calculations/task08_cross_divergence.md](calculations/task08_cross_divergence.md) |
| 09 | Multi-component workload | [calculations/task09_multicomponent.md](calculations/task09_multicomponent.md) |
| 10 | Memory growth limits | [calculations/task10_memory_growth.md](calculations/task10_memory_growth.md) |
| 11 | Sun–Ni comparison | [theory/task11_sun_ni_comparison.md](theory/task11_sun_ni_comparison.md) |
| 12 | Communication penalty model | [theory/task12_communication_penalty.md](theory/task12_communication_penalty.md) |
| 13 | Failure cases | [theory/task13_failure_cases.md](theory/task13_failure_cases.md) |
| 14 | Isoefficiency | [theory/task14_isoefficiency.md](theory/task14_isoefficiency.md) |
| 15 | Energy scaling | [theory/task15_energy_scaling.md](theory/task15_energy_scaling.md) |
| 16 | GEMM scaling | [calculations/task16_gemm_scaling.md](calculations/task16_gemm_scaling.md) |
| 17 | 3D stencil scaling | [calculations/task17_stencil_scaling.md](calculations/task17_stencil_scaling.md) |
| 18 | N-body scaling | [analysis/task18_nbody_scaling.md](analysis/task18_nbody_scaling.md) |
| 19 | Monte Carlo | [analysis/task19_monte_carlo.md](analysis/task19_monte_carlo.md) |
| 20 | Graph processing | [analysis/task20_graph_processing.md](analysis/task20_graph_processing.md) |
| 21 | Simulator | [benchmarks/simulator.py](benchmarks/simulator.py), outputs in [plots/](plots/) |
| 22 | Weak-scaling benchmark | [benchmarks/weak_scale_bench/](benchmarks/weak_scale_bench/) |
| 23 | Data + regression | `benchmarks/results.csv` (**generate**), [benchmarks/fit_gustafson.py](benchmarks/fit_gustafson.py) |
| 24 | Plots + hardware audit | [benchmarks/plot_scaling.py](benchmarks/plot_scaling.py), [analysis/task24_hardware_audit.md](analysis/task24_hardware_audit.md), `plots/scaling_comparison.*` (**generate**) |
| 25 | This README | README.md |

## 6. Data status
* Tasks 01–21 and 25 are complete and self-contained. Numbers in `calculations/` are reproducible via `generate_tables.py`.
* **Tasks 23–24 need a run on your own multi-core machine.** Drafted in a 1-vCPU sandbox, so only a pipeline smoke test exists (`benchmarks/results_sandbox_smoketest.csv`, `plots/smoketest_sandbox_1vcpu.*`) — it is **not**
  scaling data and must not be submitted as `results.csv`. After you run §4, fill the template at the end of `analysis/task24_hardware_audit.md` and (optionally) add the measured α to this README.
* Task 05 quotes historical figures from memory-level knowledge; verify against the cited papers before submission (note at top of that file).
