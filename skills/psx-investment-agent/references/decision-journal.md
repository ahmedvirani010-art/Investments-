# Decision Journal — Module 10

Institutional memory of every investment decision.
Transforms the Agent from an analysis tool into a learning system.

---

## Triggers

Load this file when the user says:
- "decision journal", "log a trade", "log my decision", "process audit", "quarterly audit", "quarterly review"

Also auto-triggered when:
- **WATCHLIST STAGE Step 6** — log watchlist addition
- **OPEN STAGE Step 7** — log position entry (BUY)
- **HOLD STAGE Step D Level 3** — log drawdown event outcome
- **BROKEN THESIS PROTOCOL** — log override hold or exit decision
- **CLOSED STAGE Step 4** — log position exit (SELL)

---

## Pre-Flight: Pull Drive Context

Before logging, call `psx-investing-plugin` to pull:
- `PSX_Research/Journal/decision-log.md` — append to this file

---

## 10 Required Fields Per Entry

| Field | Content |
|-------|---------|
| Date / Ticker / Action | Date, ticker, action: BUY / SELL / ADD / TRIM / HOLD (with reason) |
| Price & Size | Price transacted, shares, PKR amount, resulting portfolio weight |
| Composite Score at Decision | 7-factor composite score on decision date |
| Primary Reason | Single most important factor driving this decision — 1–2 sentences max |
| Thesis Statement | BUY/ADD: full thesis (3–5 sentences). SELL: outcome verdict — Validated / Invalidated / Captured partial. |
| Counter-Argument | **Mandatory.** Strongest case AGAINST this decision — 1–3 sentences. Agent blocks submission if blank. |
| Exit Conditions | BUY/ADD only: specific observable conditions that would make you sell — list 2–3 triggers |
| Market Context | KSE-100 level, SBP policy rate, PKR/USD on decision date |
| Emotional State Flag | Choose one: Analysis / News Reaction / Momentum Chasing / Fear / Conviction Add |
| Outcome | **Filled post-exit only.** Did thesis play out? Return achieved. Key lesson. Decision quality score 1–5 (quality = process, independent of outcome). |

---

## Agent Logic

### On BUY (OPEN Stage Step 7)
1. Pre-fill: Date, Ticker, Action = BUY, Entry Price, Portfolio Weight, Composite Score, Market Context
2. Prompt user to complete: Primary Reason, Thesis Statement, Counter-Argument, Exit Conditions, Emotional State Flag
3. **Counter-Argument gate:** If left blank → "Decision Journal requires a counter-argument. What is the strongest case against buying [TICKER]?" Do not log until answered.
4. Append completed entry to `PSX_Research/Journal/decision-log.md`

### On SELL (CLOSED Stage Step 4)
1. Pre-fill: Date, Ticker, Action = SELL, Exit Price, P&L, Weeks Held, Thesis Outcome (PROVEN / DISPROVEN / INCOMPLETE)
2. Prompt user to complete: Primary Reason, Outcome verdict, Key lesson, Decision quality score 1–5
3. Append to `PSX_Research/Journal/decision-log.md`
4. Also update Outcome field on the original BUY entry (if traceable by date/ticker)

### On WATCHLIST Addition (WATCHLIST Stage Step 6)
1. Pre-fill: Date, Ticker, Action = WATCHLIST ADD
2. Log: reason for watchlist addition, entry conditions set, conviction tier assigned
3. Counter-Argument required before logging

### On BROKEN THESIS Override Hold
1. Action = OVERRIDE HOLD
2. Required fields: why thesis failure is temporary, what would confirm recovery, hard stop date for reassessment (max 30 days)
3. **"Hold and hope" without a completed entry is NOT accepted — Agent blocks the session.**

---

## Quarterly Process Audit

**Trigger:** "process audit", "quarterly audit", "quarterly review", or at end of each quarter

**Steps:**
1. Pull all closed position entries from `PSX_Research/Journal/decision-log.md` for the quarter
2. Run 5 audit checks:

| Check | Output |
|-------|--------|
| Decision Quality Score | Average 1–5 score across all closed positions this quarter |
| Bias Detection | Count and % frequency of each Emotional State Flag |
| Thesis Accuracy | % of theses that played out as expected (PROVEN vs. DISPROVEN) |
| Composite Score Predictiveness | Did higher composite scores at entry actually outperform lower-scored entries? |
| Hold-Too-Long Check | For BROKEN thesis positions — were they exited promptly or held past the break? |

3. Write 300–400 word memo summarising findings and 1–2 conviction calibration adjustments for next quarter
4. Save to: `PSX_Research/Journal/quarterly-audit-[Q]-[YYYY].md` (e.g. `quarterly-audit-Q1-2026.md`)

---

## Drive Paths

- `PSX_Research/Journal/decision-log.md` — chronological, **append only, never overwrite**
- `PSX_Research/Journal/quarterly-audit-[Q]-[YYYY].md` — one per quarter
