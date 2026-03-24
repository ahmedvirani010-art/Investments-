# Routing Logic — Master Session Table

All 17 session types the PSX Investment Agent handles.
This file is the canonical routing reference — cross-indexed to modules, skills, and reference files.

---

## Full Routing Table

| Session Type | Trigger Phrases | Modules / Skills Activated | Reference Files |
|-------------|----------------|---------------------------|----------------|
| Morning Briefing | "morning", "start session", "morning check", "morning briefing" | Drawdown scan (M06) + Dividend ex-date check (M05) + Capital queue check (M08) + Earnings 30-day check (M09) + Stale research flags (Step 0) | `drawdown.md`, `dividend-calendar.md`, `capital-queue.md`, `earnings-calendar.md` |
| Position Open | "I bought X", "entering X at PKR Y", "took a position", "open a position", "added X" | M01 OPEN + M04 thesis capture + M10 journal entry (BUY) + cash floor check | `thesis-tracker.md`, `decision-journal.md`, `drawdown.md` |
| Position Close | "I sold X", "exiting X", "closing X", "out of X", "sold my X" | M01 CLOSED + `psx-tax-harvester` + M10 outcome log + capital queue update | `decision-journal.md`, `capital-queue.md` |
| Hold / Monitor | "check X", "thesis update on X", "rescore X", "position review", "how is X doing", "news on X" | M01 HOLD (event type determines path) + thesis check + drawdown check | `thesis-tracker.md`, `drawdown.md`, `earnings-calendar.md` |
| Watchlist Add | "add X to watchlist", "researched X — not buying yet", "watching X", "looking at X" | M03 entry + M04 thesis v1 + M10 watchlist log | `watchlist.md`, `thesis-tracker.md`, `decision-journal.md` |
| Watchlist Management | "show watchlist", "review watchlist", "clean up watchlist", "watchlist status" | M03 review logic — display entries, check expiry, promote or remove | `watchlist.md` |
| Thesis Review | "is my thesis intact for X?", "check thesis X", "thesis update", "thesis integrity" | M04 + `sector-analysis` if rescore needed | `thesis-tracker.md` |
| Monthly Review | "monthly review", "EOM", "end of month", "EOM review", "monthly check" | M02 — all 7 steps in sequence | `monthly-review.md` |
| Drawdown Alert | "drawdown alert", "position down X%", "drawdown check", "stop check" | M06 — per-position L1/L2/L3 + portfolio-level | `drawdown.md` |
| Dividend Check | "what dividends coming?", "ex-date for X?", "dividend check", "upcoming dividends", "dividend calendar" | M05 + `psx-tax-harvester` (WHT) | `dividend-calendar.md` |
| Earnings Preview | "results due for X", "earnings preview", "results season", "earnings calendar", "Q results" | M09 — proactive PREVIEW trigger + save to Drive | `earnings-calendar.md` |
| Earnings Event (reactive) | "results out for X", "X just reported", "earnings out" | `psx-earnings-analyzer` (ANALYZER mode) → `psx-portfolio-analysis` (event rescore) → save outcome + accuracy grade | `earnings-calendar.md` |
| Deploy Capital | "I have PKR X to deploy", "what should I buy?", "capital to deploy", "cash queue", "deploy cash" | M08 — queue check + watchlist promotion + cash floor enforcement | `capital-queue.md`, `watchlist.md` |
| Benchmark | "run benchmark", "vs KSE-100", "benchmark check", "alpha vs index" | M07 — 6 metrics vs KSE-100 + Process Audit trigger if BENCHMARK LAG | `benchmark.md` |
| Decision Log | "log this trade", "record my decision", "decision journal", "log a trade", "log my decision" | M10 — structured 10-field journal entry with counter-argument gate | `decision-journal.md` |
| Quarterly Audit | "Q1 audit", "Q2 audit", "process review", "quarterly audit", "quarterly review" | M10 quarterly audit (5 checks → 300–400 word memo) + M07 benchmark summary | `decision-journal.md`, `benchmark.md` |
| Sector Research | "analyze X sector", "sector deep dive", "research X sector" | `sector-analysis` → `psx-valuation-screen` → `psx-rs-trend` | — |
| Portfolio Review | "review my portfolio", "rescore all", "rescore", "what's in my portfolio" | `psx-investing-plugin` (pull all) → `psx-portfolio-analysis` → `psx-tax-harvester` (if within 60 days of June 30) | — |
| Commodity Check | "gold outlook", "cotton impact", "oil price", "palm oil", "PMEX" | `PMEX Commodities` → `sector-analysis` (equity linkage to PSX tickers) | — |
| Macro Shock | "SBP cuts", "SBP hikes", "PKR crash", "Hormuz escalation", "macro event" | `psx-news-monitor` → `PMEX Commodities` → `psx-portfolio-analysis` (scenario rescore) → `psx-rs-trend` | — |

---

## Routing Disambiguation Rules

1. "Check X" without context → default to HOLD/Monitor
2. "Research X" without "bought" or "buying" → default to Watchlist Add
3. "Rescore" without a specific ticker → Portfolio Review (all positions)
4. "Morning" or "start session" → always Morning Briefing regardless of other content
5. If ambiguous between Watchlist Add and Position Open → ask: "Are you adding [TICKER] to the watchlist, or have you already bought it?"
6. Quarterly Audit always also runs Benchmark summary — they are paired

---

## Skill Load Order (where multiple skills activate)

For sessions activating multiple skills, always call in this order:
1. `psx-investing-plugin` — pull Drive context first
2. Analysis skills — `psx-news-monitor`, `sector-analysis`, `PMEX Commodities`
3. Scoring skills — `psx-portfolio-analysis`, `psx-valuation-screen`, `psx-rs-trend`
4. Event skills — `psx-earnings-analyzer`
5. Tax/compliance — `psx-tax-harvester`
6. Persistence — `psx-investing-plugin` save (always last)
