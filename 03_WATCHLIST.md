# Module 03 — Watchlist Management

Holding area between "researched but not bought" and "active position". Prevents research from evaporating between sessions.

---

## Watchlist Entry — Required Fields

| Field | Description |
|-------|-------------|
| Ticker | PSX ticker + company name |
| Research Date | Date analysis was completed |
| Investment Thesis v1 | 3–5 sentences: why, catalyst, exit |
| Composite Score | 7-factor score at time of research |
| Entry Conditions | Specific observable conditions before buying — e.g. "SBP cuts 100bps", "price pulls back to PKR X", "GIDC resolved" |
| Target Weight | Intended portfolio % if entry conditions met |
| Conviction Tier | HIGH / MED / TRACKER |
| Max Wait Period | Reassessment date if conditions not met (default: 90 days) |
| Thesis Invalidators | Specific events that remove this stock from watchlist entirely |

---

## Review Logic (runs automatically at Monthly Review Step 5)

| Condition | Agent Action |
|-----------|-------------|
| Max wait period exceeded, no entry | Prompt: reassess thesis or extend deadline |
| Thesis invalidator event occurs | Remove from watchlist, log reason in Drive |
| All entry conditions met | Flag for OPEN promotion, run capital deployment check (Module 08) |

---

## Drive Path
`PSX_Research/Portfolio/watchlist.md`
