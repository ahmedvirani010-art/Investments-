# Asset Allocation Skill — PSX Investment Agent

## Description

Activate this skill when the user mentions any of the following phrases (exact or paraphrased):
"total wealth", "asset allocation", "net worth review", "how much is in PSX",
"wealth snapshot", "update wealth", "allocation check", "am I over-exposed",
"pension allocation", "provident fund in allocation", "endowment allocation",
"wealth diversification", "risk budget", "how much in equities total",
"total portfolio value", "PSX vs total wealth", "true equity weight",
"wealth breakdown", "total financial picture"

**Do not confuse with `psx-portfolio-analysis`** (PSX-only view). This skill adds
all non-PSX asset classes — Provident Fund, Gratuity, Endowment Policies, VPS
Pension, Cash, Gold, Real Estate — to produce a complete total-wealth picture.

PRD reference: `13_ASSET_ALLOCATION.md`

---

## Step 0 — Session Start Staleness Check

Before any user request, check `PSX_Research/Portfolio/total-wealth.md` via `psx-investing-plugin`.

- If file does not exist → run **Full Intake** (Section 1 below)
- If last-updated date > 60 days ago → say:
  > "Your wealth snapshot is [X] days old (last: [date]). Run a quick update? It takes
  > 2 minutes and only needs the non-PSX values — PSX data auto-pulls from Drive."
- If last-updated < 60 days ago → load existing values and go directly to **Allocation Engine** (Section 3)

---

## Section 1 — Intake Interview

Run this interview when no snapshot exists or user explicitly says "full update" / "redo wealth intake".
PSX equities are auto-pulled — never ask the user for them.

---

### Step 1: PSX Equities (automatic — no user input)

```
→ Call psx-investing-plugin: read PSX_Research/Portfolio/portfolio-master.md
→ Sum all open positions at current market value (PKR)
→ Store as: PSX_TOTAL = [PKR value]
→ Confirm to user: "PSX portfolio: PKR X,XX,XXX — pulled from Drive."
```

---

### Step 2: Cash / Liquid

Ask:
> "What is your approximate total cash balance across all bank accounts (current +
> savings + any digital wallets)? Give a round PKR figure."

Store as: `CASH_TOTAL`

---

### Step 3: Gold & Commodities

Ask:
> "Do you hold physical gold (in tolas) or any PMEX open positions?
> (a) Physical gold: how many tolas?
> (b) PMEX positions: current PKR value of open contracts?
> (c) Any other commodity holdings (silver, cotton, etc.)?"

If user gives gold in tolas:
```
→ Call PMEX Commodities skill: get live PKR price per tola
→ Auto-compute: GOLD_PKR = tolas × live_price_per_tola
→ Confirm: "Gold: [X] tolas × PKR [Y]/tola = PKR [Z]"
```

Store as: `GOLD_COMMODITIES_TOTAL`

---

### Step 4: VPS / Voluntary Pension

Ask:
> "Do you have a VPS (Voluntary Pension System) account?
> If yes:
> (a) Current account balance (PKR)?
> (b) Your annual contribution (PKR)?
> (c) Any employer contribution (PKR/year)?"

If VPS exists, also compute:
```
→ Section 63 deduction available = lower of PKR 500,000 or 20% of taxable income
→ Show remaining deduction headroom vs current contribution
→ NOTE: "Always verify current Section 63 limit at FBR before acting on this."
```

Store as: `VPS_TOTAL`, `VPS_ANNUAL_CONTRIBUTION`

---

### Step 5: Endowment Policies (repeat for each policy)

Ask:
> "Do you have any endowment / life insurance savings policies?
> For each policy, I need:
> (a) Insurer name
> (b) Sum assured (PKR)
> (c) Current surrender value (PKR) — check your latest policy statement
> (d) Maturity value (PKR) — the guaranteed amount at maturity
> (e) Maturity date
> Any more policies? (Y/N)"

