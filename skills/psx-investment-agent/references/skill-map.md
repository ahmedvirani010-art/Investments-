# Skill Map — PSX Investment Agent

Maps each lifecycle stage and action to the correct existing sub-skill.
All sub-skills are used as-is. Never modify their logic.

---

## Lifecycle Stage → Sub-skill Routing

| Stage | Action | Sub-skill | Notes |
|-------|--------|-----------|-------|
| WATCHLIST | Sector / stock deep dive | `sector-analysis` | Pass ticker + sector + prior Drive context |
| WATCHLIST | Cheapness check + BUY/HOLD/AVOID signal | `psx-valuation-screen` | Pass ticker + sector context |
| WATCHLIST | Momentum, RS rank, Weinstein Stage | `psx-rs-trend` | Used for entry timing read |
| OPEN | 7-factor composite score at entry | `psx-portfolio-analysis` | Pass all holdings + weights + macro context |
| OPEN | CGT cohort assignment | `psx-tax-harvester` | Pass entry date, price, quantity |
| HOLD (event) | News-to-ticker impact mapping | `psx-news-monitor` | Pass news headline/event; maps to portfolio tickers |
| HOLD (event) | Rescore after news / earnings | `psx-portfolio-analysis` | EVENT RESCORE mode |
| HOLD (earnings) | Results normalization, EPS surprise, forward EPS | `psx-earnings-analyzer` | Also handles PREVIEW mode pre-earnings |
| HOLD (commodity) | Gold, oil, cotton, palm oil macro read | `PMEX Commodities` | Anchor to US/China macro context |
| CLOSED | CGT calculation, loss harvesting | `psx-tax-harvester` | Pass entry/exit dates, prices, quantity, cohort |
| ALL | Drive read / write (portfolio-master, ticker files, logs) | `psx-investing-plugin` | Always the persistence layer |
| ALL | Decision Journal entry | Module 10 (`10_DECISION_JOURNAL.md`) | Log every entry, exit, override decision |

---

## Sub-skill Primary Functions (reference)

| Sub-skill | Primary Function | When NOT to Use |
|-----------|-----------------|-----------------|
| `psx-investing-plugin` | Drive persistence, session memory, cross-session context | Never skip — always route Drive I/O through this |
| `psx-portfolio-analysis` | 7-factor composite scoring, concentration, rebalancing signals | Not for individual stock deep dives |
| `sector-analysis` | Sector/ticker deep dives, driver frameworks, valuation narratives | Not for portfolio-level scoring |
| `psx-earnings-analyzer` | Results normalization, EPS surprise, forward EPS, PREVIEW mode | Not for ongoing thesis checks between earnings |
| `psx-news-monitor` | News-to-ticker impact mapping, macro event routing | Not for deep valuation work |
| `psx-valuation-screen` | Cheapness check, yield spread, GGM, buy/hold/avoid signal | Not for momentum / timing analysis |
| `psx-rs-trend` | Momentum, RS rank, Weinstein Stage, sector rotation | Not for fundamental valuation |
| `psx-tax-harvester` | CGT, loss harvest, VPS pension, year-end plan | Not for portfolio scoring or thesis work |
| `PMEX Commodities` | Gold, oil, cotton, palm oil anchored to US/China macro | Only for commodity-linked tickers or macro context |

---

## Session Type → Module Routing

When the Agent detects a session type beyond lifecycle, route to the appropriate PRD module:

| Session Type | Trigger Phrases | Module |
|-------------|----------------|--------|
| Monthly Review | "monthly review", "end of month", "EOM review" | `02_MONTHLY_REVIEW.md` |
| Watchlist Management | "show watchlist", "review watchlist", "clean up watchlist" | `03_WATCHLIST.md` |
| Thesis Check | "thesis update", "thesis integrity", "check thesis" | `04_THESIS_TRACKER.md` |
| Dividend Tracking | "dividend check", "ex-date", "upcoming dividends" | `05_DIVIDEND_CALENDAR.md` |
| Drawdown Alert | "drawdown", "position down X%", "stop check" | `06_DRAWDOWN.md` |
| Benchmark | "vs KSE-100", "benchmark check", "alpha vs index" | `07_BENCHMARK.md` |
| Capital Deployment | "capital to deploy", "cash queue", "what to buy next" | `08_CAPITAL_QUEUE.md` |
| Earnings Calendar | "earnings preview", "results season", "who reports next" | `09_EARNINGS_CALENDAR.md` |
| Decision Journal | "log decision", "decision journal", "why did I buy/sell" | `10_DECISION_JOURNAL.md` |
| Routing / Alerts | Agent setup, alert threshold config | `11_ROUTING_AND_ALERTS.md` |
| Drive Setup | Drive schema, folder structure, templates | `12_DRIVE_SCHEMA.md` |
