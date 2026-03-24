# Module 12 — Google Drive Schema

Complete folder structure and file inventory. Load this when setting up or extending the Drive knowledge base.

---

## Full Structure

```
PSX_Research/
│
├── Portfolio/
│   ├── portfolio-master.md        ← All open positions (Module 01 position record fields)
│   ├── watchlist.md               ← Watchlist entries (Module 03)
│   ├── capital-queue.md           ← Deployment queue Slots A/B/C (Module 08)
│   ├── closed-positions.md        ← Exited positions archive (Module 01)
│   ├── benchmark.md               ← Monthly return table vs. KSE-100 (Module 07)
│   ├── scores-history.md          ← Composite score history — append only (existing)
│   └── trade-log.md               ← Chronological trade record (existing)
│
├── Thesis/
│   └── [TICKER]-thesis.md         ← Per-ticker thesis, all versions (Module 04)
│
├── Dividends/
│   └── calendar.md                ← Ex-dates, amounts, net yields (Module 05)
│
├── Earnings/
│   ├── calendar.md                ← Results month estimates per ticker (Module 09)
│   ├── previews/
│   │   └── [TICKER]_preview_[YYYY-MM].md
│   └── outcomes/
│       └── [TICKER]_outcome_[YYYY-MM].md
│
├── Journal/
│   ├── decision-log.md            ← Chronological journal (Module 10)
│   └── quarterly-audit-[Q]-[YYYY].md
│
├── Reviews/
│   └── monthly-[YYYY-MM].md       ← Monthly review outputs (Module 02)
│
├── Stocks/
│   └── [TICKER].md                ← Per-ticker research notes (existing)
│
├── Sectors/
│   └── [SECTOR].md                ← Sector analysis files (existing)
│
├── Macro/
│   └── macro-context.md           ← Rolling macro context (existing)
│
├── Commodities/
│   ├── [gold|oil|cotton|palm].md  ← Per-commodity research (PMEX skill)
│   └── commodity-macro.md         ← Master commodity context
│
└── Sessions/
    └── [YYYY-MM-DD]-session.md    ← Session summaries (existing)
```

---

## File Naming Conventions

| Pattern | Example |
|---------|---------|
| Monthly review | `monthly-2026-03.md` |
| Quarterly audit | `quarterly-audit-Q1-2026.md` |
| Earnings preview | `FFC_preview_2026-08.md` |
| Earnings outcome | `FFC_outcome_2026-08.md` |
| Ticker thesis | `FFC-thesis.md` |

---

## Write Rules
- `scores-history.md` and `decision-log.md` — **append only, never overwrite**
- Thesis files — **append new versions on top, preserve all prior versions**
- All other files — overwrite with latest, Drive version history provides rollback
