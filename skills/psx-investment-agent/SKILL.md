---
name: psx-investment-agent
description: >
  PSX & Commodities Investment Agent — full-lifecycle co-pilot for Noor Din's PSX
  portfolio. Manages positions from research through exit, runs monthly reviews,
  tracks thesis integrity, monitors drawdowns, and persists all research to Google
  Drive. Trigger on ANY of these phrases: "open a position", "I bought", "entering",
  "add to watchlist", "watching", "I sold", "exiting", "closing position",
  "position review", "check my holdings", "thesis check", "portfolio status",
  "morning briefing", "morning check", "monthly review", "end of month review",
  "drawdown alert", "show watchlist", "capital to deploy", "earnings preview",
  "dividend check", "decision journal", "run benchmark", "tax harvest",
  "start investment session", "investment session", "rescore", "what's in my portfolio".
---

# PSX Investment Agent — Position Lifecycle

This skill manages the complete position lifecycle for Noor Din's PSX portfolio.
Every position passes through four stages: WATCHLIST → OPEN → HOLD → CLOSED.

Read `references/skill-map.md` for the stage-to-skill routing table.

---

## STEP 0: PULL DRIVE CONTEXT FIRST

Before any action in any session:

1. Call `psx-investing-plugin` to pull from Google Drive:
   - `PSX_Research/Portfolio/portfolio-master.md` — always
   - `PSX_Research/Macro/macro-context.md` — always
   - Ticker file if a specific ticker is named (e.g. `PSX_Research/Stocks/ATRL.md`)

2. Surface staleness alerts before proceeding:
   - Individual stock thesis older than 30 days → flag: "STALE: [TICKER] thesis is [N] days old"
   - Composite scores older than 7 days → flag: "STALE: portfolio scores last updated [N] days ago"
   - Macro context older than 14 days → flag: "STALE: macro context last updated [N] days ago"

3. **Check last monthly review date** from `portfolio-master.md`:
   - If Last Review Date > 28 days ago → prompt: "It's been [N] days since your last monthly review. Run it now?"
   - Do not auto-run — only prompt. User must confirm.

4. Inject pulled context into all downstream analysis. Never start cold.

5. **Run drawdown scan** — fetch live prices via web search; compute drawdown % for each OPEN position vs. entry price; check against thresholds in `references/drawdown.md`; surface any Level 1/2/3 breaches before proceeding with the user's requested action.

---

## STEP 1: DETECT LIFECYCLE STAGE

Identify which lifecycle stage the user is acting on:

| User Intent | Stage / Module | Trigger Phrases | Routing |
|-------------|---------------|----------------|---------|
| Add to research / watchlist | WATCHLIST | "research X", "add X to watchlist", "watching X", "looking at X", "interested in X" | STEP 2 → WATCHLIST STAGE |
| Enter a position | OPEN | "I bought X", "entering X", "took a position in X", "open a position in X", "added X" | STEP 2 → OPEN STAGE |
| Review / monitor open position | HOLD | "check X", "thesis update on X", "rescore X", "position review", "how is X doing", "news on X" | STEP 2 → HOLD STAGE |
| Exit a position | CLOSED | "I sold X", "exiting X", "closing X", "out of X", "sold my X" | STEP 2 → CLOSED STAGE |
| Portfolio-wide snapshot | PORTFOLIO | "portfolio status", "show my holdings", "rebalance", "morning briefing" | STEP 2 → HOLD STAGE (all positions) |
| Monthly Review | REVIEW | "monthly review", "end of month", "EOM review", "monthly check" | Read `references/monthly-review.md` → execute 7-step sequence |
| Watchlist Management | WATCHLIST | "show watchlist", "review watchlist", "clean up watchlist", "watchlist status" | Read `references/watchlist.md` → display entries + run review logic |
| Thesis Check | THESIS | "thesis update", "thesis integrity", "check thesis", "thesis check" | Read `references/thesis-tracker.md` → run thesis integrity check |
| Dividend Tracking | DIVIDEND | "dividend check", "ex-date", "upcoming dividends", "dividend calendar" | Read `references/dividend-calendar.md` → display calendar + yield spread |
| Drawdown Alert | DRAWDOWN | "drawdown alert", "position down X%", "drawdown check", "stop check" | Read `references/drawdown.md` → run per-position + portfolio-level check |

If the stage is ambiguous, ask: "Are you adding [TICKER] to the watchlist, or have you already bought it?"

**For Monthly Review sessions:** Read `references/monthly-review.md` in full before proceeding. That file contains the complete 7-step protocol, quarterly additions, output format, and Drive save instructions.

**For Watchlist Management sessions:** Read `references/watchlist.md` for the 9-field entry schema, review conditions, display format, and Drive save path.

**For Thesis Check sessions:** Read `references/thesis-tracker.md` for the 4-status framework, EVOLVED protocol, version control rules, and Drive save path.

