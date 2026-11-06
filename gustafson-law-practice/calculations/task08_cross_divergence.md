# Task 08 — Amdahl vs Gustafson divergence (s = α = 0.08, P = 128)

## Step 1 — Amdahl (fixed size)
S_A = 1 / (s + (1−s)/P) = 1 / (0.08 + 0.92/128) = 1 / (0.08 + 0.0071875) = 1 / 0.0871875 = **11.4695**

## Step 2 — Gustafson (scaled)
S_G = P − α(P−1) = 128 − 0.08·127 = 128 − 10.16 = **117.84**

## Step 3 — Discrepancy
* Absolute difference: 117.8400 − 11.4695 = 106.3705
* Ratio S_G / S_A = **10.274×**
* Gustafson relative to Amdahl: (S_G − S_A)/S_A = **927.4 %** higher
* Amdahl relative to Gustafson: (S_G − S_A)/S_G = **90.3 %** lower (Amdahl under-predicts by this much)

## Divergence with P (same s = α = 0.08)

| P | Amdahl | Gustafson | Ratio | Amdahl shortfall |
|---|---|---|---|---|
| 2 | 1.852 | 1.920 | 1.04× | 3.55 % |
| 8 | 5.128 | 7.440 | 1.45× | 31.07 % |
| 32 | 9.195 | 29.520 | 3.21× | 68.85 % |
| 128 | 11.470 | 117.840 | 10.27× | 90.27 % |
| 512 | 12.225 | 471.120 | 38.54× | 97.41 % |
| 2048 | 12.430 | 1884.240 | 151.59× | 99.34 % |
| 16384 | 12.491 | 15073.360 | 1206.72× | 99.92 % |

## Why they diverge
* Amdahl is **bounded**: S_A → 1/s = 12.5 as P → ∞. Adding cores beyond ~10/s buys nothing.
* Gustafson is **unbounded and linear**: S_G = (1−α)P + α, slope 0.92.
* The two answer different questions with the *same number* 0.08:
  Amdahl's s is the fraction of the **1-core** time of a **fixed** problem; Gustafson's α is a fraction of the
  **P-core** time of a problem that was **enlarged** until runtime stayed constant. In the scaled problem the serial
  part is a vanishing share of the *equivalent serial* work, (s + pP), so it matters less and less.
* The ratio therefore grows ~linearly in P (≈ 0.92P·0.08 = 0.0736P for large P).
