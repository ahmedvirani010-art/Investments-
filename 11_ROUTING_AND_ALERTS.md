# Module 11 — Session Routing & Alert System

---

## Session Routing Table

| Session Type | Trigger Examples | Modules / Skills Activated |
|-------------|-----------------|---------------------------|
| Morning Briefing | "morning", "start session" | v1.0 workflow + Drawdown alerts (M06) + Dividend ex-date alerts (M05) + Queue check (M08) |
| Monthly Review | "monthly review", "EOM", "end of month" | Module 02 — all 7 steps |
| Position Open | "I bought X", "entering X at PKR Y" | Module 01 OPEN + Module 04 thesis capture + Module 10 journal |
| Position Close | "I sold X", "exiting X" | Module 01 CLOSED + psx-tax-harvester + Module 10 outcome |
| Watchlist Add | "add X to watchlist", "researched X — not buying yet" | Module 03 — structured entry with entry conditions |
| Thesis Review | "is my thesis intact for X?", "check thesis X" | Module 04 + sector-analysis if rescore needed |
| Dividend Check | "what dividends coming?", "ex-date for FFC?" | Module 05 + psx-tax-harvester (WHT) |
| Drawdown Alert | Price falls below threshold (auto-detected at session start) | Module 06 — mandatory thesis review + rescore |
| Deploy Capital | "I have PKR X to deploy", "what should I buy?" | Module 08 — Queue check + watchlist promotion |
| Earnings Preview | "results due for X next month" | Module 09 — proactive preview + save to Drive |
| Decision Log | "log this trade", "record my decision" | Module 10 — structured journal entry |
| Quarterly Audit | "Q1 audit", "process review" | Module 10 quarterly audit + Module 07 benchmark |
| Sector Research | "analyze X sector" | sector-analysis → psx-valuation-screen → psx-rs-trend |
| Earnings Event | "results out for X" | psx-earnings-analyzer → psx-portfolio-analysis (event rescore) |
| Portfolio Review | "review my portfolio", "rescore" | psx-investing-plugin (pull) → psx-portfolio-analysis → psx-tax-harvester (if June) |
| Commodity Check | "gold outlook", "cotton impact" | PMEX Commodities → sector-analysis (equity linkage) |
| Macro Shock | "SBP cuts", "Hormuz escalation" | psx-news-monitor → PMEX Commodities → psx-portfolio-analysis (scenario rescore) → psx-rs-trend |
| Web Research | "scrape X", "fetch data from Y", "crawl SECP filings", "extract from PSX site", "get data from [URL]" | crawl4ai → feed result to relevant downstream skill (sector-analysis / psx-earnings-analyzer / psx-news-monitor) |

---

## Alert System

| Alert | Version | Condition | Response |
|-------|---------|-----------|----------|
| STALE RESEARCH | v1.0 | Thesis >30d / macro context >14d / scores >7d | Auto-flag at session start |
| CONCENTRATION | v1.0 | Sector >40% or single name >20% | Auto-flag in morning briefing |
| EARNINGS WINDOW | v1.0 | Held ticker approaching results | Trigger PREVIEW mode (30 days before) |
| MACRO SHIFT | v1.0 | SBP decision / PKR move >2% / Brent move >5% | psx-news-monitor + rescore |
| TAX HARVEST | v1.0 | Within 60 days of June 30 | Auto-flag harvest opportunities |
| DRAWDOWN BREACH | v2.0 | Position breaches L1/L2/L3 threshold | Mandatory thesis review. L3 = exit flag. |
| THESIS BROKEN | v2.0 | Monthly review finds BROKEN status | Mandatory exit decision before session ends |
| DIVIDEND EX-DATE | v2.0 | Ex-date within 15 trading days | Flag in morning briefing with net yield after WHT |
| WATCHLIST EXPIRY | v2.0 | Max wait period reached without entry | Prompt: reassess or remove |
| BENCHMARK LAG | v2.0 | Portfolio underperforms KSE-100 by >10% over 3 months | Trigger Process Audit (Module 10) |
