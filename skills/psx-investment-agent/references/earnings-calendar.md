# Earnings Season Calendar — Module 09

Proactive preview triggering before results — not reactive analysis after.
PSX results cluster: **February** (H1), **August** (Full Year), **October/November** (Q1).

---

## Triggers

Load this file when the user says:
- "earnings preview", "results season", "earnings calendar", "when are results", "Q results"

Also auto-checked at:
- Every **morning briefing / PORTFOLIO session** — surface any OPEN positions with results due within 30 days
- Every **HOLD STAGE ticker review** — check if results are within 30 days and preview has not yet been run

---

## Pre-Flight: Pull Drive Context

Before reviewing the calendar, call `psx-investing-plugin` to pull:
- `PSX_Research/Earnings/calendar.md` — master list of all tickers + estimated results months
- `PSX_Research/Portfolio/portfolio-master.md` — OPEN positions to cross-reference

---

## 4-Step Calendar Logic

| Step | When | Action |
|------|------|--------|
| 1. Estimate results month | Onboarding + updated annually | Infer from historical pattern + fiscal year. Store per ticker in `PSX_Research/Earnings/calendar.md`. |
| 2. Trigger PREVIEW | 30 days before estimated results month | Call `psx-earnings-analyzer` in PREVIEW mode. Save to `PSX_Research/Earnings/previews/[TICKER]_preview_[YYYY-MM].md`. |
| 3. Trigger ANALYZER | User confirms results are published | Call `psx-earnings-analyzer` in ANALYZER mode. Compare actual vs. preview. Grade forecast accuracy (Beat / In-Line / Miss / Big Miss). |
| 4. Log accuracy | After every results cycle | Append accuracy grade + notes to `PSX_Research/Earnings/outcomes/[TICKER]_outcome_[YYYY-MM].md`. Update forecast accuracy log per ticker. |

---

## Proactive PREVIEW Check

At morning briefing or HOLD Stage ticker review:

1. For each OPEN position, look up ticker in `PSX_Research/Earnings/calendar.md`
2. Compute days until estimated results month
3. If ≤ 30 days **and** preview not yet run for this cycle:
   - Flag: "📅 [TICKER] results due ~[Month YYYY] ([N] days). Earnings preview not yet run. Run now?"
   - If yes → call `psx-earnings-analyzer` PREVIEW mode → save to Drive path below
4. If preview already run for this cycle: show preview summary + flag when results are expected

---

## Earnings Calendar Display Format

```
## Earnings Calendar — OPEN Positions  [Date]

| Ticker | Est. Results Month | Days Until | Preview Run? | Last Outcome Grade |
|--------|--------------------|-----------|--------------|-------------------|
| [TKR]  | [Month YYYY]       | [N]       | Yes / No     | Beat / Miss / —   |

Upcoming (≤30 days): [TICKER list]
```

---

## Results Cluster Reference

| Cluster | Months | Coverage |
|---------|--------|----------|
| H1 Results | February | Half-year (Jul–Dec for Jun-year companies) |
| Full Year Results | August | Full-year results |
| Q1 Results | October / November | First quarter (Jul–Sep) |

*Fiscal year end varies by company — verify per ticker at onboarding.*

---

## Drive Structure

```
PSX_Research/Earnings/
├── calendar.md                              ← master list: ticker + estimated results month
├── previews/
│   └── [TICKER]_preview_[YYYY-MM].md        ← psx-earnings-analyzer PREVIEW output
└── outcomes/
    └── [TICKER]_outcome_[YYYY-MM].md        ← actual results + accuracy grade + lesson
```
