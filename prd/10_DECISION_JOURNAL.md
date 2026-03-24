# Module 10 — Decision Journal

Institutional memory of every investment decision. Transforms the Agent from an analysis tool into a learning system.

---

## Journal Entry — Required Fields

| Field | Content |
|-------|---------|
| Date / Ticker / Action | Date, ticker, action: BUY / SELL / ADD / TRIM / HOLD (with reason) |
| Price & Size | Price transacted, shares, PKR amount, resulting portfolio weight |
| Composite Score at Decision | 7-factor score on decision date |
| Primary Reason | Single most important factor — 1–2 sentences max |
| Thesis Statement | BUY: full thesis (3–5 sentences). SELL: outcome verdict (validated / invalidated / captured). |
| Counter-Argument | **Mandatory.** Strongest case AGAINST this decision. Agent will prompt if left blank. |
| Exit Conditions | BUY/ADD: specific observable conditions that would make you sell |
| Market Context | KSE-100 level, SBP rate, PKR/USD on decision date |
| Emotional State Flag | Analysis / News Reaction / Momentum Chasing / Fear / Conviction Add — choose one |
| Outcome (filled post-exit) | Did thesis play out? Return achieved. Lesson. Decision quality score 1–5, independent of outcome. |

---

## Quarterly Process Audit

Run at end of each quarter on all closed positions from that quarter:

| Check | Output |
|-------|--------|
| Decision Quality Score | Average 1–5 score across closed positions |
| Bias Detection | Frequency of each Emotional State Flag |
| Thesis Accuracy | % of theses that played out as expected |
| Composite Score Predictiveness | Did high scores at entry actually outperform? |
| Hold-Too-Long Check | Were BROKEN theses exited promptly or held past the break? |

> Output: 300–400 word memo. Feeds conviction calibration for next quarter.

---

## Drive Paths
- `PSX_Research/Journal/decision-log.md` — chronological, append only
- `PSX_Research/Journal/quarterly-audit-[Q]-[YYYY].md` — one per quarter
