# Investment Thesis Tracker — Module 04

Records and monitors the original reason a position exists.
Positions are held for the right reason, not inertia.

---

## Triggers

Load this file when the user says:
- "thesis update", "thesis integrity", "check thesis", "thesis check", "rescore thesis"

Also invoked during:
- Monthly Review Step 4 (thesis integrity check)
- HOLD STAGE — any scheduled or event-triggered thesis reassessment

---

## Pre-Flight: Pull Drive Context

Before running any thesis check, call `psx-investing-plugin` to pull:
- `PSX_Research/Thesis/[TICKER]-thesis.md` — all thesis versions for the ticker
- `PSX_Research/Portfolio/portfolio-master.md` — current thesis status per holding

---

## 4-Status Framework

| Status | Definition | Agent Action |
|--------|-----------|--------------|
| INTACT | All key assumptions valid. Catalyst pending or playing out. | No change. Monitor at next monthly review. |
| STRESSED | One or two assumptions weakened but core case intact. | Flag for review. Consider trimming position. Check Factor 6 (Macro Alignment) in composite score. |
| BROKEN | Central thesis assumption invalidated. Catalyst won't materialise or already captured. | **Mandatory exit flag.** Invoke Broken Thesis Protocol (SKILL.md). Run `psx-tax-harvester` for CGT. Log in Decision Journal. No "hold and hope" without explicit documented override. |
| EVOLVED | Thesis changed — not broken, but holding rationale materially different from entry. | Write Thesis v2. Record exactly what changed vs. v1. Treat as fresh hold decision at current composite score. |

---

## Running a Thesis Integrity Check

For each ticker being reviewed:

1. Pull thesis file from Drive (`PSX_Research/Thesis/[TICKER]-thesis.md`)
2. Read the active thesis version (v1 or latest)
3. Evaluate each thesis bullet against current reality:
   - Is the core growth/value driver still intact?
   - Have earnings surprised positively or negatively since thesis was written?
   - Has sector dynamics shifted against the thesis?
   - Any management changes, regulatory risk, or structural threats emerged?
4. Call `sector-analysis` if thesis is in question
5. Call `psx-earnings-analyzer` if results were released in the past 30 days
6. Assign status using the 4-status framework above
7. Update `portfolio-master.md` with new Thesis Status + date

---

## EVOLVED Thesis Protocol

When a position is marked EVOLVED:

1. Flag: "📝 EVOLVED THESIS: [TICKER] — rationale has materially changed from v[N]. Writing Thesis v[N+1]."
2. Draft Thesis v[N+1]:
   - What has changed from the prior version
   - What the new holding rationale is
   - Updated catalyst and exit conditions
3. Record the delta explicitly: "Changed from: [old assumption] → Changed to: [new assumption]"
4. Treat as a fresh hold decision: re-run composite score via `psx-portfolio-analysis`
5. User must confirm the hold continues under the new thesis — no auto-continuation
6. Save new thesis version to Drive (newest on top, old version preserved below)

---

## Version Control Rules

- Any material change to investment rationale → increment version (v1 → v2 → v3...)
- All versions preserved in `PSX_Research/Thesis/[TICKER]-thesis.md` — old versions never overwritten
- Append new version at the top of the file; old versions remain below with their original date
- Agent compares v1 assumptions vs. current reality at every Monthly Review
- **Auto-suggest EVOLVED** when 3 or more assumptions from v1 have changed — flag: "⚠️ 3+ original assumptions have shifted for [TICKER]. Consider marking EVOLVED and writing Thesis v2."

---

## Thesis File Format (per version block)

```
## Thesis v[N] — [DD-MMM-YYYY]

**Status:** INTACT / STRESSED / BROKEN / EVOLVED
**Composite Score at writing:** [X.X] ([DD-MMM-YYYY])

### Investment Case (3–5 bullets)
- ...

### Key Catalyst
...

### Exit Conditions
...

### Risks / Thesis Invalidators
...

### Change from Prior Version (if v2+)
Changed: [what changed]
Reason: [why the thesis evolved]
```

---

## Drive Path

`PSX_Research/Thesis/[TICKER]-thesis.md` — one file per ticker, all versions appended newest-first
