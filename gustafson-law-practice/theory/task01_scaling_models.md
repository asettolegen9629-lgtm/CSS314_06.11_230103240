# Task 01 — Amdahl (1967) vs Gustafson (1988): strong vs weak scaling

## 1. Side-by-side

| | Amdahl (1967) | Gustafson–Barsis (1988) |
|---|---|---|
| Question asked | "How much faster can I solve *this* problem?" | "How much *more* problem can I solve in the same time?" |
| Held constant | Problem size W (total work) | Wall-clock time T (parallel runtime) |
| Varies with P | Time per processor shrinks: T(P) = T₁(s + (1−s)/P) | Problem size grows: W(P) = s + pP |
| Serial fraction measured | s on **1 processor**, of the fixed problem | α on **P processors**, of the scaled run |
| Formula | S = 1/(s + (1−s)/P) | S = P − α(P−1) = s + pP |
| Limit P → ∞ | S → 1/s (hard ceiling) | S ~ (1−α)P (unbounded, linear) |
| Scaling type | Strong scaling | Weak scaling |

## 2. Behaviour of the problem dimension as P → ∞
* **Amdahl:** the problem dimension is **fixed**, N = N₀ for every P. Work per processor ∝ 1/P → 0, so the serial section (constant) eventually
  *is* the runtime: the parallel fraction of the P-processor run tends to 0.
* **Gustafson:** the dimension **grows with P** so that per-processor work is constant. For an algorithm with complexity Θ(N^d) in the
  *parallel* section: N(P) = N₀ · P^(1/d) (e.g. 3D stencil with Θ(N³) work: N ∝ P^(1/3); dense GEMM with Θ(N³): N ∝ P^(1/3); N-body direct Θ(N²): N ∝ P^(1/2)).
  The parallel work per processor stays constant, the serial work is (assumed) constant too ⇒ their ratio α is constant.

## 3. Why "fixed-size" vs "fixed-time"
* **Fixed-size:** Amdahl's model compares *time to solution of one fixed instance* as resources are added. The only free variable is time.
* **Fixed-time:** Gustafson's model pins the *wall-clock budget* (an hour, an overnight run, a 10 ms frame) and lets the *amount of work*
  float: the user spends extra processors on resolution, accuracy, particle count, ensemble size. The free variable is problem size.
  Normalizing T = s + p = 1 gives the "scaled speedup" (work done)/(time) relative to one processor.

## 4. Philosophical / physical divergence
1. **Where the serial part lives.** Amdahl treats the serial part as a property of the *program*; Gustafson treats it as a property of the *run*
   (setup, I/O, sequential control), which in practice grows far slower than the parallel kernel (resolution, particles).
2. **User behaviour.** Amdahl implicitly assumes users want the same answer faster. Practitioners in science and engineering usually want a *better* answer in
   the same time — finer meshes, more samples (this is the empirical basis of Gustafson's argument).
3. **Optimism vs pessimism.** Amdahl: massive parallelism is only for programs with s ≈ 0. Gustafson: massive parallelism is for programs whose *problem size can grow*.
4. **Both are correct** under their own assumptions; they are the same speedup definition (T_serial/T_parallel) evaluated on different workloads
   (see Task 03: Gustafson = Amdahl applied to the *enlarged* problem).
5. **Where each is the right tool:** Amdahl for latency-bound problems (real-time control, fixed-size queries, a given game frame), Gustafson for
   throughput/capacity-bound scientific simulation, Monte Carlo, ML training with weak-scaled batch size.
