# Task 06 — Parametric speedup, α = 0.04

Formulas: S(P) = P − α(P − 1), E(P) = S(P)/P = 1 − α(P−1)/P, with α = 0.04.

| P | Substitution | S(P) | E(P) | Efficiency loss 1−E | ΔE vs previous row |
|---|---|---|---|---|---|
| 16 | 16 - 0.04·(16-1) = 15.40 | 15.40 | 0.962500 | 3.7500 % | - |
| 64 | 64 - 0.04·(64-1) = 61.48 | 61.48 | 0.960625 | 3.9375 % | -0.001875 |
| 256 | 256 - 0.04·(256-1) = 245.80 | 245.80 | 0.960156 | 3.9844 % | -0.000469 |
| 1024 | 1024 - 0.04·(1024-1) = 983.08 | 983.08 | 0.960039 | 3.9961 % | -0.000117 |
| 4096 | 4096 - 0.04·(4096-1) = 3932.20 | 3932.20 | 0.960010 | 3.9990 % | -0.000029 |
| 16384 | 16384 - 0.04·(16384-1) = 15728.68 | 15728.68 | 0.960002 | 3.9998 % | -0.000007 |

## Evaluation

* Efficiency does **not** collapse as P grows exponentially. It falls from 0.9625 (P=16) and
  **saturates** at 1 − α = 0.96: E(P) = (1−α) + α/P, so the only P-dependent part is α/P → 0.
* From P = 1024 onward the change per ×4 in cores is below 4·10⁻⁵ — scaling is "free" in efficiency terms.
* Every extra core delivers (1 − α) = 0.96 of a core of useful work: S(P) ≈ 0.96·P + 0.04.
  At P = 16384 the speedup is 15728.68, i.e. 655.32 core-equivalents are lost to serial waiting — always exactly α(P−1).
* Caveat: this is the *idealised* model; Task 12 shows what happens when α itself grows with P.
