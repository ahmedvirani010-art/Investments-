# Module 06 — Drawdown Control System

Forcing functions — not stop-losses. Thresholds that require mandatory thesis reassessment before holding further. Agent does not execute trades.

---

## Per-Position Alert Levels

| Tier | Level 1 (Warn) | Level 2 (Review) | Level 3 (Mandatory Action) |
|------|---------------|-----------------|---------------------------|
| HIGH conviction (>15%) | −10% from entry | −18% from entry | −25%: Full thesis review. BROKEN = exit. INTACT = reduce to MED sizing. |
| MED conviction (8–15%) | −12% from entry | −20% from entry | −28%: Thesis review. BROKEN = exit. STRESSED = halve position. INTACT = document and hold. |
| TRACKER (<8%) | −15% from entry | −25% from entry | −35%: Mandatory exit unless thesis materially improved since entry. |

---

## Portfolio-Level Alerts

| Threshold | Agent Response |
|-----------|---------------|
| Portfolio down 8% from peak | Morning briefing drawdown flag. Determine: systematic (KSE-100 down) or idiosyncratic? |
| Portfolio down 15% from peak | Mandatory session: full rescore + macro scenario analysis. Agent asks: is cash the right position? |
| Portfolio underperforms KSE-100 by >10% over 3 months | Trigger Process Audit (Module 10) — not just a portfolio review |

---

## Detection Timing
Drawdown levels checked at every session start against live prices fetched via web search.
