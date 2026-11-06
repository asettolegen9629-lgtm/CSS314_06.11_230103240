#!/usr/bin/env python3
"""Task 23 - statistics + least-squares extraction of the empirical serial fraction.

Input : results.csv   (columns: threads, run, wall_s, ...)   from weak_scale_bench/weak_bench.py
Output: summary.csv   (mean/std/SEM of wall time and scaled speedup per thread count)
        fit_results.json (alpha_observed, standard error, R^2, unconstrained fit for reference)

Model (Gustafson):  S(P) = P - alpha*(P-1)   <=>   S(P)-1 = (1-alpha)*(P-1)
Weak-scaling measurement: S_run(P) = P * T1 / t_run(P),   T1 = mean wall time at P = 1.
Fit: ordinary least squares of y = S-1 on x = P-1 through the origin (S(1)=1 by definition);
     slope m = sum(xy)/sum(x^2),  alpha = 1 - m,  SE(alpha) = SE(m) = sqrt( SSR/(n-1) / sum(x^2) ).
Uses all individual runs (not just the means) so run-to-run noise enters the standard error.
"""
import argparse, csv, json, math
from collections import defaultdict
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--input", default="results.csv")
ap.add_argument("--summary", default="summary.csv")
ap.add_argument("--json", default="fit_results.json")
a = ap.parse_args()

times = defaultdict(list)
with open(a.input, newline="") as f:
    for r in csv.DictReader(f):
        times[int(r["threads"])].append(float(r["wall_s"]))
if 1 not in times:
    raise SystemExit("need runs with threads=1 as the baseline")
Ps = sorted(times)
if len([p for p in Ps if p > 1]) < 2:
    print("WARNING: fewer than two thread counts > 1; regression is weak (task asks for >= 5 counts)")
T1 = float(np.mean(times[1]))

summary, xs, ys = [], [], []
for P in Ps:
    t = np.array(times[P]); n = len(t)
    S = P * T1 / t
    summary.append(dict(threads=P, n_runs=n, mean_t=t.mean(), std_t=t.std(ddof=1) if n > 1 else 0.0,
                        mean_S=S.mean(), std_S=S.std(ddof=1) if n > 1 else 0.0,
                        sem_S=(S.std(ddof=1) / math.sqrt(n)) if n > 1 else 0.0, efficiency=S.mean() / P))
    xs += [P - 1] * n; ys += list(S - 1)
x, y = np.array(xs, float), np.array(ys, float)
m = float((x * y).sum() / (x * x).sum())
res = y - m * x
dof = max(len(x) - 1, 1)
se = math.sqrt(float((res ** 2).sum()) / dof / float((x * x).sum()))
ybar = y.mean(); r2 = 1 - float((res ** 2).sum()) / float(((y - ybar) ** 2).sum()) if len(y) > 1 else float("nan")
# unconstrained reference fit  S = c1*P + c0  (Gustafson predicts c1 = 1-alpha, c0 = alpha)
Pall = np.array([P for P in Ps for _ in times[P]], float); Sall = y + 1
c1, c0 = np.polyfit(Pall, Sall, 1)
out = dict(alpha_observed=1 - m, alpha_std_error=se, slope=m, r_squared=r2, T1_mean_s=T1,
           unconstrained_slope=float(c1), unconstrained_intercept=float(c0),
           thread_counts=Ps, runs_per_count=[len(times[p]) for p in Ps])
with open(a.summary, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(summary[0])); w.writeheader(); w.writerows(summary)
with open(a.json, "w") as f: json.dump(out, f, indent=2)
print(f"{'P':>4} {'mean t (s)':>11} {'std t':>9} {'mean S':>9} {'sem S':>8} {'E':>7}")
for s in summary:
    print(f"{s['threads']:>4} {s['mean_t']:>11.4f} {s['std_t']:>9.4f} {s['mean_S']:>9.3f} {s['sem_S']:>8.3f} {s['efficiency']:>7.3f}")
print(f"\nalpha_observed = {out['alpha_observed']:.4f} +/- {se:.4f}   (R^2 = {r2:.3f})")
