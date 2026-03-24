# UI Formats — Display Standards

Consistent output formats across all session types.
Apply these templates when presenting analysis to Noor.

---

## Session Header

Every session opens with:

```
═══════════════════════════════════════
PSX Investment Agent — [Session Type]
[Date]  |  KSE-100: [level]  |  Cash: [X]%
═══════════════════════════════════════
[Any Step 0 alerts — one line each]
```

---

## Portfolio Snapshot (Morning Briefing / Portfolio Review)

```
## Portfolio — [Date]

| Ticker | Stage | Weight | Entry Price | Current | P&L% | Thesis | Composite |
|--------|-------|--------|-------------|---------|------|--------|-----------|
| [TKR]  | OPEN  | [X]%   | PKR [X]     | PKR [X] | [X]% | INTACT | [X.X]     |

Cash: [X]%  |  Total Deployed: [X]%  |  Positions: [N]

[Alerts — one block per alert type]
```

---

## Position Record Card (OPEN Stage output)

```
## Position Opened — [TICKER]  [Date]

Entry Price:    PKR [X]       | Shares: [N]
Capital:        PKR [X]       | Weight: [X]%
Conviction:     [HIGH/MED/TRACKER]
Composite:      [X.X] / 10    | Thesis: v1 INTACT
CGT Cohort:     [1–4]         | Clock starts: [Date]

Drawdown Alerts:
  L1 Warn:      −[X]%  (PKR [X])
  L2 Review:    −[X]%  (PKR [X])
  L3 Exit Flag: −[X]%  (PKR [X])

Ex-Date (next): [Date or TBC]
Results Month:  [Month YYYY or TBC]

Drive saved: PSX_Research/Portfolio/portfolio-master.md ✓
```

---

## Thesis Integrity Card (HOLD Stage / Thesis Check)

```
## Thesis Check — [TICKER]  [Date]

Status: [INTACT / STRESSED / BROKEN / EVOLVED]
Version: v[N]  |  Last checked: [Date]

Thesis bullets:
  ✅ [Bullet 1] — still valid
  ✅ [Bullet 2] — still valid
  ⚠️ [Bullet 3] — under pressure: [reason]

Recommended action: [Hold / Review / Exit / Evolve thesis]
```

---

## Drawdown Alert Card

```
## Drawdown Alert — [TICKER]

Entry: PKR [X]  →  Current: PKR [X]  |  Drawdown: −[X]%
Alert Level: L[N] — [WARN / REVIEW / EXIT FLAG]

[Required action per level]
```

---

## Benchmark Performance Card

```
## Benchmark — [Month YYYY]

Monthly:  Portfolio [X]%  vs  KSE-100 [Y]%  |  Alpha: [Z]%
YTD:      Portfolio [X]%  vs  KSE-100 [Y]%
3M Alpha: [X]%  |  Beta: [X.X]  |  Win/Loss: [W]/[L] months

Top contributors:  [TICKER] +[X]%,  [TICKER] +[X]%
Top detractors:    [TICKER] −[X]%,  [TICKER] −[X]%
```

---

## Capital Queue Card

```
## Capital Deployment Queue — [Date]

Available cash: [X]%  |  Max deployable (5% floor): [X]%

| Slot | Ticker | Conviction | Composite | Signal | Size | Status |
|------|--------|-----------|-----------|--------|------|--------|
| A    | [TKR]  | HIGH      | [X.X]     | Stage 2| [X]% | Ready  |
| B    | [TKR]  | MED       | [X.X]     | Stage 2| [X]% | T+30 review [Date] |

[Cash floor warning if applicable]
```

---

## Decision Journal Entry Format

```
## Decision Log — [Date]  [TICKER]  [BUY/SELL/HOLD]

Price: PKR [X]  |  Shares: [N]  |  Weight: [X]%
Composite at decision: [X.X]
Market context: KSE-100 [level], SBP [X]%, PKR/USD [X]

Primary reason: [1–2 sentences]
Thesis: [3–5 sentences for BUY; outcome verdict for SELL]
Counter-argument: [1–3 sentences — mandatory]
Exit conditions: [list 2–3 for BUY/ADD]
Emotional state: [Analysis / News Reaction / Momentum Chasing / Fear / Conviction Add]

Outcome (post-exit): [filled after close]
Decision quality: [1–5 — process score, independent of outcome]
```

---

## Session Footer

Every session closes with:

```
───────────────────────────────────────
Saved:   [list of Drive files updated]
Next:    [any pending actions / T+30 reviews / upcoming alerts]
───────────────────────────────────────
```

---

## Alert Display Order in Morning Briefing

Always surface alerts in this priority order:
1. 🚨 BROKEN THESIS (blocks session — must resolve first)
2. 📉 DRAWDOWN L3 (blocks session — must resolve first)
3. 📉 DRAWDOWN L2 (flag before proceeding)
4. 📉 DRAWDOWN L1 (note and continue)
5. ⚠️ STALE RESEARCH / SCORES / MACRO
6. 🚨 TAX HARVEST window open
7. 📅 EARNINGS WINDOW upcoming
8. 💰 DIVIDEND EX-DATE upcoming
9. ⏰ WATCHLIST EXPIRY
10. ⚠️ CONCENTRATION breach
11. ✅ Capital queue slots ready
