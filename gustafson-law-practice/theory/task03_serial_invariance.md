# Task 03 — The serial-fraction "invariance paradox": the frame of reference matters

## 1. Two different quantities with the same name
* Amdahl: **s₁ = t_serial / (t_serial + t_parallel,1)** measured on **one processor** for a *fixed* problem.
* Gustafson: **α = t_serial / (t_serial + t_parallel,P)** measured on **P processors**, where t_parallel,P is the *wall-clock* time of the parallel part.

The apparent contradiction: "if 1 % of my code is serial, speedup can never exceed 100" (Amdahl) vs "with 1 % serial I get ≈ 0.99P" (Gustafson).
They are not contradictory because the two "1 %" refer to different runs and different times.

## 2. Converting between frames (analytic)
**(a) Fixed-size problem, observed on P processors.** If the uniprocessor fraction is s₁, the parallel run takes s₁ + (1−s₁)/P (normalized), so

  α_P = s₁ / (s₁ + (1−s₁)/P)  →  1  as P → ∞.

The serial share *of the parallel runtime* of a fixed problem inexorably tends to 1: that is Amdahl's bottleneck, seen from the parallel machine.

**(b) Scaled problem: α fixed on the parallel machine.** Invert the relation: the **equivalent uniprocessor fraction** of the enlarged problem is

  s₁(P) = α / (α + (1−α)P)  →  0  as P → ∞.   (e.g. α = 0.04, P = 1024: s₁ = 0.04/(0.04 + 983.04) = 4.07·10⁻⁵)

So s₁ is **not invariant**: it is a function of problem size. Amdahl's s is a constant only because Amdahl keeps the size constant.

## 3. Proof that the two laws agree on the enlarged problem
Apply Amdahl's formula to the enlarged problem, using s₁(P) from (b):

 S_A = 1 / ( s₁ + (1−s₁)/P ),  with s₁ = α/D, 1 − s₁ = (1−α)P/D, D = α + (1−α)P

   = 1 / ( α/D + (1−α)/D ) = D / (α + 1 − α) = D = α + (1−α)P = P − α(P−1) = S_G.  ∎

**Gustafson's law is Amdahl's law evaluated on the P-times-larger problem**; the "serial fraction" of that bigger problem on one processor is tiny.

## 4. Why measuring α on the parallel machine removes the paradox
1. On a real machine the *fraction of wall-clock time the parallel machine is idle* is what you can observe cheaply (per-rank timers, profilers); the
   uniprocessor time of a problem that fits only because of P nodes' memory often cannot be measured at all (this was the case on the nCUBE, Task 05).
2. α measures **lost core-time**: loss = α(P−1) cores, linear in P but the *gain* is (1−α)P, also linear, so efficiency is bounded below by (1−α).
3. Serial overhead only "throttles" scaling when the problem is held fixed (shrinking parallel time); when problem size is increased, serial time stays
   constant while parallel work grows, so serial work becomes an ever smaller share of the *work*, even though it stays the same share of *time*.

## 5. Caveat (critical comment)
α is constant only if A3 holds (serial time independent of the scaled problem). If serial work grows with N (reading the mesh, global
reductions, sequential I/O) then α = α(P) rises (Task 12, 18) and the paradox returns in a milder form: a model of α(N(P)) is then required.
