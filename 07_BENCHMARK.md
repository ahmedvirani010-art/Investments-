# Module 07 — Benchmark Performance Tracker

All portfolio returns measured relative to KSE-100 Total Return Index. Absolute returns are only meaningful in context of what the benchmark returned.

---

## Metrics Tracked

| Metric | Definition |
|--------|-----------|
| Monthly Return | Weighted portfolio return (price + dividend) vs. KSE-100 monthly return |
| YTD Return | Portfolio YTD (price + dividend reinvested) vs. KSE-100 YTD |
| Rolling Alpha (3-month) | Portfolio excess return over KSE-100 on rolling 3-month basis |
| Win/Loss Month Ratio | Months portfolio beat KSE-100 vs. missed |
| Active Share Contribution | Which positions contributed to vs. detracted from alpha |
| Beta to KSE-100 | Is the portfolio moving more or less than the market? |

---

## Alert Rule
If portfolio underperforms KSE-100 by >10% over 3 consecutive months → trigger **Process Audit** (Module 10).
The question is whether the analytical process is sound — not just which stocks to swap.

---

## Drive Path
`PSX_Research/Portfolio/benchmark.md`
Append monthly — one row per month, never overwrite historical data.
