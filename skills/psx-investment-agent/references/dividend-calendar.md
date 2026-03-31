# Dividend Calendar — Module 05

Tracks ex-dates, payout schedules, and dividend capture opportunities.
PSX is income-heavy — missed ex-dates are a direct cost.

---

## Triggers

Load this file when the user says:
- "dividend check", "ex-date", "upcoming dividends", "dividend calendar"

Also auto-populated at **Monthly Review Step 6** (`references/monthly-review.md`).

---

## Pre-Flight: Pull Drive Context

Before displaying the calendar, call `psx-investing-plugin` to pull:
- `PSX_Research/Dividends/calendar.md` — stored dividend data
- `PSX_Research/Portfolio/portfolio-master.md` — all OPEN holdings

---

## Per-Holding Calendar Fields

All 8 fields maintained per ticker in `PSX_Research/Dividends/calendar.md`:

| Field | Description |
|-------|-------------|
| Ex-Date (next) | Must be held before this date to receive dividend |
| Dividend Type | Interim / Final / Special |
| Dividend Amount | PKR per share (announced or estimated) |
| Annualized Yield | Dividend ÷ current price × 100 |
| WHT Rate | From `psx-tax-harvester` (filer vs. non-filer) — **never hardcode** |
| Net Yield (after WHT) | Annualized yield × (1 − WHT rate) |
| Historical Pattern | 5-year dividend CAGR, typical interim/final split |
| Payout Date | Expected payment date after ex-date |

> WHT rates must always be fetched live from `psx-tax-harvester`. Never assume a fixed rate.

---

## Agent Actions

| Trigger | Action |
|---------|--------|
| Monthly Review Step 6 | Auto-populate ex-dates for all OPEN tickers via web search; update `calendar.md` in Drive |
| Ex-date within 15 trading days | Flag in session output: "📅 [TICKER] ex-date in [N] days — Net yield: [X]% after WHT. Ensure held by [Ex-Date − 1]." |
| Watchlist stock: ex-date within 30 days + entry conditions met | Flag as time-sensitive: "⚡ [TICKER] (watchlist) ex-date in [N] days and entry conditions met — capture opportunity?" |
| Monthly Review or dividend check | Compute yield spread = weighted portfolio yield − SBP policy rate. If spread < 1%: flag "⚠️ Yield spread vs. SBP rate is [X]% — portfolio income is barely beating risk-free rate." |

---

## Displaying the Calendar

When user asks "dividend check" or "upcoming dividends":

1. Pull `PSX_Research/Dividends/calendar.md` and `portfolio-master.md` from Drive
2. Fetch live prices via web search to compute current yields
3. Call `psx-tax-harvester` to get current WHT rates
4. Display summary table sorted by nearest ex-date:

```
| Ticker | Ex-Date | Type | Amount (PKR) | Gross Yield | Net Yield | Days Until |
```

5. Flag any ex-dates within 15 trading days
6. Compute and display yield spread vs. SBP rate
7. Check WATCHLIST entries for any time-sensitive capture opportunities

---

## Updating the Calendar

After a dividend is announced or results are published:
1. Update `PSX_Research/Dividends/calendar.md` via `psx-investing-plugin`
2. Update `Ex-Date (next)` field in `portfolio-master.md` for the affected ticker
3. Recompute net yield using current WHT rate from `psx-tax-harvester`

---

## Drive Path

`PSX_Research/Dividends/calendar.md`
