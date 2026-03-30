# Module 09 — Earnings Season Calendar

Proactive preview triggering before results — not reactive analysis after. PSX results cluster: February (H1), August (FY), October/November (Q1).

---

## Calendar Logic

| Step | When | Action |
|------|------|--------|
| Estimate results month | Onboarding + updated annually | Infer from historical pattern + fiscal year. Store per ticker in Drive. |
| Trigger PREVIEW | 30 days before estimated results month | Run psx-earnings-analyzer in PREVIEW mode. Save output to Drive. |
| Trigger ANALYZER | User confirms results are out | Run psx-earnings-analyzer in ANALYZER mode. Compare to preview. Grade forecast accuracy. |
| Log accuracy | After every results cycle | Maintain forecast accuracy log per ticker. Improves future preview calibration. |

---

## Priority Catalyst Calendar (per holding)

Non-earnings events that are the single most important catalyst for each holding. Monitor alongside the earnings calendar.

| Ticker | Priority Event / Date |
|---|---|
| ATRL | Next OGRA petroleum product price notification |
| PNSC | Q3 FY26 results — confirms freight rate capture |
| NRL | Next quarterly results — lube vs fuel segment split |
| POL | Semi-annual results + OGRA wellhead price review |
| OGDC | IMF programme review (circular debt resolution linked) |
| NATF | SBP May 2026 MPC decision |
| ICL | April 2026 — flaker plant commissioning confirmation |
| PAKT | FY2026 federal budget (June 2026) — FED rate announcement |
| BFBIO | Next quarterly revenue — confirms Zeptide ramp pace |
| BAFL | SBP rate cut materialising — threshold trigger for re-weight decision |
| HALEON | DRAP pricing revision announcement |
| AGP | Next quarterly gross margin |
| HIGHNOON | FORCE export approval announcement |
| ATLH | PAMA monthly motorcycle volumes |

**Routing rule:** At each session start, check whether any priority event has occurred or is within 14 days. If yes, trigger the relevant module (Thesis Review / Earnings Preview / Macro Shock) before proceeding.

---

## Drive Structure

```
PSX_Research/Earnings/
├── calendar.md              ← master list: all tickers + estimated results month
├── previews/
│   └── [TICKER]_preview_[YYYY-MM].md
└── outcomes/
    └── [TICKER]_outcome_[YYYY-MM].md   ← actual results + accuracy grade
```
