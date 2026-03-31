# Watchlist Management — Module 03

Holding area between "researched but not bought" and "active position".
Prevents research from evaporating between sessions.

---

## Triggers

Load this file when the user says:
- "show watchlist", "review watchlist", "clean up watchlist", "watchlist status"

Also used automatically at **Monthly Review Step 5** (`references/monthly-review.md`).

---

## Pre-Flight: Pull Drive Context

Before displaying or reviewing the watchlist, call `psx-investing-plugin` to pull:
- `PSX_Research/Portfolio/watchlist.md` — all WATCHLIST entries

---

## Watchlist Entry — Required Fields

All 9 fields required per ticker in `PSX_Research/Portfolio/watchlist.md`:

| Field | Description |
|-------|-------------|
| Ticker | PSX ticker + company name |
| Research Date | Date analysis was completed (DD-MMM-YYYY) |
| Investment Thesis v1 | 3–5 sentences: why this stock, what catalyst, what exit condition |
| Composite Score | 7-factor score at time of research (date-stamped) |
| Entry Conditions | Specific observable conditions before buying — e.g. "SBP cuts 100bps", "price pulls back to PKR X", "GIDC resolved" |
| Target Weight | Intended portfolio % if entry conditions are met |
| Conviction Tier | HIGH (>15%) / MED (8–15%) / TRACKER (<8%) |
| Max Wait Period | Reassessment date if conditions not met (default: 90 days from Research Date) |
| Thesis Invalidators | Specific events that remove this stock from watchlist entirely |

---

## Displaying the Watchlist

When user asks "show watchlist" or "watchlist status":

1. Pull `PSX_Research/Portfolio/watchlist.md` from Drive
2. Display all WATCHLIST entries in a summary table:
   - Ticker / Research Date / Conviction Tier / Entry Conditions / Days on Watchlist / Max Wait Deadline
3. Flag any entries where Max Wait Period is within 14 days of expiry: "⏰ [TICKER] watchlist deadline in [N] days."
4. Flag any entries older than 90 days: "📌 [TICKER] on watchlist for [N] days — consider reassessment."

---

## Review Logic

Run these checks when reviewing the watchlist (standalone or at Monthly Review Step 5):

| Condition | Agent Action |
|-----------|-------------|
| Max wait period exceeded, no entry | Prompt: "Reassess thesis for [TICKER] or extend deadline?" — do not auto-remove |
| Thesis invalidator event has occurred | Remove from watchlist. Log reason to Drive: `PSX_Research/Portfolio/watchlist.md` + Decision Journal entry |
| All entry conditions met | Flag: "✅ [TICKER] entry conditions met. Promote to OPEN?" — if yes, trigger OPEN workflow in SKILL.md |

For any ticker where entry conditions may be met:
1. Call `psx-valuation-screen` — confirm buy signal active
2. Call `psx-rs-trend` — confirm Weinstein Stage and entry timing
3. If both confirm → flag for promotion

---

## Adding a New Watchlist Entry

When WATCHLIST STAGE completes (SKILL.md Step 2):
1. Collect all 9 required fields
2. Save to `PSX_Research/Portfolio/watchlist.md` via `psx-investing-plugin`
3. Also save to `PSX_Research/Stocks/[TICKER].md` — full research output
4. Update `portfolio-master.md` — add ticker with Stage: WATCHLIST

---

## Removing a Watchlist Entry

When user removes a ticker from watchlist (thesis invalidated, interest lost, or promoted to OPEN):
1. Log removal reason to Decision Journal
2. Archive entry to `PSX_Research/Portfolio/watchlist-archive.md` — never delete permanently
3. Remove from active `watchlist.md`
4. Update `portfolio-master.md` — remove or promote ticker accordingly

---

## Drive Path

`PSX_Research/Portfolio/watchlist.md` — active entries only
`PSX_Research/Portfolio/watchlist-archive.md` — removed/expired entries
