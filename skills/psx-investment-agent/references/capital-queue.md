# Capital Deployment Queue — Module 08

Undeployed cash is a portfolio position.
Prevents idle cash and impulsive deployment via conviction-tiered, condition-based staging.

---

## Triggers

Load this file when the user says:
- "capital to deploy", "cash queue", "what to buy next", "deploy cash"

Also auto-checked at every **morning briefing** and when a position is closed (CLOSED STAGE Step 6).

---

## Pre-Flight: Pull Drive Context

Before reviewing the queue, call `psx-investing-plugin` to pull:
- `PSX_Research/Portfolio/capital-queue.md` — current queue state
- `PSX_Research/Portfolio/portfolio-master.md` — current weights + cash %
- `PSX_Research/Portfolio/watchlist.md` — watchlist entries with entry conditions

---

## 4-Slot Queue Structure

| Slot | Source | Entry Condition | Sizing Rule |
|------|--------|----------------|-------------|
| **Slot A — HIGH conviction** | Watchlist HIGH tier ticker | All entry conditions met + composite score ≥ 7.0 + RS Weinstein Stage 2 or early Stage 3 | Full target weight — deploy in a single tranche |
| **Slot B — MED conviction (staged)** | Watchlist MED tier ticker | Entry conditions met + composite 5.5–6.9 + current price within 5% of target entry | 50% at entry; 50% at T+30 if thesis still holding — prompt user at T+30 |
| **Slot C — Opportunistic** | Event rescore: market overreaction to one-off event | Composite score jumped ≥ 1.0 point due to news, earnings miss, or sector dislocation | 1 tranche = 50% of target weight; review at T+30 |
| **Cash Floor** | Always maintained | Portfolio cash ≥ 5% at all times | Non-negotiable. Breach requires explicit user acknowledgment before any deployment proceeds. |

---

## Agent Logic

### At Morning Briefing or "Capital to Deploy"

1. Pull `PSX_Research/Portfolio/capital-queue.md` from Drive
2. Display all active slots with signal summary:
   ```
   | Slot | Ticker | Conviction | Composite | Signal | Proposed Size | Status |
   ```
3. Flag any Slot B / Slot C positions due for T+30 review
4. Check if any watchlist entries now meet Slot A or B conditions — flag for queue promotion
5. Show cash % remaining and max deployable without breaching 5% floor

### Watchlist Stock Meets Entry Conditions

1. Check conviction tier and composite score
2. Auto-populate appropriate slot:
   - HIGH + composite ≥ 7.0 + Stage 2/3 → Slot A
   - MED + composite 5.5–6.9 → Slot B
3. Flag: "✅ [TICKER] entry conditions met — proposed for Slot [A/B]. Confirm to add?"
4. Do not add without user confirmation

### Slot B / Slot C T+30 Review

At session start, check `capital-queue.md` for any staged entries ≥ 30 days from initial entry:
- Prompt: "📅 [TICKER] Slot [B/C] T+30 — thesis still holding? Options: (1) Deploy second tranche, (2) Hold pending, (3) Exit first tranche."
- Run thesis integrity check (`references/thesis-tracker.md`) before confirming second tranche

### Cash Floor Enforcement

Before confirming any deployment:
1. Compute post-deployment cash % = current cash % − proposed deployment weight
2. If post-deployment cash < 5%:
   - Flag: "⚠️ Cash floor warning: deploying this position would leave [X]% cash. 5% floor requires explicit acknowledgment."
   - Do not proceed until user confirms
3. If current cash is already below 5%: flag immediately at session start

### Capital Freed from Closed Position

When a position closes (CLOSED STAGE Step 6 in SKILL.md):
1. Compute capital freed: PKR amount + weight released
2. Prompt: "Capital freed: ~[PKR amount] / [weight]% released from [TICKER]. Add to Capital Deployment Queue?"
3. If yes: update `capital-queue.md` with available capital and prompt review of Slot A/B/C candidates

---

## Drive Path

`PSX_Research/Portfolio/capital-queue.md`
