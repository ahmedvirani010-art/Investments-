# Monthly Review Engine — Module 02

Runs on the last trading Friday of each month. Prevents portfolio quality from
degrading silently between ad-hoc sessions.

---

## Triggers

- **Explicit:** "monthly review", "end of month", "EOM review", "monthly check"
- **Auto-prompt:** If `portfolio-master.md` Last Review Date > 28 days ago at session
  start → prompt: "It's been [N] days since your last monthly review. Run it now?"

---

## Pre-Flight: Pull Drive Context

Before starting the sequence, call `psx-investing-plugin` to pull:
- `PSX_Research/Portfolio/portfolio-master.md` — all holdings + last review date
- `PSX_Research/Macro/macro-context.md` — stored macro snapshot
- `PSX_Research/Portfolio/scores-history.md` — prior month composite scores

---

## 7-Step Sequence

Execute steps in order. Do not skip any step.

---

### STEP 1 — Macro Refresh

**Action:**
1. Pull stored `macro-context.md` from Drive (already fetched in pre-flight)
2. Fetch live data via web search:
   - SBP policy rate (current)
   - KSE-100 level + monthly return %
   - PKR/USD exchange rate
   - Brent crude price
   - Gold price (PKR/tola or USD/oz)
3. Call `PMEX Commodities` if any portfolio holdings are commodity-linked
4. Compare live vs. stored — what shifted materially since last review?
5. Assign macro regime: **Risk-On** / **Risk-Off** / **Transitional**
   - Risk-On: SBP cutting, PKR stable/strengthening, KSE-100 uptrend
   - Risk-Off: SBP hiking or holding at restrictive level, PKR weakening, KSE-100 under pressure
   - Transitional: mixed signals, regime not yet confirmed
6. Update `macro-context.md` with today's live data and regime label

**Output:** 3-sentence macro snapshot + regime verdict.

---

### STEP 2 — Benchmark Performance

**Action:**
1. Fetch KSE-100 monthly return % via web search
2. Compute weighted portfolio return for the month:
   - Use entry prices + current prices from portfolio-master.md
   - Weight each position by its portfolio weight %
3. Compute alpha = portfolio return − KSE-100 return
4. Compute YTD portfolio return vs. KSE-100 YTD
5. Call `psx-portfolio-analysis` for beta and concentration review
6. **Flag:** If 2 or more consecutive months of underperformance → "⚠️ 2-month underperformance vs. benchmark. Strategy review warranted."

**Output:** Monthly return vs. KSE-100 / YTD return vs. KSE-100 / alpha / beta / any underperformance flag.

---

### STEP 3 — Full Composite Rescore

**Action:**
1. Call `psx-portfolio-analysis` for all OPEN holdings
   - Pass: current holdings + weights + macro context (just updated in Step 1)
   - Output: updated 7-factor composite score per holding
2. Pull prior month scores from `scores-history.md`
3. Compute delta per holding: current score − prior month score
4. **Flag conditions:**
   - Score delta > +0.5 or < −0.5 → material change, highlight
   - Score crosses a conviction boundary (e.g. was 6.8, now 7.2 → HIGH threshold crossed) → flag
5. Append new scores to `scores-history.md` (never overwrite)

**Output:** Composite Score Delta Table (all holdings: current / prior / delta / boundary flag).

---

### STEP 4 — Thesis Integrity Check

**Action:**
1. For each OPEN holding, pull ticker file from Drive (`PSX_Research/Stocks/[TICKER].md`)
2. Compare current fundamentals vs. original thesis bullets:
   - Is the core growth/value driver still intact?
   - Have earnings surprised positively or negatively?
   - Has sector dynamics shifted against the thesis?
   - Any management changes, regulatory risk, or structural threats emerged?
3. Call `sector-analysis` for any holding where thesis is in question
4. Call `psx-earnings-analyzer` for any holding with results in the past 30 days
5. Assign thesis status per holding:
   - **INTACT** — all core thesis points holding, no new disconfirming evidence
   - **STRESSED** — 1–2 thesis points under pressure; position under active watch
   - **BROKEN** — core investment thesis has materially failed
6. **BROKEN thesis → invoke Broken Thesis Protocol** (defined in SKILL.md):
   - Flag immediately: "🚨 BROKEN THESIS: [TICKER] — mandatory exit decision required."
   - Do not continue to next holding until user addresses it
7. Update thesis status + date in `portfolio-master.md` for all holdings

**Output:** Thesis Status Table (all holdings: status / key supporting or disconfirming evidence sentence).

---

### STEP 5 — Watchlist Promotion Review

