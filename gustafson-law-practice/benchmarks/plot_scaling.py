#!/usr/bin/env python3
"""Task 24 - plots: ideal, Gustafson (regression fit), measured +- SEM, Amdahl (same serial fraction).
Run after fit_gustafson.py:  python plot_scaling.py [--title "Ryzen 7 5825U, 5 runs"]"""
import argparse, csv, json
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument("--summary", default="summary.csv"); ap.add_argument("--json", default="fit_results.json")
ap.add_argument("--outdir", default="../plots"); ap.add_argument("--title", default="")
a = ap.parse_args()
rows = list(csv.DictReader(open(a.summary)))
P = np.array([int(r["threads"]) for r in rows]); S = np.array([float(r["mean_S"]) for r in rows])
E = np.array([float(r["sem_S"]) for r in rows])
fit = json.load(open(a.json)); al = fit["alpha_observed"]; se = fit["alpha_std_error"]
Pf = np.linspace(1, P.max(), 200)
fig, ax = plt.subplots(figsize=(7.5, 5.2))
ax.plot(Pf, Pf, "k:", label="ideal linear  S = P")
ax.plot(Pf, Pf - al * (Pf - 1), "-", color="C0", label=f"Gustafson fit  α = {al:.3f} ± {se:.3f}")
ax.plot(Pf, 1 / (al + (1 - al) / Pf), "--", color="C3", label=f"Amdahl, same s = {al:.3f}")
ax.errorbar(P, S, yerr=E, fmt="o", color="C2", capsize=3, label="measured (mean ± SEM)")
ax.set_xlabel("workers P (constant work k per worker)"); ax.set_ylabel("scaled speedup S(P) = P·T(1)/T(P)")
ax.set_title("Weak scaling: measured vs Gustafson vs Amdahl" + (f"\n{a.title}" if a.title else ""))
ax.grid(alpha=.3); ax.legend(fontsize=8)
out = Path(a.outdir); out.mkdir(exist_ok=True)
for ext in ("png", "pdf"): fig.savefig(out / f"scaling_comparison.{ext}", dpi=300, bbox_inches="tight")
print("wrote", out / "scaling_comparison.png", "and .pdf")
