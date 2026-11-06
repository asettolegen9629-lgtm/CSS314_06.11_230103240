# Task 02 — Derivation of Gustafson's scaled speedup

**Setting.** A program is run on P identical processors. Normalize the *observed parallel wall-clock time* to 1:

  s + p = 1,      s = serial time (one processor busy, P−1 idle), p = time of the parallel section (all P processors busy). (1)

**Assumptions** (state them — the result is only as good as they are):
A1. The parallel section is perfectly divisible over P processors and scales to use them with no extra overhead.
A2. The workload is enlarged with P so that the parallel-run time stays constant (fixed-time).
A3. The serial time s does not depend on P (setup, I/O, control flow do not grow with the problem).
A4. The enlarged problem would run on one processor with the same per-unit speed.

**Step 1 — Work done on the parallel machine.**
The serial part takes s. During the parallel part each of P processors is busy for time p, so the parallel section contains P·p units of
processor-time of work. (justified by A1 and (1))

**Step 2 — Time the same enlarged job needs on ONE processor.**
No parallelism available: the single processor must run the serial part (s) and *then all* the parallel work, one piece after another:

  T₁ = s + P·p. (2)   (justified by A3, A4)

**Step 3 — Speedup by definition** S = T₁/T_P with T_P = s + p = 1:

  **S(P) = (s + P·p) / (s + p) = s + P·p.** (3)

**Step 4 — Rewrite in the serial fraction α.**
Because the run time is normalized, α = s/(s+p) = s and p = 1 − α. Substituting in (3):

  S(P) = α + P(1 − α)   (4)
     = α + P − Pα
     = P − α(P − 1)   ∎   (5)   (the last step: −Pα + α = −α(P − 1))

**Step 5 — Checks.**
* P = 1: S = 1 − 0 = 1 ✓. α = 0: S = P (ideal) ✓. α = 1: S = P − (P−1) = 1 (all serial, no gain) ✓.
* Slope dS/dP = 1 − α: each added processor contributes (1 − α) of a processor. Not 1/s-limited.
* Efficiency E = S/P = (1−α) + α/P → 1 − α.

**Step 6 — Equivalent serial workload** (what "scaled" means). Relative to the unit parallel run, the serial-equivalent problem has size
W_scaled = s + pP, i.e. the scaled problem is [(s + pP)/1] = S times bigger than one that would take time 1 on one processor.
