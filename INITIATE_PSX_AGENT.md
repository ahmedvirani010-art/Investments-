# PSX Investment Agent — Intake Interview

Run this prompt at the start of a new session to configure the Agent for Noor Din's
specific portfolio, risk tolerance, and preferences. Answers are used when writing
SKILL.md thresholds and routing defaults.

---

## Instructions

Answer each question below. Leave a field blank only if it is genuinely not yet
decided — the Agent will use default values from the PRD for any blank fields.

---

## Section 1 — Portfolio Identity

1. **Full name / preferred name** for the Agent to address you by:
   > ___

2. **Active broker(s)** (e.g. Taurus, ISB Capital, JS Direct):
   > ___

3. **Total portfolio size** (approximate PKR, as of today):
   > ___

4. **Number of current open positions:**
   > ___

5. **Is this a fresh portfolio or an existing one being migrated?**
   (Fresh / Migrating existing / Partially migrated)
   > ___

---

## Section 2 — Risk & Sizing Preferences

6. **Maximum single-name concentration (% of portfolio):**
   Default = 20%. Override?
   > ___

7. **Maximum sector concentration (% of portfolio):**
   Default = 40%. Override?
   > ___

8. **Cash floor minimum (% always kept in cash):**
   Default = 5%. Override?
   > ___

9. **Conviction tier definitions — confirm or adjust:**
   - HIGH conviction: >15% weight  → ___
   - MED conviction:  8–15% weight → ___
   - TRACKER:         <8% weight   → ___

10. **Preferred minimum composite score before opening a new position:**
    Default = Slot A ≥ 7.0, Slot B ≥ 5.5. Override?
    > ___

---

## Section 3 — Tax & Filing Status

11. **Are you a registered tax filer (Active Filer)?**
    (Yes / No / In progress)
    > ___

12. **Do you use VPS (Voluntary Pension Scheme) for CGT sheltering?**
    (Yes / No / Planning to)
    > ___

13. **Target CGT annual limit awareness:**
    The Agent will track CGT exposure and flag proximity to thresholds.
    Any specific limit to watch for beyond the statutory Section 63 rules?
    > ___

---

## Section 4 — Income & Dividends

14. **Is dividend income a primary objective or secondary?**
    (Primary / Secondary / Indifferent)
    > ___

15. **Minimum net yield (after WHT) you require before a dividend is worth capturing:**
    Default = flag if portfolio yield spread vs. SBP rate < 1%.
    Override?
    > ___

---

## Section 5 — Review Cadence

16. **Preferred day for monthly review:**
    Default = last trading Friday of the month. Override?
    > ___

17. **Do you want the Agent to auto-prompt if no session in > 28 days?**
    (Yes / No)
    > ___

18. **Morning briefing preference:**
    - Full briefing (drawdown + dividends + capital queue) every session?
    - Brief mode (alerts only, no narrative)?
    > ___

---

## Section 6 — Sectors & Tickers In Scope

19. **List the PSX sectors you actively invest in (or are open to):**
    > ___

20. **List any tickers or sectors that are permanently excluded (e.g. ethical screens, liquidity, personal policy):**
    > ___

21. **Commodities of interest via PMEX:**
    (Gold / Oil / Cotton / Palm Oil / All / None)
    > ___

---

## Section 7 — Existing Skill Configuration

22. **Confirm all 9 skills are installed in your Claude.ai / Cowork environment:**
    - [ ] psx-investing-plugin
    - [ ] psx-portfolio-analysis
    - [ ] sector-analysis
    - [ ] psx-earnings-analyzer
    - [ ] psx-news-monitor
    - [ ] psx-valuation-screen
    - [ ] psx-rs-trend
    - [ ] psx-tax-harvester
    - [ ] PMEX Commodities

23. **Is Google Drive MCP connected and authenticated?**
    (Yes / No — if No, Drive persistence will be unavailable until connected)
    > ___

24. **Confirm the root Drive folder path for PSX research:**
    Default = `PSX_Research/`. Override?
    > ___

---

## Section 8 — Agent Persona Preferences

25. **Communication style preference:**
    (Concise / Detailed / Structured tables / Narrative prose)
    > ___

26. **When the Agent detects a BROKEN thesis, preferred default response:**
    - Hard stop — mandatory exit discussion before session continues
    - Soft flag — surface alert but allow session to proceed
    Default = Hard stop (per PRD hard rule).
    > ___

27. **Any additional instructions or preferences for the Agent?**
    > ___

---

## Completion

Once answered, share this file with Claude and say:
**"Initiate PSX Investment Agent with these settings."**

Claude will read your answers, configure SKILL.md thresholds, and confirm the
Agent is ready for its first session.
