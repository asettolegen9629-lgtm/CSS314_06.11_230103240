# Task 24 — Hardware audit and interpretation of deviations

> **Data status.** The final empirical plot `plots/scaling_comparison.(png|pdf)` and the numbers in §3 must be produced **on your own machine**:
> run `benchmarks/weak_scale_bench/weak_bench.py` → `fit_gustafson.py` → `plot_scaling.py` → `collect_hw.py` (see README). The sandbox where this repo was drafted has only
> **1 vCPU**, so its output (`plots/smoketest_sandbox_1vcpu.*`, `benchmarks/*_sandbox_smoketest.*`) only proves that the pipeline runs; it is not a scaling measurement (α ≈ 1, as expected for P workers sharing one core).

## 1. Target machine (fill/verify with `python benchmarks/collect_hw.py` → `analysis/hardware_snapshot.txt`)

| Item | Value (known from your notes; ✎ = confirm with the snapshot) |
|---|---|
| CPU | AMD Ryzen 7 5825U (Zen 3 "Barcelo-U" mobile APU) |
| Cores / threads | 8 cores / 16 logical processors (2-way SMT) |
| Clocks | ~2.0 GHz base, boost up to ~4.5 GHz ✎ |
| Power envelope | 15 W class (configurable ~10–25 W) ✎ |
| Cache hierarchy | L1: 32 KB I + 32 KB D per core ✎; **L2: 512 KB per core (4 MB total)**; **L3: 16 MB shared** by all 8 cores (single core complex) |
| RAM | 15.4 GB usable (16 GB installed class); channels/speed ✎ — typically dual-channel (128-bit) DDR4-3200 or LPDDR4x on this APU class |
| NUMA | Single socket, single memory controller → **one NUMA node** |
| OS / runtime | Windows (Russian UI), Python 3.12 and 3.14 installed |

For comparison, the drafting sandbox (`analysis/hardware_snapshot_sandbox.txt`): Intel Xeon @ 2.1 GHz (Sapphire Rapids class) under KVM, **1 vCPU**, L1d 48 KiB, L2 2 MiB, L3 260 MiB reported (shared host cache), ~3–4 GB RAM, 1 NUMA node.

## 2. Expected shape of the curve on this machine (to compare against your data)
1. **P = 1…8 (physical cores):** near-linear if the kernel is compute-bound (the integral workload is a streaming NumPy kernel; chunks of 10⁶ doubles = 8 MB per temp array
   exceed L2, so memory bandwidth starts to matter ⇒ efficiency may sag early). Fit α here is dominated by the intentionally serial master phase + process dispatch.
2. **P = 9…16 (SMT siblings):** two threads share the execution units, L1/L2 and the FPU: expect **≈ 1.1–1.3× per core**, not 2×, so S(16) well below the Gustafson line
   fitted from P ≤ 8 data. This is a *hardware* "serial fraction", unrelated to the program's α.
3. **Memory channels:** weak scaling fixes work per worker, so total memory traffic grows ∝ P over a **shared 128-bit bus** (~50 GB/s class) — this creates a
   P-dependent α_eff exactly like a shared resource contention term (Task 12/13).
4. **Python/Windows specifics:** `multiprocessing` uses *spawn*: process start and pickling are paid once per `Pool` (warm-up excluded from timings) but task dispatch + result gather
   is a per-run serial cost → part of the measured α.

## 3. Deviations to look for and how to attribute them

| Symptom | Likely cause | How to confirm |
|---|---|---|
| Efficiency declines steadily with P and first run in a series is slowest | **Thermal/power throttling** (mobile 15 W part: boost drops from ≈ 4.5 GHz at 1 core to a lower all-core clock) | Log clocks (HWiNFO / `Get-Counter "\Processor Information(_Total)\% Processor Performance"`) during runs; compare run 1 vs run 5; run with the laptop on a hard surface, High-performance power plan, and repeat after a 2-min cooldown |
| Knee at P = 8 | SMT: threads 9–16 are not real cores | Plot per-P efficiency; fit α with P ≤ 8 only (`--threads 1 2 4 6 8`) and compare |
| Plateau in speedup although cores idle | **Memory-bandwidth saturation** | Shrink the chunk so data fits in L2 (`CHUNK` 20k doubles); curve should straighten |
| Large run-to-run std at big P | OS scheduling, background tasks, Windows Defender | Close apps; more runs; use medians |
| "NUMA boundary" effects | **None expected** on this 1-node, single-CCX machine (cross-NUMA/CCX penalties appear on Threadripper/EPYC, multi-socket Xeons) — state this explicitly in your report and mention what would change on a dual-socket server (remote-memory latency ×1.5–2, first-touch page placement, `numactl --interleave`) | `collect_hw.py` shows 1 NUMA node |
| S(P) > P at small P | Turbo/boost rebalance, cache effects, T(1) measured at a cold clock | Warm-up (already done), pin baseline repeats |

## 4. Write-up template for your measured results
* Fitted α = ___ ± ___ (from `fit_results.json`), R² = ___, T(1) = ___ s, k = ___ points/worker.
* Gustafson fit vs ideal vs Amdahl (same s): at P = 8: S = ___ (ideal 8), P = 16: S = ___ (ideal 16).
* Largest deviation from fit at P = ___, attributed to ___ (SMT / bandwidth / thermal), evidence: ___.
