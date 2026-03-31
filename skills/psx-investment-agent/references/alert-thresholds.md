# Alert Thresholds — Module 11

All 10 system alerts with version, trigger condition, flag message, and required response.
This is the canonical reference — checked by Step 0 and individual module files.

---

## Alert Table

| Alert | Ver | Trigger Condition | Where Checked | Flag Message | Required Response |
|-------|-----|-------------------|--------------|--------------|------------------|
| STALE RESEARCH | v1.0 | Ticker thesis >30 days old | Step 0 — every session | `⚠️ STALE: [TICKER] thesis is [N] days old` | Offer to refresh before proceeding |
| STALE SCORES | v1.0 | Composite scores >7 days old | Step 0 — every session | `⚠️ STALE: portfolio scores last updated [N] days ago` | Prompt rescore if doing analysis |
| STALE MACRO | v1.0 | Macro context >14 days old | Step 0 — every session | `⚠️ STALE: macro context last updated [N] days ago` | Pull fresh macro before analysis |
| CONCENTRATION | v1.0 | Single sector >40% or single name >20% | Morning briefing + Portfolio Review | `⚠️ CONCENTRATION: [Sector/TICKER] at [X]% — above limit` | Flag only; user decides action |
| EARNINGS WINDOW | v1.0 | OPEN position ≤30 days from estimated results month | Morning briefing + HOLD Stage | `📅 [TICKER] results due ~[Month YYYY] ([N] days). Preview not yet run.` | Offer PREVIEW mode via `references/earnings-calendar.md` |
| MACRO SHIFT | v1.0 | SBP decision / PKR move >2% in a session / Brent move >5% | Any session where macro event is mentioned | `📊 MACRO SHIFT detected: [event]. Running impact assessment.` | Call `psx-news-monitor` → `PMEX Commodities` → `psx-portfolio-analysis` scenario rescore |
| TAX HARVEST | v1.0 | Current date within 60 days of June 30 | Morning briefing + Portfolio Review | `💰 TAX WINDOW: [N] days to June 30. Harvest opportunities available.` | Call `psx-tax-harvester` — identify loss harvest candidates |
| DRAWDOWN BREACH | v2.0 | Position breaches L1 / L2 / L3 threshold (see `references/drawdown.md` for conviction-tier thresholds) | Step 0 drawdown scan — every session | `📉 DRAWDOWN L[N]: [TICKER] is [X]% below entry` | L1: warn + continue. L2: flag + rescore. L3: halt + mandatory thesis review. |
| THESIS BROKEN | v2.0 | Position marked BROKEN in thesis status | HOLD Stage + Monthly Review | `🚨 BROKEN THESIS: [TICKER] — mandatory exit decision required` | Invoke BROKEN THESIS PROTOCOL. No "hold and hope" without Decision Journal entry. |
| DIVIDEND EX-DATE | v2.0 | Ex-date ≤15 trading days away | Morning briefing | `💰 EX-DATE: [TICKER] ex-date [DD-MMM]. Net yield [X]% after WHT.` | Flag in briefing; prompt WHT check via `psx-tax-harvester` if not yet calculated |
| WATCHLIST EXPIRY | v2.0 | Ticker on watchlist past maximum wait period (set at entry) | Morning briefing + Watchlist Management | `⏰ WATCHLIST EXPIRY: [TICKER] — entry conditions not met after [N] days. Reassess or remove?` | Present options: extend wait / update entry conditions / remove from watchlist |
| BENCHMARK LAG | v2.0 | Portfolio underperforms KSE-100 by >10% over 3 consecutive months | Benchmark session + Monthly Review | `⚠️ BENCHMARK LAG: Portfolio has underperformed KSE-100 by >10% for 3 consecutive months.` | Trigger Process Audit (Module 10 quarterly audit). Question is process soundness — not just stock swaps. |

---

## Step 0 Alert Sequence

At the start of every session, run these checks in order before any user-requested action:

1. Pull Drive context (`psx-investing-plugin`)
2. **STALE RESEARCH** — check thesis age per OPEN ticker
3. **STALE SCORES** — check composite score freshness
4. **STALE MACRO** — check macro-context.md age
5. **DRAWDOWN BREACH** — fetch live prices, compute drawdown % for each OPEN position, surface any L1/L2/L3 breaches
6. **Monthly Review overdue** — if Last Review Date >28 days, prompt (do not auto-run)

---

## Morning Briefing Alert Sequence

After Step 0, morning briefing additionally checks:

1. **DIVIDEND EX-DATE** — any OPEN position with ex-date ≤15 trading days
2. **EARNINGS WINDOW** — any OPEN position with results due ≤30 days and preview not run
3. **CONCENTRATION** — sector >40% or single name >20%
4. **TAX HARVEST** — if within 60 days of June 30
5. **WATCHLIST EXPIRY** — any watchlist ticker past max wait period
6. **Capital queue** — any slots in `capital-queue.md` ready to deploy

---

## Alert Flag Emoji Standards

| Emoji | Alert Type |
|-------|-----------|
| ⚠️ | Staleness, concentration, benchmark lag, cash floor |
| 🚨 | BROKEN thesis, Level 3 drawdown |
| 📉 | Drawdown breach (any level) |
| 📅 | Earnings window, ex-date approaching |
| 💰 | Dividend ex-date, tax harvest window |
| 📊 | Macro shift |
| ⏰ | Watchlist expiry |
| ✅ | Entry conditions met, slot ready to deploy |
