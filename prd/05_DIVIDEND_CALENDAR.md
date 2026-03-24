# Module 05 — Dividend Calendar

Tracks ex-dates, payout schedules, and dividend capture opportunities. PSX is income-heavy — missed ex-dates are a direct cost.

---

## Calendar Data — Per Holding

| Field | Description |
|-------|-------------|
| Ex-Date (next) | Must be held before this date to receive dividend |
| Dividend Type | Interim / Final / Special |
| Dividend Amount | PKR per share (announced or estimated) |
| Annualized Yield | Dividend ÷ current price × 100 |
| WHT Rate | From psx-tax-harvester (filer vs. non-filer) |
| Net Yield (after WHT) | Annualized yield × (1 − WHT rate) |
| Historical Pattern | 5-year dividend CAGR, typical interim/final split |
| Payout Date | Expected payment date after ex-date |

---

## Agent Actions

| Trigger | Action |
|---------|--------|
| Monthly Review Step 6 | Auto-populate ex-dates for all held tickers via web search |
| Ex-date within 15 trading days | Flag in morning briefing with net yield after WHT |
| Watchlist stock: ex-date within 30 days + entry conditions met | Flag as time-sensitive capture opportunity |
| Monthly Review | Compute yield spread = weighted portfolio yield − SBP rate. Flag if spread < 1% |

---

## Drive Path
`PSX_Research/Dividends/calendar.md`
