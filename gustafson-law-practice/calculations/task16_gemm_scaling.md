# Task 16 — GEMM weak scaling

## Derivation
Work of C = A·B (N×N): W(N) = 2N³ flops (Θ(N³)). Gustafson fixes parallel runtime T. With P processors at rate r each and ideal
distribution: T = W/(P·r) ⇒ for T constant, **W(P) = P·W(1)** ⇒ 2N³ = P·2N₁³ ⇒

**N(P) = N₁ · P^(1/3)**   (not P, and not √P).

Memory: total = 3·8·N² B ∝ P^(2/3); per processor ∝ P^(−1/3) — it *shrinks*, so memory is never the binding limit
under fixed-time scaling (it would be under a memory-bounded model: N ∝ P^(1/2), work ∝ P^(3/2), see Task 11).

## Scaling targets (N₁ = 2048, r = 100 GFLOP/s per processor — assumptions)

| P | N(P) | total flops 2N³ | time/proc (s) | matrix mem per proc (MiB) | 2D-SUMMA comm per proc (MiB) |
|---|---|---|---|---|---|
| 1 | 2,048 | 1.718e+10 | 0.172 | 96.0 | 32.0 |
| 8 | 4,096 | 1.374e+11 | 0.172 | 48.0 | 45.3 |
| 64 | 8,192 | 1.100e+12 | 0.172 | 24.0 | 64.0 |
| 512 | 16,384 | 8.796e+12 | 0.172 | 12.0 | 90.5 |
| 4096 | 32,768 | 7.037e+13 | 0.172 | 6.0 | 128.0 |
| 32768 | 65,536 | 5.629e+14 | 0.172 | 3.0 | 181.0 |

(Perfect cubes of P are chosen so N is an integer multiple of N₁.)

## Observations
* Per-processor time is constant (0.172 s) by construction — Gustafson's premise.
* Communication volume per processor of 2D algorithms (SUMMA/Cannon) is ∝ N²/√P ∝ P^(2/3−1/2) = P^(1/6): it **grows slowly**,
  so the constant-time premise needs overlap of comm and compute or a 3D/2.5D algorithm (comm ∝ N²/P^(2/3) = const).
  This is the mechanism by which α creeps up in real GEMM runs.
* Arithmetic intensity grows with N (flops/byte ∝ N), a reason why GEMM is the "best case" for weak scaling.
