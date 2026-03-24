# Module 02 — Monthly Review Engine

Runs on the last trading Friday of each month. Prevents portfolio quality from degrading silently between ad-hoc sessions.

---

## Triggers
- User says: "monthly review", "end of month", "EOM review", "monthly check"
- Auto-prompt if last review was > 28 days ago at session start

---

## 7-Step Sequence

| # | Step | Agent Action | Skills |
|---|------|-------------|--------|
| 1 | Macro Refresh | Pull macro-context.md from Drive. Fetch live: SBP rate, KSE-100, PKR/USD, commodities. Flag regime shift. | Web search, PMEX Commodities |
| 2 | Benchmark Performance | Fetch KSE-100 monthly return. Compute weighted portfolio return. Compute alpha. Flag 2+ consecutive months underperformance. | Web search, psx-portfolio-analysis |
| 3 | Full Composite Rescore | Re-run 7-factor scoring for all holdings. Delta vs. prior month. Flag score delta > 0.5 or boundary crossing. | psx-portfolio-analysis |
| 4 | Thesis Integrity Check | Compare current fundamentals vs. original thesis per holding. Assess INTACT / STRESSED / BROKEN. BROKEN = mandatory exit flag. | sector-analysis, psx-earnings-analyzer |
| 5 | Watchlist Promotion Review | Check all watchlist entries. Flag any where entry conditions are now met. Offer to promote to OPEN. | psx-valuation-screen, psx-rs-trend |
| 6 | Forward Calendar Update | Refresh dividend ex-dates. Flag ex-dates within 15 trading days. Update earnings estimates. Trigger PREVIEW for results due next month. | psx-earnings-analyzer (PREVIEW) |
| 7 | Tax Position Snapshot | Within 120 days of June 30: flag harvest opportunities to watch. Within 60 days of June 30: full harvest analysis, act on opportunities. Otherwise: days to year-end, CGT threshold watches, losses vs. gains. | psx-tax-harvester |

---

## Output Format

Fixed sections — in this order every time:

1. **MACRO REGIME** — 3-sentence snapshot + Risk-On / Risk-Off / Transitional
2. **PORTFOLIO PERFORMANCE** — month return vs. KSE-100, YTD, alpha/beta
3. **COMPOSITE SCORE DELTA TABLE** — all holdings, current / prior / delta / boundary flag
4. **THESIS STATUS TABLE** — all holdings, status, key evidence
5. **WATCHLIST PROMOTIONS** — stocks now meeting entry conditions
6. **FORWARD CALENDAR** — ex-dates + earnings previews next 30 days
7. **TAX SNAPSHOT** — days to June 30, harvest opportunities, threshold watches
8. **3 PRIORITY ACTIONS** — highest-urgency items before next review

> Target: 800–1,200 words. Every section ends with a verdict — no ambiguous narratives.

---

## Quarterly Deep Dive (March / June / September / December)

Two additional steps added to the standard 7:
- **Sector Rotation Analysis** — re-run psx-rs-trend across all sectors
- **June Q-Review only** — run full psx-tax-harvester year-end plan before July 1

---

## Drive Output
Save to: `PSX_Research/Reviews/monthly-[YYYY-MM].md`