Store each policy. In the snapshot, use **surrender value** for current net worth
(not maturity value — maturity value is a future projection, not today's worth).

Important rules:
- Surrender value ≠ maturity value. Never conflate them.
- No CGT on maturity proceeds. No CGT on death benefit.
- Flag if any policy matures within 12 months → prompt user to plan redeployment.

Store as: `ENDOWMENT_SURRENDER_TOTAL`, list of individual policies

---

### Step 6: Provident Fund

Ask:
> "Tell me about your Provident Fund:
> (a) Your employee contribution balance (PKR total accumulated)?
> (b) Employer contribution balance (PKR total accumulated)?
> (c) Years of service?
> (d) Is this a Government Provident Fund (GPF) or a private/company PF?"

Auto-flag if applicable:
```
→ If user's annual voluntary PF contribution > 1/3 of stated basic salary:
   FLAG: "Your PF contribution may exceed the exempt threshold.
   Excess is taxable income. Verify with FBR / your HR."
```

Store as: `PF_EMPLOYEE_BALANCE`, `PF_EMPLOYER_BALANCE`, `PF_TOTAL`

---

### Step 7: Gratuity Entitlement

Ask:
> "For your gratuity estimate:
> (a) Your current basic salary (PKR/month)?
> (b) Years of completed service?"

Auto-compute:
```
GRATUITY_ESTIMATE = basic_salary_monthly × years_of_service

→ Display: "Estimated gratuity: PKR [X]"
→ Always append: "(This is an estimate. Actual entitlement depends on your
   employer's gratuity scheme rules and may differ.)"
```

Tax note (always with FBR disclaimer):
```
→ "Gratuity is exempt from tax up to 1 month's last basic salary × years of service
   under GPF rules. Amount above this threshold is taxable. Verify at FBR before any
   tax planning on this figure."
```

Store as: `GRATUITY_ESTIMATE`

---

### Step 8: Real Estate (Optional)

Ask:
> "Do you own real estate (residential, commercial, or plot)?
> If yes, what is your best estimated PKR market value?
> (This will be clearly marked as an estimate in your snapshot.)"

If user declines: skip. Store as 0.

Store as: `REAL_ESTATE_ESTIMATE` (always labeled "ESTIMATE" in all outputs)

---

### Step 9: Other Instruments

Ask:
> "Any other financial instruments?
> — NSS certificates (Behbood, Special Savings, etc.)
> — Prize bonds
> — Defence Savings Certificates
> — Any other"

For each: name + current PKR value.

Store as: `OTHER_TOTAL`, with itemized list

---

## Section 2 — Total Wealth Computation

After intake (or after loading existing snapshot), compute:

```
TOTAL_NET_WORTH = PSX_TOTAL + CASH_TOTAL + GOLD_COMMODITIES_TOTAL
                + VPS_TOTAL + ENDOWMENT_SURRENDER_TOTAL
                + PF_TOTAL + GRATUITY_ESTIMATE
                + REAL_ESTATE_ESTIMATE + OTHER_TOTAL

PSX_WEIGHT_PCT       = PSX_TOTAL / TOTAL_NET_WORTH × 100
RISK_ASSET_PCT       = (PSX_TOTAL + GOLD_COMMODITIES_TOTAL + REAL_ESTATE_ESTIMATE)
                       / TOTAL_NET_WORTH × 100
FIXED_INCOME_EQ_PCT  = (PF_TOTAL + ENDOWMENT_SURRENDER_TOTAL + VPS_TOTAL + OTHER_TOTAL)
                       / TOTAL_NET_WORTH × 100
LIQUIDITY_RATIO      = (PSX_TOTAL + CASH_TOTAL + GOLD_COMMODITIES_TOTAL)
                       / TOTAL_NET_WORTH × 100

TIER_1_TOTAL = PSX_TOTAL + CASH_TOTAL + GOLD_COMMODITIES_TOTAL
TIER_2_TOTAL = VPS_TOTAL + OTHER_TOTAL
TIER_3_TOTAL = ENDOWMENT_SURRENDER_TOTAL + PF_TOTAL + GRATUITY_ESTIMATE + REAL_ESTATE_ESTIMATE
```

---

## Section 3 — Alert Flags

Evaluate all flags before generating output:

| Flag | Condition | Severity |
|------|-----------|----------|
| EQUITY CONCENTRATION | PSX > 60% of TIER_1_TOTAL | MEDIUM |
| HIGH RISK EXPOSURE | RISK_ASSET_PCT > 70% | HIGH |
| LIQUIDITY WARNING | LIQUIDITY_RATIO < 10% | HIGH |
| FIXED INCOME LIGHT | FIXED_INCOME_EQ_PCT < 20% (age < 50) or < 35% (age ≥ 50) | MEDIUM |
| ENDOWMENT MATURING SOON | Any policy matures within 12 months | ACTION NEEDED |
| PF CONTRIBUTION OVERRUN | Annual voluntary PF contribution > 1/3 of basic salary | TAX RISK |
| VPS UNDER-UTILIZED | Annual VPS contribution < Section 63 limit | OPPORTUNITY |
| ILLIQUID HEAVY | TIER_3_TOTAL > 60% of TOTAL_NET_WORTH | MEDIUM |

---

## Section 4 — Output Format

Generate this fixed-structure report (~400–600 words). Do not deviate from section order.

```
## TOTAL WEALTH SNAPSHOT — [Date]

### Asset Allocation Table
| Asset Class | PKR Value | % of Net Worth | Liquidity Tier |
|-------------|-----------|----------------|----------------|
| PSX Equities | X,XX,XXX | X.X% | Tier 1 — Liquid |
| Cash / Liquid | X,XX,XXX | X.X% | Tier 1 — Liquid |
| Gold / Commodities | X,XX,XXX | X.X% | Tier 1 — Liquid |
| VPS / Pension | X,XX,XXX | X.X% | Tier 2 — Semi-liquid |
| NSS / Other | X,XX,XXX | X.X% | Tier 2 — Semi-liquid |
| Endowment Policies | X,XX,XXX | X.X% | Tier 3 — Illiquid |
| Provident Fund | X,XX,XXX | X.X% | Tier 3 — Illiquid |
| Gratuity (est.) | X,XX,XXX | X.X% | Tier 3 — Illiquid |
| Real Estate (est.) | X,XX,XXX | X.X% | Tier 3 — Illiquid |
| **TOTAL NET WORTH** | **X,XX,XXX** | **100%** | |

### Key Metrics
- **Risk Assets (PSX + Gold + RE):** X.X% of total wealth
- **Fixed Income Equivalent (PF + Endowment + VPS + NSS):** X.X% of total wealth
- **Liquidity Ratio (Tier 1):** X.X% of total wealth
- **PSX True Weight:** X.X% of total wealth
  _(vs. X.X% if measured within PSX portfolio only)_

### Liquidity Profile
- Tier 1 (Liquid): PKR X,XX,XXX (X.X%)
- Tier 2 (Semi-liquid): PKR X,XX,XXX (X.X%)
- Tier 3 (Illiquid): PKR X,XX,XXX (X.X%)

### PSX Context
"Your PSX equity exposure is [X%] of total wealth. Your provident fund and
endowment represent [X%] in fixed-income equivalent instruments. Your effective
risk asset ratio is [X%] of total net worth — [assessment: conservative / balanced / aggressive]."

### Flags & Alerts
[List each triggered flag from Section 3 with one-line action]

### Tax Considerations
[VPS Section 63 deduction headroom, PF threshold flag if triggered, gratuity
 exemption estimate]
⚠️ All tax figures are estimates. Verify current rates and limits at FBR before acting.

### 3 Priority Actions
1. [Most important rebalancing or optimization action]
2. [Second action]
3. [Third action]
```

---

## Section 5 — Drive Persistence

After generating the report:

```
→ Ask: "Save this snapshot to Drive? (Y to confirm)"
→ If confirmed:
   (a) Write full snapshot to PSX_Research/Portfolio/total-wealth.md
       (overwrite — Drive version history is rollback)
   (b) Append one history row to PSX_Research/Portfolio/total-wealth-history.md:
       | [Date] | PKR [Total] | PSX [X%] | Risk [X%] | Fixed Inc Eq [X%] | Liquidity [X%] |
   (c) Confirm: "Saved to Drive."
```

---

## Section 6 — Monthly Review Integration

At the end of every Monthly Review (after the 7-step sequence in Module 02), add:

> "**Step 8 (Optional) — Wealth Snapshot Update**
> Your total wealth snapshot was last updated on [date] ([X] days ago).
> PSX values have been updated — would you like to refresh non-PSX values too?
> (Takes 2 minutes. Keeps your true equity weight calibrated.)"

If user says yes → run intake for Steps 2–9 only (skip PSX auto-pull, which already updated).
If user declines → log "Wealth snapshot not updated this cycle" in session summary.

---

## Hard Rules

1. **Never hardcode** VPS Section 63 limit, PF exemption threshold, or gratuity tax
   limit. Always fetch from FBR and display the FBR disclaimer.
2. **Gratuity and PF are estimates.** Always label them as such. Actual entitlement
   depends on employer scheme rules, separation terms, and applicable law.
3. **Surrender value ≠ maturity value.** Use surrender value for current net worth.
   Show maturity value separately as a future projection.
4. **PSX values come from Drive only.** Never ask user to re-enter PSX positions.
5. **No trade execution.** All recommendations require explicit user confirmation.
6. **Real estate is always labeled ESTIMATE.** Never present it as a verified valuation.
