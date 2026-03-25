# PSX Investment Agent — PRD Module Index
**Owner:** Noor Din · **Version:** 2.0 · **March 2026**

Load only the module(s) relevant to your current build task.
All 9 existing PSX skills are used as-is — never modified.

---

## Modules

| File | Feature | Load When... |
|------|---------|--------------|
| `01_LIFECYCLE.md` | Portfolio Management Lifecycle | Building position open/hold/close workflow |
| `02_MONTHLY_REVIEW.md` | Monthly Review Engine | Building the EOM review sequence |
| `03_WATCHLIST.md` | Watchlist Management | Building watchlist entry/promotion logic |
| `04_THESIS_TRACKER.md` | Investment Thesis Tracker | Building thesis status tracking |
| `05_DIVIDEND_CALENDAR.md` | Dividend Calendar | Building ex-date tracking and alerts |
| `06_DRAWDOWN.md` | Drawdown Control System | Building position/portfolio-level alerts |
| `07_BENCHMARK.md` | Benchmark Performance Tracker | Building KSE-100 relative tracking |
| `08_CAPITAL_QUEUE.md` | Capital Deployment Queue | Building cash staging logic |
| `09_EARNINGS_CALENDAR.md` | Earnings Season Calendar | Building proactive preview triggering |
| `10_DECISION_JOURNAL.md` | Decision Journal | Building trade reasoning log |
| `11_ROUTING_AND_ALERTS.md` | Session Routing + Alert System | Building the Agent's routing table |
| `12_DRIVE_SCHEMA.md` | Google Drive Schema | Setting up all Drive file/folder templates |
| `13_ASSET_ALLOCATION.md` | Asset Allocation & Total Wealth View | Building holistic net worth view across PSX equities, provident fund, gratuity, endowment policies, VPS pension, cash, gold, real estate |

---

## Shared Context (applies to every module)

**Existing skills — orchestrate only, never modify:**
`psx-investing-plugin` · `psx-portfolio-analysis` · `sector-analysis` · `psx-earnings-analyzer` · `psx-news-monitor` · `psx-valuation-screen` · `psx-rs-trend` · `psx-tax-harvester` · `PMEX Commodities`

**Hard rules across all modules:**
- No automated trade execution — human confirmation required
- Tax rates always fetched live — never hardcoded
- Drive files are the source of truth — always pull before generating, save after
- BROKEN thesis = mandatory exit decision, no exceptions
- 5% cash floor is non-negotiable without explicit user override