**Action:**
1. Pull all WATCHLIST entries from `portfolio-master.md`
2. For each watchlist ticker, check entry conditions set at watchlist time:
   - Call `psx-valuation-screen` — is the buy signal now active?
   - Call `psx-rs-trend` — has the Weinstein Stage improved / entry timing confirmed?
3. For any ticker where entry conditions are now met:
   - Flag: "✅ [TICKER] entry conditions met. Promote to OPEN?"
   - If user says yes → trigger OPEN workflow from SKILL.md
4. For watchlist entries older than 90 days with no progress → flag for removal or thesis refresh

**Output:** List of watchlist tickers now meeting entry conditions, with signal summary. If none: "No watchlist promotions this month."

---

### STEP 6 — Forward Calendar Update

**Action:**
1. **Dividend ex-dates:**
   - Check upcoming ex-dates for all OPEN holdings (web search + prior calendar data)
   - Flag any ex-dates within 30 days: "📅 [TICKER] ex-date: [DATE] — ensure holding by [DATE − 1]"
2. **Earnings calendar:**
   - Identify which OPEN holdings report results next month
   - Call `psx-earnings-analyzer` in **PREVIEW mode** for each:
     - Pass: ticker + prior earnings data + current thesis
     - Output: earnings preview — what to expect, key metrics to watch, consensus vs. prior
3. Update `earnings-calendar.md` and `dividend-calendar.md` in Drive

**Output:** Table of ex-dates within 30 days + earnings previews for next month's results.

---

### STEP 7 — Tax Position Snapshot

**Action:**
1. Call `psx-tax-harvester` with current portfolio state:
   - Pass: all holdings with entry dates, entry prices, CGT cohorts, current prices
2. **If within 120 days of June 30 (i.e., after ~March 1):**
   - Run full harvest analysis: which losses to realize, which gains to defer
   - Identify cross-cohort harvesting opportunities
   - Flag any position near the CGT exemption threshold
3. **Otherwise (more than 120 days from June 30):**
   - Days remaining to June 30
   - Current unrealized gains vs. losses balance
   - Any CGT cohort boundaries approaching in next 30 days
4. **Note:** Never hardcode CGT rates — always fetch live via `psx-tax-harvester`

**Output:** Days to June 30 / unrealized gains-losses balance / harvest opportunities or threshold watches.

---

## Quarterly Deep Dive

Run these additional steps in **March, June, September, and December** only:

### STEP 8 — Sector Rotation Analysis (all quarters)

1. Call `psx-rs-trend` across all major KSE sectors
2. Identify: which sectors are strengthening vs. weakening in momentum
3. Compare portfolio sector weights vs. sector strength ranking
4. Flag any major misalignment (overweight weak sectors, underweight strong ones)

### STEP 9 — Year-End Tax Plan (June only)

1. Call `psx-tax-harvester` for full year-end plan
2. Output: complete harvest strategy, positions to exit before June 30, positions to hold
3. This replaces the standard Step 7 snapshot for the June review

---

## Output Format

Produce exactly 8 sections in this order every time:

```
## 1. MACRO REGIME
[3-sentence snapshot]
Verdict: Risk-On / Risk-Off / Transitional

## 2. PORTFOLIO PERFORMANCE
Monthly: [X]% vs KSE-100 [Y]% | Alpha: [Z]%
YTD: [X]% vs KSE-100 [Y]%
[Any underperformance flag]

## 3. COMPOSITE SCORE DELTA TABLE
| Ticker | Prior Score | Current Score | Delta | Flag |
...

## 4. THESIS STATUS TABLE
| Ticker | Status | Key Evidence |
...

## 5. WATCHLIST PROMOTIONS
[Tickers meeting entry conditions, or "None this month."]

## 6. FORWARD CALENDAR
[Ex-dates within 30 days + earnings previews]

## 7. TAX SNAPSHOT
Days to June 30: [N]
[Harvest opportunities or threshold watches]

## 8. PRIORITY ACTIONS (Top 3)
1. [Highest urgency action]
2. [Second priority]
3. [Third priority]
```

> Target: 800–1,200 words total. Every section ends with a clear verdict — no ambiguous narratives.

---

## Drive Output

After completing the sequence and user confirms:
- Save full review to: `PSX_Research/Reviews/monthly-[YYYY-MM].md`
- Update `PSX_Research/Macro/macro-context.md` with Step 1 live data
- Append scores to `PSX_Research/Portfolio/scores-history.md`
- Update `portfolio-master.md` with new thesis statuses + last review date = today

All saves routed through `psx-investing-plugin`.
