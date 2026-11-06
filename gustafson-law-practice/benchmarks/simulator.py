#!/usr/bin/env python3
"""Task 21 - Amdahl vs Gustafson parametric simulator.

Examples
  python benchmarks/simulator.py                       # defaults, writes CSV + plots
  python benchmarks/simulator.py --alphas 0.01 0.05 --pmax 4096 --outdir out
Domain enforced: 1 <= P <= 65536, 0.001 <= alpha <= 0.20.
Output: <outdir>/speedup_model.csv, <outdir>/overlay_speedup.(png|pdf), <outdir>/overlay_efficiency.(png|pdf)
"""
import argparse, csv, sys
from pathlib import Path

def amdahl(s, P):    return 1.0 / (s + (1.0 - s) / P)
def gustafson(a, P): return P - a * (P - 1)

def core_counts(pmax):
    out, p = [], 1
    while p <= pmax:
        out.append(p); p *= 2
    if out[-1] != pmax: out.append(pmax)
    return out

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--alphas", type=float, nargs="+", default=[0.001, 0.01, 0.05, 0.10, 0.20])
    ap.add_argument("--pmax", type=int, default=65536)
    ap.add_argument("--outdir", default="plots")
    ap.add_argument("--csv", default=None, help="CSV path (default <outdir>/speedup_model.csv)")
    ap.add_argument("--no-plots", action="store_true")
    a = ap.parse_args()
    if not 1 <= a.pmax <= 65536: sys.exit("pmax must be in [1, 65536]")
    if any(not 0.001 <= x <= 0.20 for x in a.alphas): sys.exit("alpha must be in [0.001, 0.20]")
    out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True)
    Ps = core_counts(a.pmax)
    rows = []
    for al in a.alphas:
        for P in Ps:
            sa, sg = amdahl(al, P), gustafson(al, P)
            rows.append(dict(alpha=al, P=P, amdahl_speedup=sa, gustafson_speedup=sg,
                             amdahl_efficiency=sa / P, gustafson_efficiency=sg / P,
                             amdahl_limit=1 / al, ratio_gustafson_over_amdahl=sg / sa))
    csv_path = Path(a.csv) if a.csv else out / "speedup_model.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(f"wrote {csv_path} ({len(rows)} rows)")
    if a.no_plots: return
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    cmap = plt.get_cmap("tab10")
    # speedup overlay
    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.plot(Ps, Ps, "k:", lw=1, label="ideal S=P")
    for i, al in enumerate(a.alphas):
        ax.plot(Ps, [gustafson(al, P) for P in Ps], "-", color=cmap(i), label=f"Gustafson α={al}")
        ax.plot(Ps, [amdahl(al, P) for P in Ps], "--", color=cmap(i), label=f"Amdahl s={al}")
    ax.set_xscale("log", base=2); ax.set_yscale("log")
    ax.set_xlabel("processors P"); ax.set_ylabel("speedup S(P)")
    ax.set_title("Strong (Amdahl, dashed) vs weak (Gustafson, solid) scaling")
    ax.grid(True, which="both", alpha=.3); ax.legend(fontsize=7, ncol=2)
    for ext in ("png", "pdf"): fig.savefig(out / f"overlay_speedup.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)
    # efficiency overlay
    fig, ax = plt.subplots(figsize=(8, 5))
    for i, al in enumerate(a.alphas):
        ax.plot(Ps, [gustafson(al, P) / P for P in Ps], "-", color=cmap(i), label=f"Gustafson α={al}")
        ax.plot(Ps, [amdahl(al, P) / P for P in Ps], "--", color=cmap(i), label=f"Amdahl s={al}")
    ax.set_xscale("log", base=2); ax.set_xlabel("processors P"); ax.set_ylabel("parallel efficiency E(P)")
    ax.set_ylim(0, 1.02); ax.grid(True, which="both", alpha=.3); ax.legend(fontsize=7, ncol=2)
    ax.set_title("Efficiency: Gustafson → 1−α, Amdahl → 0")
    for ext in ("png", "pdf"): fig.savefig(out / f"overlay_efficiency.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"plots written to {out}/")

if __name__ == "__main__":
    main()
