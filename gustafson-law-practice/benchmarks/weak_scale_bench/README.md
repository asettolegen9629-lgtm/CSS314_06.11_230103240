# weak_scale_bench — how to run

Requirements: Python ≥ 3.9, `numpy` (benchmark), `matplotlib` (plots).  `pip install numpy matplotlib`

```bash
cd benchmarks/weak_scale_bench
python weak_bench.py --out ../results.csv                 # all powers of two up to os.cpu_count(), 5 runs each
python weak_bench.py --threads 1 2 4 8 12 16 --k 20000000 --out ../results.csv   # e.g. Ryzen 7 5825U (16 logical CPUs)
cd .. && python fit_gustafson.py                          # regression -> fit_results.json, summary.csv
python plot_scaling.py                                    # ../plots/scaling_comparison.(png|pdf)
python collect_hw.py                                      # hardware facts for analysis/task24_hardware_audit.md
```

Method: each of P workers integrates 4/(1+x²) with a constant `k` points → total work = P·k. A fixed serial
phase (master-side setup of `serial_frac·k` points + final reduction) provides a measurable α.
Scaled speedup S(P) = P·T(1)/T(P). Tips for clean data: plug in power, close other programs, fix the Windows power plan to
"High performance", run once to warm up, and keep thread counts ≤ logical CPUs (SMT threads share a core, so expect the curve
to bend after 8 on an 8-core/16-thread CPU).
