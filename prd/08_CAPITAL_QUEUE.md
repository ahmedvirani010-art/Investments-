# Module 08 — Capital Deployment Queue

Undeployed cash is a portfolio position. Prevents idle cash and impulsive deployment via conviction-tiered, condition-based staging.

---

## Queue Structure

| Slot | Source | Entry Condition | Sizing Rule |
|------|--------|----------------|-------------|
| Slot A — HIGH conviction | Watchlist HIGH tier | All entry conditions met + composite ≥ 7.0 + RS Stage 2 or early Stage 3 | Full target weight — single tranche |
| Slot B — MED conviction (staged) | Watchlist MED tier | Entry conditions met + composite 5.5–6.9 + entry within 5% of target | 50% at entry, 50% at T+30 confirmation |
| Slot C — Opportunistic | Event rescore: market overreaction | Composite jumped ≥ 1.0 due to one-off event (news, earnings miss) | 1 tranche = 50% of target; review at T+30 |
| Cash Floor | Always maintained | Portfolio cash always ≥ 5% | Non-negotiable. Breach requires explicit user acknowledgment. |

---

## Agent Logic

- Queue checked at start of every morning briefing: any slots ready to deploy?
- When a watchlist stock meets entry conditions → auto-populate appropriate Slot
- Cash floor breach: Agent flags and requests explicit override acknowledgment
- Slot B T+30: Agent tracks entry date and prompts second tranche decision review

---

## Drive Path
`PSX_Research/Portfolio/capital-queue.md`
