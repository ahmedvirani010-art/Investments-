# Skill Map — PSX Investment Agent
**Version:** 2.1 · **Updated:** 2026-03-28

Maps each session type to its full skill chain. `crawl4ai` rows are marked **[C4AI]**
to indicate optional upstream web-fetch steps.

---

## Full Skill Chain by Session Type

| Session Type | Step 1 | Step 2 | Step 3 | Step 4 | Notes |
|-------------|--------|--------|--------|--------|-------|
| Morning Briefing | `psx-investing-plugin` (pull) | Drawdown check (M06) | Dividend alerts (M05) | Queue check (M08) | **[C4AI]** optional: fetch PSX index page if MCP unavailable |
| Monthly Review | `psx-investing-plugin` (pull) | `psx-portfolio-analysis` | `psx-tax-harvester` (if June) | `psx-investing-plugin` (save) | 7-step sequence per M02 |
| Position Open | `sector-analysis` (thesis) | `psx-valuation-screen` | `psx-rs-trend` | `psx-investing-plugin` (save) + M10 journal | |
| Position Close | `psx-tax-harvester` (CGT calc) | `psx-portfolio-analysis` (rebalance) | `psx-investing-plugin` (save) | M10 outcome entry | |
| Watchlist Add | `psx-valuation-screen` | `psx-rs-trend` | `sector-analysis` (driver summary) | `psx-investing-plugin` (save) | **[C4AI]** optional: crawl company IR page for thesis input |
| Thesis Review | `psx-investing-plugin` (pull thesis) | `sector-analysis` (rescore if >30d) | BROKEN flag if triggered | `psx-investing-plugin` (save) | **[C4AI]** optional: crawl SECP filings for updated data |
| Dividend Check | `psx-investing-plugin` (pull calendar) | `psx-tax-harvester` (WHT calc) | — | — | |
| Drawdown Alert | `psx-investing-plugin` (pull position) | `sector-analysis` (thesis review) | `psx-portfolio-analysis` (rescore) | `psx-investing-plugin` (save) | L3 breach = mandatory exit flag |
| Deploy Capital | `psx-investing-plugin` (pull queue) | Queue rank check (M08) | 5% floor check | Watchlist promotion if applicable | |
| Earnings Preview | `psx-earnings-analyzer` (PREVIEW mode) | `psx-investing-plugin` (save preview) | — | — | **[C4AI]** optional: crawl PSX notice board for result date confirmation |
| Decision Log | `psx-investing-plugin` (pull context) | M10 journal entry | `psx-investing-plugin` (save) | — | |
| Quarterly Audit | `psx-portfolio-analysis` | M07 benchmark vs KSE-100 | M10 quarterly audit | `psx-investing-plugin` (save) | |
| Sector Research | `sector-analysis` | `psx-valuation-screen` | `psx-rs-trend` | `psx-investing-plugin` (save) | **[C4AI]** optional: crawl annual report / investor presentation |
| Earnings Event | `psx-earnings-analyzer` (normalize results) | `psx-portfolio-analysis` (event rescore) | `psx-investing-plugin` (save) | M10 outcome if position affected | |
| Portfolio Review | `psx-investing-plugin` (pull) | `psx-portfolio-analysis` | `psx-tax-harvester` (if June) | `psx-investing-plugin` (save) | |
| Commodity Check | `PMEX Commodities` | `sector-analysis` (equity linkage) | — | — | |
| Macro Shock | `psx-news-monitor` | `PMEX Commodities` | `psx-portfolio-analysis` (scenario rescore) | `psx-rs-trend` | **[C4AI]** optional: crawl Dawn/Business Recorder for full article text |
| Web Research | `crawl4ai` (extract) | Downstream skill (see table below) | `psx-investing-plugin` (save if material) | — | Primary crawl4ai session type |

---

## crawl4ai Downstream Routing

| URL / Source Type | Downstream Skill |
|------------------|-----------------|
| PSX notice board | `psx-earnings-analyzer` |
| Company annual report / IR page | `sector-analysis` |
| SECP filing | `sector-analysis` or `psx-valuation-screen` |
| Dawn / Business Recorder article | `psx-news-monitor` |
| PMEX / commodity price page | `PMEX Commodities` |
| FBR tax circular | `psx-tax-harvester` |
| PSX index / market data | `psx-portfolio-analysis` |
| Generic research URL | User-directed — present markdown, ask which skill to feed |

---

## crawl4ai vs MCP Tool Decision Rule

```
IF web search MCP or S&P Global MCP can satisfy the request
  → Use MCP tool (faster, integrated)
ELSE IF user provides a specific URL or requests raw page extraction
  → Use crawl4ai
ELSE IF MCP returns no result or partial result
  → Fall back to crawl4ai with fit-markdown extraction
```

---

## Skill Dependency Notes

- `psx-investing-plugin` is called at the **start** (pull) and **end** (save) of
  almost every session — it is the session memory layer.
- `psx-tax-harvester` is mandatory on Position Close and in Portfolio Review
  sessions during June (tax year end).
- `crawl4ai` is **never** the final step — its output always feeds a downstream
  analytical skill before being presented to the user.
- `psx-portfolio-analysis` rescores are triggered by: Earnings Event, Drawdown
  Alert, Macro Shock, Monthly Review, Quarterly Audit.
