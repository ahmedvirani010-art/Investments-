# PSX Investment Agent — Skill Map
**Version:** 2.1 · **Updated:** March 2026

Reference for all 10 skills orchestrated by the PSX Investment Agent.
Never modify these skills — call them by name only.

---

## Skill Directory

| # | Skill Name | Primary Function | Key Outputs | Chains Into |
|---|-----------|-----------------|-------------|-------------|
| 1 | `psx-investing-plugin` | Drive persistence, session memory | Portfolio snapshot, saved files, session context | All skills (read before, write after) |
| 2 | `psx-portfolio-analysis` | 7-factor composite scoring, concentration, rebalancing | Score table, concentration alerts, rebalancing suggestions | `psx-tax-harvester` (if June), `psx-rs-trend` |
| 3 | `sector-analysis` | Sector/ticker deep dives, driver frameworks, valuation | Sector report, ticker thesis, driver scorecard | `psx-valuation-screen`, `psx-rs-trend` |
| 4 | `psx-earnings-analyzer` | Results normalization, EPS surprise, forward EPS, PREVIEW mode | Earnings brief, EPS delta, forward guidance | `psx-portfolio-analysis` (event rescore) |
| 5 | `psx-news-monitor` | News-to-ticker impact mapping, macro event routing | Impact summary, affected tickers, macro alert | `pakistan-macro-analyst`, `PMEX Commodities`, `psx-portfolio-analysis` |
| 6 | `psx-valuation-screen` | Cheapness check, yield spread, GGM, buy/hold/avoid signal | Valuation signal, yield spread, GGM output | `psx-rs-trend` |
| 7 | `psx-rs-trend` | Momentum, RS rank, Weinstein Stage, sector rotation | RS rank table, stage classification, rotation signal | `psx-portfolio-analysis` |
| 8 | `psx-tax-harvester` | CGT, loss harvest, VPS pension, year-end plan | Tax liability estimate, harvest list, VPS headroom | Standalone; feeds Decision Journal (M10) |
| 9 | `PMEX Commodities` | Gold, oil, cotton, palm oil — anchored to US/China macro | Commodity outlook, equity linkage | `sector-analysis` (E&P, fertilizer, textile) |
| 10 | `pakistan-macro-analyst` | Scenario forecasting, KPI early-warning dashboards, threshold backtesting | Flash brief / full research brief, scenario table, KPI dashboard, validation report | `psx-portfolio-analysis` (sector impact), `psx-news-monitor` (trigger source) |

---

## pakistan-macro-analyst — Extended Reference

This skill was added in v2.1. It is the primary entry point for all Pakistan macro, geopolitical, and scenario analysis requests.

### Trigger Phrases (route to this skill)
> "macro risks" · "scenario analysis" · "IMF risks" · "SBP outlook" · "PKR trajectory" · "energy security" · "political risk" · "tail risk" · "what happens if" · "PSX impact" · "war scenario" · "election risk" · "sovereign risk" · "KPI dashboard" · "which scenario is unfolding" · "monitor Pakistan macro" · "indicator thresholds" · "backtest the dashboard" · "validate thresholds" · "are we in the base case"

### 7-Step Framework

| Step | Name | Purpose |
|------|------|---------|
| 1 | Intake & Scope | Clarify trigger event, time horizon, output depth, decision context |
| 2 | Live Research | Web search for current macro indicators, geopolitical flashpoints, IMF status |
| 3 | Macro Event Map | Document current status, trajectory, Pakistan direct + indirect impacts |
| 4 | Scenario Framework | Build 3–5 distinct scenarios (Base / Optimistic / Pessimistic / Tail Risk) |
| 5 | Uncertainty Quantification | Confidence calibration, blind spots, tail risks outside main scenarios |
| 6 | KPI Indicator Dashboard | 20–30 indicators across 5 domains; threshold tracking; scenario probability update |
| 7 | Threshold Backtesting | Historical validation of dashboard thresholds against Pakistan 2015–2025 data |

### Output Formats

| Format | When | Length |
|--------|------|--------|
| Flash Brief | Default / quick check | 400–600 words |
| Full Research Brief | Explicit request / monthly review | 1,500–2,500 words |
| KPI Dashboard | Step 6 invocation | 20–30 indicators + summary table |
| React Dashboard | "build the dashboard" | Interactive artifact with live threshold logic |
| Validation Report | Step 7 invocation | Per-indicator calibration grades + deployment verdict |

### Portfolio Sector Linkages

When macro scenarios shift, flag these sectors first:

| Scenario Driver | Primary Sectors | Secondary Sectors |
|----------------|----------------|------------------|
| PKR depreciation | E&P (OGDC, PPL), Fertilizer (FFC, EFERT) | Banks (import LC exposure) |
| SBP rate cut | Banks (NIM expansion), Construction | Cement, Steel |
| IMF program at risk | Banks (sovereign exposure), Power | Across all |
| India-Pakistan escalation | Defense proxies, Gold | Cement, Consumer |
| Oil price spike | E&P upside, Fertilizer input cost up | Circular debt worsens |
| Flood / climate shock | Fertilizer (demand spike), Cement (rebuild) | Textile (cotton damage) |

### Alert Integration

| Alert | Condition | Action |
|-------|-----------|--------|
| MACRO MONITOR STALE | macro-context.md >14 days old | Run Steps 1–5 to refresh scenario framework; save to Drive |
| KPI THRESHOLD BREACH | Pessimistic or tail-risk threshold crossed | Run Step 6C dashboard; update scenario probabilities; flag affected sectors |
| MACRO SHIFT | SBP decision / PKR >2% / Brent >5% | psx-news-monitor → pakistan-macro-analyst (scenario delta only, not full brief) |

---

## Cross-Skill Chain Reference

```
Morning Briefing:
  psx-investing-plugin (pull) → check MACRO MONITOR STALE → check DRAWDOWN BREACH → check DIVIDEND EX-DATE

Macro Shock:
  psx-news-monitor → pakistan-macro-analyst (scenario update) → PMEX Commodities → psx-portfolio-analysis → psx-rs-trend

Pakistan Macro Analysis (full):
  pakistan-macro-analyst (Steps 1–7) → psx-portfolio-analysis (sector impact, if portfolio context)

Portfolio Review:
  psx-investing-plugin (pull) → psx-portfolio-analysis → psx-tax-harvester (if June)

Sector Deep Dive:
  sector-analysis → psx-valuation-screen → psx-rs-trend

Earnings Event:
  psx-earnings-analyzer → psx-portfolio-analysis (event rescore)

Commodity Check:
  PMEX Commodities → sector-analysis (equity linkage)
```
