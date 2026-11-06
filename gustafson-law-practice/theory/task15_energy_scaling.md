# Task 15 — Energy under Gustafson scaling

## 1. Power model
Each of P nodes draws **P_idle** whenever it is powered/allocated (static) and an extra **P_active** while it computes (so total P_idle + P_active). Normalize the
wall-clock of the scaled run to T (= T·(s+p), s+p = 1).

* Time busy: serial phase sT (1 node active), parallel phase pT (all P nodes active).
* Active (dynamic) energy:  E_dyn = P_active·(sT + P·pT) = P_active·T·(s + pP) = P_active·T·S(P)
* Static energy (all P allocated for T): E_stat = P·P_idle·T

  **E_P = T·[ P·P_idle + P_active·(s + pP) ] = T·[ P·P_idle + P_active·S(P) ]**.

## 2. One core running the *same* (scaled) job
It needs T₁ = (s + pP)·T = S·T (Task 02). Energy E₁ = T₁·(P_idle + P_active) = S·T·(P_idle + P_active).

## 3. Comparison
E_P / E₁ = [P·P_idle + S·P_active] / [S·(P_idle + P_active)] = 1 + φ·(P/S − 1), φ = P_idle/(P_idle+P_active).

Since P/S = 1/E(P): **E_P/E₁ = 1 + φ·(1/E − 1)** and the excess energy is **ΔE = P_idle·T·(P − S) = P_idle·T·α(P−1)**: exactly the idle power burned by the P−1 cores
waiting during the serial phase. Dynamic energy is **identical** (same total work).

Example: α = 0.04, E → 0.96 ⇒ 1/E − 1 = 0.0417; φ = 0.4 (idle = 2/3 of active) ⇒ E_P/E₁ = 1.0167 (+1.7 %).

## 4. Identical wall-clock runtime (T) — what the question really compares
* 1 core in T: does 1 unit of work, energy T(P_idle + P_active).
* P cores in T: do S(P) units of work, energy E_P above.
* Energy per unit of work: e₁ = (P_idle+P_active)·T; e_P = E_P/S = T[P·P_idle/S + P_active] = T[P_idle/E + P_active].
  Ratio e_P/e₁ = (P_idle/E + P_active)/(P_idle+P_active) — i.e. the same formula; for E = 0.96, φ = 0.4: **1.017**.
* If P_idle ≫ P_active (static-dominated nodes, old hardware): e_P/e₁ → 1/E: energy efficiency = parallel efficiency. Under weak scaling E ≥ 1−α, so the
  energy penalty is ≤ α/(1−α) (4.2 % for α = 0.04).
* If P_idle ≪ P_active (strong power-proportionality, race-to-idle hardware): ratio → 1 regardless of α.

## 5. Contrast with fixed-size (Amdahl) energy
E = 1/(sP + 1 − s) ⇒ ΔE ∝ P·P_idle·T(1 − E) grows without bound (idle nodes). Weak scaling is the energy-friendly regime: waste α(P−1)·P_idle·T is
a *constant fraction* of total energy, not a growing one. Mitigations: power-gating idle nodes in serial phases, DVFS on waiting ranks, hiding serial I/O.
