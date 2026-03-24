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

## Drive Structure

```
PSX_Research/Earnings/
├── calendar.md              ← master list: all tickers + estimated results month
├── previews/
│   └── [TICKER]_preview_[YYYY-MM].md
└── outcomes/
    └── [TICKER]_outcome_[YYYY-MM].md   ← actual results + accuracy grade
```
