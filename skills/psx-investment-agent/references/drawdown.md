# Drawdown Control System — Module 06

Forcing functions — not stop-losses. Thresholds that require mandatory thesis
reassessment before holding further. The Agent does not execute trades.

---

## Triggers

Load this file when the user says:
- "drawdown alert", "position down X%", "drawdown check", "stop check"

Also **auto-checked at every session start** (Step 0 of SKILL.md).

---

## Per-Position 3-Level Alert System

| Tier | Level 1 — Warn | Level 2 — Review | Level 3 — Mandatory Action |
|------|---------------|-----------------|---------------------------|
| HIGH conviction (>15% weight) | −10% from entry | −18% from entry | −25%: full thesis review. BROKEN = exit. INTACT = reduce to MED sizing. |
| MED conviction (8–15% weight) | −12% from entry | −20% from entry | −28%: thesis review. BROKEN = exit. STRESSED = halve position. INTACT = document and hold. |
| TRACKER (<8% weight) | −15% from entry | −25% from entry | −35%: mandatory exit unless thesis materially improved since entry. |

---

## Level Response Protocol

**Level 1 — Warn:**
- Flag in session output: "⚠️ [TICKER] at [N]% drawdown from entry ([conviction tier] — Level 1 warn at [threshold]%)."
- No action required. Continue session.

**Level 2 — Review:**
- Flag: "⚠️ [TICKER] at [N]% drawdown. Level 2 review threshold reached."
- Prompt thesis integrity check: call `psx-portfolio-analysis` (EVENT RESCORE mode)
- Reassess thesis status using `references/thesis-tracker.md`
- Document outcome in Decision Journal

**Level 3 — Mandatory Action:**
- Flag: "🚨 [TICKER] at [N]% drawdown. LEVEL 3 — mandatory action required before session continues."
- Full thesis review required immediately using `references/thesis-tracker.md`
- Response depends on thesis status:
  - **BROKEN** → invoke Broken Thesis Protocol (SKILL.md) — mandatory exit decision
  - **STRESSED** (MED tier): halve position; document reasoning in Decision Journal
  - **INTACT** (HIGH/MED tier): document explicitly why hold is justified; Decision Journal entry required
  - **TRACKER**: mandatory exit unless thesis materially improved since entry date
- Set mandatory reassessment date: max 30 days from today
- Do not proceed with the user's requested action until Level 3 is addressed

---

## Portfolio-Level Alerts

Run these checks alongside per-position scan at session start:

| Threshold | Agent Response |
|-----------|---------------|
| Portfolio down 8% from peak NAV | Flag in session: "⚠️ Portfolio is [N]% below peak. Determine: systematic (KSE-100 down) or idiosyncratic?" Compare vs. KSE-100 drawdown over same period. |
| Portfolio down 15% from peak NAV | Mandatory session: "🚨 Portfolio at [N]% drawdown from peak. Full rescore + macro scenario analysis required. Is cash the right position?" Call `psx-portfolio-analysis` for full portfolio rescore. |
| Underperforms KSE-100 by >10% over rolling 3 months | Flag: "⚠️ Portfolio has underperformed KSE-100 by [N]% over 3 months. Process Audit (Module 10) recommended — not just a portfolio review." |

> Portfolio peak NAV tracked in `PSX_Research/Portfolio/portfolio-master.md` — update the peak value at each session if current value exceeds it.

---

## Session-Start Scan

Runs automatically after Drive context pull (Step 0 of SKILL.md):

1. Fetch live prices via web search for all OPEN positions
2. Compute drawdown % = (entry price − current price) / entry price × 100 for each position
3. Check each position against its conviction tier thresholds (table above)
4. Check portfolio-level thresholds
5. Surface all breaches at the top of the session before the user's requested action:
   - Level 1: warn and continue
   - Level 2: flag and prompt review
   - Level 3: halt and require resolution first
6. If no breaches: "✅ No drawdown alerts. All positions within thresholds."

---

## Drive Path

Drawdown events logged to:
- `PSX_Research/Portfolio/portfolio-master.md` — Drawdown Alert Level field updated per position
- Decision Journal (`PSX_Research/Decisions/decision-log.md`) — mandatory for Level 3 events
