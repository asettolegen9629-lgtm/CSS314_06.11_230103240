# Task 19 — Monte Carlo: the ideal weak-scaling model and its residual α

Each rank draws k independent samples and averages. Work per rank is constant, no communication until the end ⇒ α is tiny — but non-zero.

## 1. Sources of serial fraction
| Source | Cost model | Behaviour |
|---|---|---|
| **PRNG seed management** | Serial seeding of P streams: O(P)·t_seed; with *skip-ahead / leapfrog / counter-based (Philox, Threefry) / SeedSequence.spawn* it is O(1) per rank and parallel | Naive "seed = rank" gives correlated streams (statistical, not just performance problem). Serial seeding is the first α(P) ∝ P term. |
| **Initial setup / input** | Reading model, broadcasting parameters: t_in + t_bcast·log P | constant + log P |
| **Reduction of results** | Tree: log₂P · (t_lat + m/BW); flat gather: P·t_msg | tree: log P; flat: P (serial at root) |
| **Output serialization** | Writing results/paths/histograms from one rank | constant, or ∝ P if each rank's output is gathered |
| **Load imbalance** | Variable-length paths (barrier options, rare events): max over ranks of T_i | grows ~ σ·√(2 ln P) |
| **Convergence/stopping test** | Global allreduce per batch | log P per batch |

## 2. Impact of the reduction tree on S(P)
Weak-scaled run: T_ideal = T (compute per rank). Fixed serial share α₀ (setup, output). Reduction adds t_red(P):

  S(P) = (α₀ + (1−α₀)P) / (1 + t_red(P)/T)

Illustration: T = 10 s, α₀ = 0.1 %, per-stage latency 20 µs (tree: t_red = 20 µs · log₂P), flat gather 2 µs per message (t_red = 2 µs · P), serial seeding 1 µs per stream.

| P | Gustafson, α₀ only | + tree reduction | + flat gather | + flat gather + serial seeding | E (flat+seed) |
|---|---|---|---|---|---|
| 64 | 63.94 | 63.94 | 63.94 | 63.94 | 0.999 |
| 1 024 | 1022.98 | 1022.96 | 1022.77 | 1022.66 | 0.999 |
| 65 536 | 65 470.5 | 65 468.4 | 64 623.4 | 64 208.1 | 0.980 |
| 1 048 576 | 1 047 528 | 1 047 485.5 | 865 929 | 796 858 | 0.760 |

(Tree values computed with 20 µs·log₂P/T = 1.2·10⁻⁵ … 4.0·10⁻⁵; flat gather 1.3·10⁻² at 65 536 and 0.21 at 10⁶; seeding 6.6·10⁻³ and 0.105. Base column = P − α₀(P−1).)

## 3. Takeaways
1. A **tree** reduction costs only O(log P) — a 10⁶-rank MC run loses < 0.01 % to it for sample sizes of seconds; the reduction is not the bottleneck.
2. **O(P) serial steps** (flat gather at root, serial seeding, per-rank output files merged by one rank) are what destroys MC scaling at ≥ 10⁵ ranks: −17 % (flat gather) and −24 % (flat gather + serial seeding) at 10⁶ ranks relative to the α₀-only column.
3. **PRNG design:** use counter-based generators with (seed, rank, stream) keys (no sequential seeding, reproducible regardless of P), or hierarchical `SeedSequence.spawn`. Check stream independence.
4. Bigger k (more samples per rank) makes every P-dependent term smaller *relative* to T — weak scaling favours large per-rank workloads.
5. MC variance falls as 1/√(Pk): weak scaling here buys accuracy ∝ √P rather than time.
