# Task 20 — Why Gustafson weak scaling is hard for graph analytics (BFS, PageRank)

## 1. What "weak scaling" even means for a graph
Dense GEMM/stencil: problem size N maps to work in a known way (N³) and every rank's work and data volume are equal and predictable. For graphs one must decide what is
held constant — vertices/rank, edges/rank, or frontier size — and the *structure* (degree distribution, diameter) changes with scale, so "same problem, bigger" is ill-defined.

## 2. Reasons efficiency collapses
1. **Irregular memory access / low arithmetic intensity.** Each edge touches a random neighbour: ~O(1) flop per cache miss, performance is limited by memory latency / bandwidth
   (and by the memory-parallelism a core can sustain), not by flops. Per-rank rate is not constant even in serial, as the graph outgrows caches.
2. **Power-law degree distribution ⇒ load imbalance.** A few hub vertices own a huge share of edges; vertex partitioning gives max-rank work ≫ mean. Time = max_i T_i, so
   S ≈ P·mean/max; the max of P heavy-tailed variables grows with P (hubs don't shrink when the graph is split).
3. **Frontier imbalance in BFS.** Levels start with 1 vertex, explode in the middle (a few levels hold most of the graph), then die out. In the thin levels ranks idle
   (α-like serial structure *per level*); with a small-world diameter D ≈ O(log N) there are few levels but each is a global synchronization.
4. **Data-dependent, fine-grained communication.** Neighbours of a vertex are spread across all ranks (cut size ∝ edges, no surface-to-volume benefit: random graphs
   have *no* good partition, edge cut ≈ (1−1/P) of all edges). Communication per rank is Θ(edges/rank), not O(surface) (contrast Task 17), i.e. comm/comp does not vanish.
   Messages are tiny and irregular → latency/injection-rate dominated; all-to-all traffic stresses bisection bandwidth (Task 13 case 2).
5. **Synchronization.** BFS: a global barrier + allreduce (is the frontier empty?) per level; PageRank: a global convergence check and a bulk-synchronous exchange per iteration. Per-level
   latency ∼ log P·t_lat adds a P-dependent C(P) (Task 12), independent of how large each rank's share is.
6. **Iteration/level counts are data-dependent.** PageRank iterations to tolerance and BFS depth depend on graph structure, not on the number of ranks, so the "fixed time per run" premise is uncontrolled.
7. **Memory capacity per node:** edges grow ∝ P at best, but replicated hub/ghost data and per-vertex frontier arrays make the footprint per rank grow with P (ghost vertices).
8. **Serial parts:** graph generation/loading/partitioning (often sequential or I/O bound, ∝ total edges) dominates; α(P) rises as graphs grow (Task 18 logic).

## 3. Why dense linear algebra is easier
Regular, predictable access (blocking, high arithmetic intensity: flops/byte ∝ N), perfectly balanced work, communication that is structured (broadcasts along rows/columns, volume ∝ N²/√P ≪ flops ∝ N³/P), static schedule → α small and nearly P-independent.

## 4. Practice and benchmarking
Graph500 reports **TEPS (traversed edges per second)** with graph scale (log₂ vertices) *increased with machine size* — a weak-scaling-style metric — and real results show per-node TEPS **decreasing** with node count (graph partition + all-to-all cost). Mitigations:
1D/2D edge partitioning, delegate/replicate high-degree vertices, direction-optimising (push/pull) BFS, message aggregation/coalescing, asynchronous (non-BSP) execution, vertex reordering for locality, communication-avoiding formulations (e.g. linear-algebra GraphBLAS style).

## 5. Verdict
Gustafson's law predicts near-linear S if *per-rank work and per-rank overhead are constant*. Graph analytics violates both: hubs make per-rank work non-constant, and communication volume/synchronisation per rank grows with P. The effective α(P) is large, P-dependent and data-dependent, so the measured curve usually falls well below S = P − α(P−1) with a fitted constant α.
