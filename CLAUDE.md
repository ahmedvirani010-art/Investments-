# CLAUDE.md — PSX Investment Agent

## What This Project Is

You are building the **PSX & Commodities Investment Agent** — an orchestration layer
that coordinates Noor Din's existing PSX skill ecosystem into a unified investment
co-pilot. The Agent manages the full position lifecycle, runs structured monthly
reviews, and persists all research to Google Drive.

**This is a skill-writing project, not an application.** The deliverable is a
`SKILL.md` file (and supporting reference files) that Claude reads at runtime to
know how to behave as an investment agent.

---

## Project Structure

```
psx-investment-agent/
├── CLAUDE.md                          ← you are here
├── INITIATE_PSX_AGENT.md              ← VS Code initiation prompt
│
├── prd/                               ← feature-wise PRD modules (load as needed)
│   ├── 00_INDEX.md                    ← always read this first
│   ├── 01_LIFECYCLE.md
│   ├── 02_MONTHLY_REVIEW.md
│   ├── 03_WATCHLIST.md
│   ├── 04_THESIS_TRACKER.md
│   ├── 05_DIVIDEND_CALENDAR.md
│   ├── 06_DRAWDOWN.md
│   ├── 07_BENCHMARK.md
│   ├── 08_CAPITAL_QUEUE.md
│   ├── 09_EARNINGS_CALENDAR.md
│   ├── 10_DECISION_JOURNAL.md
│   ├── 11_ROUTING_AND_ALERTS.md
│   └── 12_DRIVE_SCHEMA.md
│
├── skills/
│   └── psx-investment-agent/
│       ├── SKILL.md                   ← primary deliverable
│       └── references/
│           ├── routing-logic.md
│           ├── alert-thresholds.md
│           ├── ui-formats.md
│           └── skill-map.md
│
└── drive-schema/                      ← Drive file templates
    ├── portfolio-master.md
    ├── watchlist.md
    ├── capital-queue.md
    ├── closed-positions.md
    ├── benchmark.md
    ├── dividend-calendar.md
    ├── earnings-calendar.md
    ├── decision-log.md
    ├── macro-context.md
    └── templates/
        ├── ticker-thesis-template.md
        ├── monthly-review-template.md
        ├── quarterly-audit-template.md
        ├── earnings-preview-template.md
        └── earnings-outcome-template.md
```

---

## How to Work on This Project

### Starting a session

1. Read `prd/00_INDEX.md` first — it's 38 lines and gives you the full map
2. Load only the PRD module(s) relevant to today's task (see table in `00_INDEX.md`)
3. Do not load the full PRD v2 docx — it will clog context unnecessarily

### Which PRD module to load

| Task | Load |
|------|------|
| Writing the SKILL.md routing table | `11_ROUTING_AND_ALERTS.md` |
| Writing position lifecycle logic | `01_LIFECYCLE.md` |
| Writing monthly review logic | `02_MONTHLY_REVIEW.md` |
| Writing watchlist logic | `03_WATCHLIST.md` + `04_THESIS_TRACKER.md` |
| Writing risk/alert logic | `06_DRAWDOWN.md` + `07_BENCHMARK.md` |
| Writing income tracking | `05_DIVIDEND_CALENDAR.md` + `09_EARNINGS_CALENDAR.md` |
| Writing capital deployment | `08_CAPITAL_QUEUE.md` |
| Writing the decision journal | `10_DECISION_JOURNAL.md` |
| Setting up Drive templates | `12_DRIVE_SCHEMA.md` |

---

## Hard Rules — Never Violate

1. **Never modify existing skill files.** The 9 PSX skills listed below are used
   as-is. The Agent calls them — it does not edit them.

2. **No automated trade execution.** Every buy/sell recommendation requires
   explicit human confirmation before acting.

3. **Tax rates are always fetched live.** Never hardcode CGT rates, WHT rates,
   or Section 63 limits. Always search FBR before any tax computation.

4. **Drive files are the source of truth.** Always pull relevant Drive context
   before generating analysis. Always offer to save after generating.

5. **BROKEN thesis = mandatory exit decision.** The Agent does not accept
   "hold and hope" without an explicit Decision Journal entry documenting
   the override reasoning.

6. **5% cash floor is non-negotiable.** Deployment below this threshold requires
   explicit user acknowledgment — Agent flags it, user must confirm.

---

## Existing Skills — Orchestrate Only

These are installed in the Claude.ai / Cowork environment. Reference them by name
in the SKILL.md. Do not rewrite their logic.

| Skill | Primary Function |
|-------|-----------------|
| `psx-investing-plugin` | Drive persistence, session memory |
| `psx-portfolio-analysis` | 7-factor composite scoring, concentration, rebalancing |
| `sector-analysis` | Sector/ticker deep dives, driver frameworks, valuation |
| `psx-earnings-analyzer` | Results normalization, EPS surprise, forward EPS, PREVIEW mode |
| `psx-news-monitor` | News-to-ticker impact mapping, macro event routing |
| `psx-valuation-screen` | Cheapness check, yield spread, GGM, buy/hold/avoid signal |
| `psx-rs-trend` | Momentum, RS rank, Weinstein Stage, sector rotation |
| `psx-tax-harvester` | CGT, loss harvest, VPS pension, year-end plan |
| `PMEX Commodities` | Gold, oil, cotton, palm oil — anchored to US/China macro |

---

## Key Design Decisions

**Why a SKILL.md and not an app?**
The Agent runs inside Claude.ai/Cowork at conversation time. A SKILL.md is the
correct format — it loads into Claude's context and instructs it how to behave.
No server, no API, no deployment pipeline needed.

**Why modular PRD files?**
The full PRD is ~1,100 lines. Loading it entirely clogs Claude's context window
for every session. The 12 module files average ~40 lines each — load only what's
relevant to the current build task.

**Why Google Drive for persistence?**
Claude has no memory between sessions. Drive files are the persistent knowledge
base. The `psx-investing-plugin` skill already handles the read/write protocol —
the Agent builds on top of it rather than reinventing it.

**Why is the SKILL.md description "pushy"?**
Per the skill-creator best practices, skill descriptions must be explicit about
when to trigger. The Agent description lists all 17 session type trigger phrases
so Claude routes correctly without hesitation.

---

## Build Order (first-time setup)

1. Complete intake interview (`INITIATE_PSX_AGENT.md`) — answers determine
   which skills are included and what thresholds are set
2. Write `skills/psx-investment-agent/SKILL.md` — core routing and module logic
3. Write `skills/psx-investment-agent/references/` — routing-logic, alert-thresholds,
   ui-formats, skill-map
4. Create `drive-schema/` templates — one file per Drive path in `12_DRIVE_SCHEMA.md`
5. Validate all 17 session types with test trigger phrases

---

## Runtime Environment

- **Build environment:** VS Code with Claude Code extension
- **Runtime environment:** Claude.ai web / Claude Cowork
- **Persistence:** Google Drive via Google Drive MCP (when connected)
- **Data:** Web search + S&P Global MCP for live prices and news
- **No local database, no backend, no deployment**
