# Module 01 — Portfolio Management Lifecycle

Every position passes through four stages. The Agent tracks stage, records transitions, and routes to the correct skill at each one.

---

## Lifecycle Stages

| Stage | Entry Trigger | Agent Action | Skills |
|-------|--------------|--------------|--------|
| WATCHLIST | Research done, no position yet | Create entry: thesis v1, entry conditions, target weight → store in Drive | sector-analysis, psx-valuation-screen, psx-rs-trend |
| OPEN | "I bought X" / "entering X" | Promote from watchlist. Record: date, price, weight, thesis version, conviction tier, composite score at entry | psx-portfolio-analysis, Decision Journal |
| HOLD | Default for all open positions | Monthly review, thesis checks, drawdown monitoring, rescore on events | All skills per event |
| CLOSED | "I sold X" / "exiting X" | Record exit: date, price, P&L, thesis outcome, lessons. Archive to Drive | psx-tax-harvester, Decision Journal |

---

## Position Record — Required Fields

Stored per ticker in `PSX_Research/Portfolio/portfolio-master.md`

| Field | Description |
|-------|-------------|
| Ticker / Stage | PSX ticker + WATCHLIST / OPEN / CLOSED |
| Entry Date / Price | Date opened, average cost (PKR) |
| Current Weight % | % of portfolio at last review |
| Conviction Tier | HIGH (>15%) / MED (8–15%) / TRACKER (<8%) |
| Composite Score at Entry | 7-factor score when position opened |
| Current Composite Score | Most recent score (date-stamped) |
| Thesis Version | Active version number |
| Thesis Status | INTACT / STRESSED / BROKEN — assessed monthly |
| Drawdown Alert Level | % below entry that triggers mandatory reassessment |
| Ex-Date (next) | From Dividend Calendar module |
| Next Results Month | From Earnings Calendar module |
| CGT Cohort | Cohorts 1–4 per psx-tax-harvester |
| P&L (Unrealized) | Fetched live at session start |
| Decision Log Reference | Link to Decision Journal entry |