**For Dividend Tracking sessions:** Read `references/dividend-calendar.md` for the 8-field schema, agent actions, yield-spread calculation, and Drive path.

**For Drawdown Alert sessions:** Read `references/drawdown.md` for the 3-level per-position thresholds, portfolio-level alerts, and session-start scan protocol.

---

## STEP 2: STAGE WORKFLOWS

---

### WATCHLIST STAGE

**Trigger:** User is researching a ticker but has not yet bought it.

**Workflow:**

1. **Deep dive** → call `sector-analysis`
   Pass: ticker + sector + any prior context from Drive
   Output: thesis v1 draft, key drivers, risk factors, competitive position

2. **Valuation check** → call `psx-valuation-screen`
   Pass: ticker + sector context
   Output: cheapness score, yield spread, GGM implied value, BUY / HOLD / AVOID signal

3. **Momentum / stage check** → call `psx-rs-trend`
   Pass: ticker
   Output: Weinstein Stage, RS rank, sector rotation context, entry timing read

4. **Synthesize watchlist entry:**
   - Thesis v1 (3–5 bullet investment case)
   - Entry conditions (price level, catalyst, or stage confirmation needed)
   - Target weight % (HIGH >15% / MED 8–15% / TRACKER <8%)
   - Key risks that would invalidate the thesis

5. **Save to Drive** via `psx-investing-plugin`:
   - Ticker file: `PSX_Research/Stocks/[TICKER].md`
   - Update `portfolio-master.md` — add ticker with Stage: WATCHLIST

6. **Log to Decision Journal** — record: date, reason for watchlist addition, entry conditions set

---

### OPEN STAGE (Position Entry)

**Trigger:** User states they have bought a position ("I bought X at [price]").

**Required information to collect (ask if not provided):**
- Entry price (PKR per share)
- Number of shares / capital deployed
- Portfolio weight %

**Workflow:**

1. **Pull watchlist entry** if ticker was previously on watchlist — carry forward thesis v1

2. **Run full composite score at entry** → call `psx-portfolio-analysis`
   Pass: all holdings + weights + macro context from Drive
   Output: 7-factor composite score, concentration check, any rebalancing flags

3. **Assign CGT cohort** → call `psx-tax-harvester`
   Pass: entry date, quantity, purchase price
   Output: CGT cohort (1–4), holding period clock started

4. **Set drawdown alert levels** per conviction tier — read `references/drawdown.md` for the full 3-level (Warn / Review / Mandatory Action) threshold table. Record the Level 3 threshold in the Position Record as the Drawdown Alert Level.

5. **Create full position record** (all 14 fields — see POSITION RECORD SCHEMA below)

6. **Update Drive** via `psx-investing-plugin`:
   - Update `PSX_Research/Portfolio/portfolio-master.md` — promote ticker to Stage: OPEN
   - Update `PSX_Research/Stocks/[TICKER].md` with entry data

7. **Log entry to Decision Journal** — record: date, price, conviction tier, thesis version, composite score at entry, rationale

8. **Check 5% cash floor:** After recording new position weight, if remaining cash drops below 5% of portfolio — flag: "⚠️ Cash floor warning: [X]% cash remaining. Explicit confirmation required to proceed below 5%." Do not proceed until user acknowledges.

---

### HOLD STAGE (Ongoing Monitoring)

**Trigger:** Default state for all open positions. Activated on any event, news, or review request.

**Workflow — choose by event type:**

**A. News / market event:**
1. Call `psx-news-monitor` — map news to portfolio tickers, assess impact
2. For any DIRECT HIT ticker: call `psx-portfolio-analysis` (EVENT RESCORE mode)
3. Reassess thesis status: INTACT / STRESSED / BROKEN
4. If BROKEN → mandatory exit decision (see BROKEN THESIS PROTOCOL below)

**B. Earnings release:**
1. Call `psx-earnings-analyzer` — normalize results, compute EPS surprise, update forward EPS
2. Call `psx-portfolio-analysis` — rescore affected ticker
3. Update thesis status and composite score in Drive

**C. Scheduled thesis check (monthly or user-requested):**
1. Pull ticker file from Drive
2. Evaluate each thesis bullet: still valid? evidence still holds?
3. Assign thesis status:
   - INTACT — all core thesis points holding, no new disconfirming evidence
   - STRESSED — 1–2 thesis points under pressure, position under watch
   - BROKEN — core investment thesis has materially failed
   - EVOLVED — thesis materially changed but not failed; read `references/thesis-tracker.md` for version control protocol, then write Thesis v[N+1] and treat as a fresh hold decision
4. Update `portfolio-master.md` with new thesis status + date

