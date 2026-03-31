# Benchmark Performance Tracker — Module 07

All portfolio returns measured relative to KSE-100 Total Return Index.
Absolute returns are only meaningful in context of what the benchmark returned.

---

## Triggers

Load this file when the user says:
- "run benchmark", "vs KSE-100", "benchmark check", "alpha vs index"

Also auto-runs at **Monthly Review Step 2** (`references/monthly-review.md`).

---

## Pre-Flight: Pull Drive Context

Before computing metrics, call `psx-investing-plugin` to pull:
- `PSX_Research/Portfolio/benchmark.md` — prior month rows for rolling calculations
- `PSX_Research/Portfolio/portfolio-master.md` — all OPEN holdings + weights

---

## 6 Metrics Tracked

| Metric | Definition |
|--------|-----------|
| Monthly Return | Weighted portfolio return (price + dividend) vs. KSE-100 monthly return |
| YTD Return | Portfolio YTD (price + dividend reinvested) vs. KSE-100 YTD |
| Rolling Alpha (3-month) | Portfolio excess return over KSE-100 on rolling 3-month basis |
| Win/Loss Month Ratio | Months portfolio beat KSE-100 vs. missed (running count since inception) |
| Active Share Contribution | Which positions contributed to vs. detracted from alpha this month |
| Beta to KSE-100 | Portfolio sensitivity to market moves — via `psx-portfolio-analysis` |

---

## Computation Steps

1. Fetch KSE-100 monthly return % via web search (KSE-100 Total Return Index or price return if TRI unavailable)
2. Compute weighted portfolio return:
   - For each OPEN position: position_return = (current price − prior month price) / prior month price
   - Add dividends received during the month to position return
   - Weighted portfolio return = sum(position_weight × position_return) across all holdings
3. Alpha (monthly) = portfolio return − KSE-100 return
4. Pull prior 2 months from `PSX_Research/Portfolio/benchmark.md` for:
   - Rolling Alpha (3M) = average monthly alpha over last 3 months
   - Win/Loss ratio = count of months portfolio beat vs. missed KSE-100
5. Active Share Contribution:
   - Sort positions by individual alpha contribution (position return vs. KSE-100 × weight)
   - Top 2 contributors and top 2 detractors
6. Call `psx-portfolio-analysis` for beta computation

---

## Alert Rule

If portfolio underperforms KSE-100 by >10% over 3 consecutive months:

> "⚠️ Portfolio has underperformed KSE-100 by >10% for 3 consecutive months. Process Audit (Module 10) recommended — the question is whether the analytical process is sound, not just which stocks to swap."

This is a process-level flag, not a portfolio rebalancing trigger.

---

## Display Format

```
## Benchmark Performance — [Month YYYY]

Monthly:  Portfolio [X]%  vs  KSE-100 [Y]%  |  Alpha: [Z]%
YTD:      Portfolio [X]%  vs  KSE-100 [Y]%
Rolling Alpha (3M): [X]%
Beta: [X.X]  |  Win/Loss: [W] months beat / [L] months missed

Top Alpha Contributors: [TICKER] +[X]%,  [TICKER] +[X]%
Top Alpha Detractors:   [TICKER] −[X]%,  [TICKER] −[X]%

[Any underperformance flag or Process Audit trigger]
```

---

## Drive Path

`PSX_Research/Portfolio/benchmark.md`
Append one row per month — **never overwrite historical data**.

Row format: `| [YYYY-MM] | [Portfolio %] | [KSE-100 %] | [Alpha %] | [Rolling 3M Alpha %] | [Beta] | [Beat/Miss] |`
