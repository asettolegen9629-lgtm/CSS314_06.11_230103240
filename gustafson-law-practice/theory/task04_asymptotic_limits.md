# Task 04 — Asymptotic parallel efficiency

## 1. Gustafson
E_G(P) = S(P)/P = [P − α(P−1)]/P = 1 − α + α/P = 1 − α(P−1)/P.

**Limit:** lim_{P→∞} E_G(P) = lim [ (1−α) + α/P ] = **1 − α** (since α/P → 0). *Proof (ε–N):* |E_G − (1−α)| = α/P < ε for P > α/ε. ∎
* Monotonic: dE/dP = −α/P² < 0 for α > 0, so E decreases from E(1) = 1 toward the floor 1−α, never below it. Finite-P efficiency is above 1−α.
* Edge cases: α = 0 → E ≡ 1; α = 1 → E = 1/P → 0 (the only α for which efficiency vanishes).
* The *rate*: E_G(P) − (1−α) = α/P: O(1/P) convergence.

## 2. Amdahl (same domain, s = α)
E_A(P) = S_A/P = 1/[P(s + (1−s)/P)] = 1/[sP + (1−s)].

**Limit:** lim_{P→∞} E_A(P) = **0** for any s > 0, since the denominator sP + (1−s) → ∞. More precisely E_A(P) ~ 1/(sP) = Θ(1/P). *Proof:* E_A·sP = sP/(sP + 1 − s) → 1. ∎
Amdahl's *speedup* is therefore bounded by 1/s and its *efficiency* decays at the rate of the number of processors.

## 3. Contrast

| s = α | P | E_Gustafson | E_Amdahl |
|---|---|---|---|
| 0.05 | 100 | 0.95050 | 0.16807 |
| 0.05 | 1 000 | 0.95005 | 0.01963 |
| 0.05 | 100 000 | 0.95000 | 0.00020 |

(Computed from the closed forms above.)

## 4. Deductions
1. Under Gustafson there is an **efficiency floor** (1 − α); a machine can be grown without bound at constant efficiency *if* the problem grows with it.
2. Under Amdahl efficiency collapses like 1/(sP); to keep E_A = e you would need s ≤ (1/e − 1)/(P − 1) → serial fraction must *shrink* ∝ 1/P — the
   same statement as "problem size must grow", i.e. the isoefficiency view (Task 14).
3. The ratio E_G/E_A → ∞ linearly in P: E_G/E_A = [1−α + α/P]·[sP + 1 − s] ≈ (1−α)αP for large P.