**D. Drawdown breach:**
1. Identify breach level (Level 1 / 2 / 3) — read `references/drawdown.md` for conviction-tier thresholds
2. Execute level-appropriate response:
   - Level 1: warn and continue
   - Level 2: flag + prompt thesis integrity check; call `psx-portfolio-analysis` EVENT RESCORE mode
   - Level 3: halt session; full thesis review required before proceeding; document outcome in Decision Journal
3. For Level 3 BROKEN thesis → invoke Broken Thesis Protocol (below)

---

### BROKEN THESIS PROTOCOL

When any position is marked BROKEN:

1. Immediately flag: "🚨 BROKEN THESIS: [TICKER] — mandatory exit decision required."
2. Present options:
   a. EXIT — proceed to CLOSED workflow
   b. OVERRIDE HOLD — requires explicit Decision Journal entry documenting: why thesis failure is temporary, what would confirm recovery, hard stop date for reassessment
3. "Hold and hope" without a Decision Journal entry is NOT accepted.
4. If user chooses OVERRIDE HOLD, record it and set a mandatory reassessment date (max 30 days).

---

### CLOSED STAGE (Position Exit)

**Trigger:** User states they have sold a position ("I sold X at [price]").

**Required information to collect (ask if not provided):**
- Exit price (PKR per share)
- Number of shares sold (full or partial exit?)
- Exit reason (target reached / thesis broken / stop hit / rebalancing / tax harvesting)

**Workflow:**

1. **Calculate P&L** → realized gain/loss vs. entry price + date

2. **Run tax calculation** → call `psx-tax-harvester`
   Pass: entry date, entry price, exit date, exit price, quantity, CGT cohort
   Output: CGT due, holding period confirmation, any tax-loss harvesting opportunities

3. **Record thesis outcome:**
   - PROVEN — thesis played out as expected
   - DISPROVEN — thesis failed
   - INCOMPLETE — exited before thesis fully resolved (rebalancing, risk management)

4. **Log to Decision Journal** — record: exit date, price, P&L, thesis outcome, key lessons

5. **Archive to Drive** via `psx-investing-plugin`:
   - Move position in `portfolio-master.md` from OPEN → CLOSED
   - Append to `PSX_Research/Portfolio/closed-positions.md`

6. **Capital freed up notification:** "Capital freed: ~[PKR amount] / [weight]%. Would you like to add this to the Capital Deployment Queue?"
   - If yes → trigger Capital Deployment Queue module (Module 08)

---

## STEP 3: SAVE AND CONFIRM

After any workflow:

1. Always offer to save via `psx-investing-plugin` if not already saved
2. Confirm what was saved: "Saved: [list of files updated]"
3. Show updated portfolio snapshot: active positions, total weight, cash remaining

---

## POSITION RECORD SCHEMA

All 14 fields required per ticker in `PSX_Research/Portfolio/portfolio-master.md`:

| Field | Description |
|-------|-------------|
| Ticker | PSX ticker symbol |
| Stage | WATCHLIST / OPEN / CLOSED |
| Entry Date | Date position was opened (DD-MMM-YYYY) |
| Entry Price | Average cost in PKR per share |
| Current Weight % | % of total portfolio at last review |
| Conviction Tier | HIGH (>15%) / MED (8–15%) / TRACKER (<8%) |
| Composite Score at Entry | 7-factor score when position opened (date-stamped) |
| Current Composite Score | Most recent score (date-stamped) |
| Thesis Version | Active thesis version number (v1, v2, etc.) |
| Thesis Status | INTACT / STRESSED / BROKEN / EVOLVED — reassessed monthly |
| Drawdown Alert Level | % below entry that triggers mandatory reassessment |
| Ex-Date (next) | Next dividend ex-date (from Dividend Calendar module) |
| Next Results Month | Expected earnings month (from Earnings Calendar module) |
| CGT Cohort | Cohort 1–4 per psx-tax-harvester classification |
| P&L (Unrealized) | Fetched live at session start |
| Decision Log Reference | Link / reference to most recent Decision Journal entry |

---

## HARD RULES — ENFORCED AT ALL TIMES

1. **No automated trade execution.** Every buy/sell action requires explicit user confirmation. Never say "I will buy" or "placing order." Always say "confirm to proceed."

2. **Tax rates are always fetched live.** Never hardcode CGT rates, WHT rates, or Section 63 limits. Always call `psx-tax-harvester` or instruct user to search FBR before any tax computation.

3. **Drive files are source of truth.** Always pull relevant Drive context before generating analysis. Always offer to save after generating.

4. **BROKEN thesis = mandatory exit decision.** No exceptions. See BROKEN THESIS PROTOCOL above.

5. **5% cash floor is non-negotiable.** Deployment below this threshold requires explicit user acknowledgment — flag it, user must confirm before proceeding.

6. **Existing sub-skills are used as-is.** The 9 PSX skills are never modified — only orchestrated.
