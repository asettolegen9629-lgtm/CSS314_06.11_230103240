#!/usr/bin/env python3
"""Task 22 - empirical weak-scaling benchmark (Python multiprocessing, NumPy).

Workload: midpoint-rule integration of f(x)=4/(1+x^2) (the integral is pi).
Weak scaling: every worker integrates the SAME number of points k on its own sub-interval,
so the total problem is P*k points. The serial phase (task setup in the master, a fixed
"serial_frac * k" amount of master-side work that models parameter setup / output, and the
final reduction) does NOT grow with P  ->  a measurable alpha.

  Scaled speedup  S(P) = P * T(1) / T(P)      (work done / time, relative to 1 worker)
  Scaled efficiency E(P) = S(P)/P = T(1)/T(P)

Usage (Linux/macOS/Windows):
  python weak_bench.py                       # threads 1,2,4,... up to os.cpu_count(), 5 runs each
  python weak_bench.py --k 20000000 --runs 5 --threads 1 2 4 8 12 16 --out ../results.csv
Windows note: uses 'spawn'; the __main__ guard below is required.
"""
import argparse, csv, math, os, platform, time
from multiprocessing import Pool
import numpy as np

CHUNK = 1_000_000

def integrate(args):
    """Midpoint rule on [a,b] with n points; returns partial integral."""
    a, b, n = args
    h = (b - a) / n
    total = 0.0
    done = 0
    while done < n:
        m = min(CHUNK, n - done)
        x = a + (done + np.arange(m) + 0.5) * h
        total += float(np.sum(4.0 / (1.0 + x * x)))
        done += m
    return total * h

def run_once(pool, P, k, serial_frac):
    t0 = time.perf_counter()
    # ---- serial phase 1: setup in master (fixed size, independent of P)
    integrate((0.0, 1.0, int(serial_frac * k)))
    tasks = [(i / P, (i + 1) / P, k) for i in range(P)]
    # ---- parallel phase
    parts = pool.map(integrate, tasks, chunksize=1)
    # ---- serial phase 2: reduction
    val = math.fsum(parts)
    return time.perf_counter() - t0, val

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=20_000_000, help="points per worker (constant)")
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--threads", type=int, nargs="+", default=None)
    ap.add_argument("--serial-frac", type=float, default=0.02, help="master-side serial work as fraction of k")
    ap.add_argument("--out", default="results.csv")
    a = ap.parse_args()
    maxp = os.cpu_count() or 1
    if a.threads is None:
        a.threads, p = [], 1
        while p < maxp: a.threads.append(p); p *= 2
        a.threads.append(maxp)
    print(f"host={platform.platform()} cpu_count={maxp} k={a.k} threads={a.threads}")
    rows = []
    for P in a.threads:
        with Pool(P) as pool:
            pool.map(integrate, [(0.0, 1.0, 1000)] * P)       # warm-up (process start, imports)
            for r in range(1, a.runs + 1):
                t, val = run_once(pool, P, a.k, a.serial_frac)
                rows.append(dict(threads=P, run=r, wall_s=t, k_per_worker=a.k, pi_estimate=val))
                print(f"P={P:3d} run={r} t={t:8.4f}s pi={val:.12f}")
    with open(a.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print("wrote", a.out)

if __name__ == "__main__":
    main()
