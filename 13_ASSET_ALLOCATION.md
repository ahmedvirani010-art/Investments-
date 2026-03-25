# Module 13 — Asset Allocation & Total Wealth View

**Purpose:** Give a holistic picture of total net worth across all asset classes so that
PSX equity weight is understood in its true context — not in isolation. A user whose
provident fund is 100% fixed income is under-weight equities even if their PSX portfolio
looks concentrated. This module corrects that distortion.

---

## Triggers

- User says: "total wealth", "asset allocation", "how much of my wealth is in PSX",
  "update wealth snapshot", "wealth review", "allocation check", "am I over-exposed",
  "pension allocation", "provident fund allocation", "endowment allocation",
  "wealth diversification", "risk budget", "total portfolio value", "PSX vs total wealth"
- **Auto-prompt at Monthly Review (Step 8 — optional):** "Update non-PSX asset values?"
- **Staleness alert:** if `total-wealth.md` last updated >60 days ago → flag at session start

---

## Asset Class Data Model

| Asset Class | Key Sub-fields | Liquidity Tier | Source |
|-------------|---------------|----------------|--------|
| PSX Equities | Total PKR value | Tier 1 — Liquid | Auto-pulled from `portfolio-master.md` |
| Cash / Liquid | Total PKR across all bank accounts | Tier 1 — Liquid | User-entered |
| Gold / Commodities | Tolas (physical) + PMEX contract value | Tier 1 — Liquid | PMEX Commodities skill (live price) |
| VPS / Pension | Account balance, annual contribution, employer match | Tier 2 — Semi-liquid | User-entered |
| NSS / Prize Bonds | Description + PKR value | Tier 2 — Semi-liquid | User-entered |
| Endowment Policy | Insurer, sum assured, surrender value, maturity value, maturity date | Tier 3 — Illiquid | User-entered (may be multiple policies) |
| Provident Fund | Employee balance, employer balance, years of service, fund type | Tier 3 — Illiquid | User-entered |
| Gratuity Entitlement | Last basic salary, years of service → auto-computed | Tier 3 — Illiquid | Auto-computed estimate |
| Real Estate | Estimated PKR value (optional) | Tier 3 — Illiquid | User-entered; always marked as estimate |

---

## Liquidity Tier Definitions

| Tier | Accessibility | Included Assets |
|------|--------------|-----------------|
| **Tier 1 — Liquid** | Within 3 days, no penalty | PSX equities, Cash, Gold/PMEX |
| **Tier 2 — Semi-liquid** | Within 90 days, penalty or tax cost applies | VPS/Pension, NSS, Prize Bonds |
| **Tier 3 — Illiquid** | Only on life event: separation, maturity, death | Endowment, Provident Fund, Gratuity, Real Estate |

---

## Computation Rules

1. **Total Net Worth** = sum of all asset classes at current PKR values
2. **PSX Equity %** = PSX portfolio value ÷ Total Net Worth × 100
3. **Risk Asset %** = (PSX + Gold/Commodities + Real Estate) ÷ Total Net Worth × 100
4. **Fixed Income Equivalent %** = (PF + Endowment surrender value + VPS + NSS) ÷ Total Net Worth × 100
5. **Liquidity Ratio** = Tier 1 assets ÷ Total Net Worth × 100
6. **Gratuity auto-estimate** = Last basic salary (PKR/month) × years of service

---

## Alert Flags

| Flag | Condition | Response |
|------|-----------|----------|
| EQUITY CONCENTRATION | PSX > 60% of Tier 1 assets | Flag; suggest diversification to Tier 2 |
| HIGH RISK EXPOSURE | Risk assets > 70% of total net worth | Flag; review against risk tolerance |
| LIQUIDITY WARNING | Tier 1 < 10% of total net worth | Flag; ensure emergency fund adequacy |
| FIXED INCOME LIGHT | Fixed income equivalent < 20% of total wealth (ex-illiquid) | Flag; review against age/life stage |
| OVER-CONCENTRATED ILLIQUID | Tier 3 > 60% of total net worth | Flag; note limited flexibility |

---

## Pakistan-Specific Rules

> **Rule: Never hardcode any rate or limit. Always search FBR before citing.**

| Rule | Detail |
|------|--------|
| VPS Section 63 deduction | Lower of: PKR 500,000 or 20% of taxable income. Verify current limit via FBR search before stating. |
| PF voluntary contributions | Employer contributions fully exempt; employee voluntary contributions taxable above 1/3 of basic salary per year. Flag if threshold exceeded. |
| Gratuity tax exemption | Exempt up to 1 month's last basic salary × years of service (Government Provident Fund rules). Amount above exempt limit is taxable income. Always verify via FBR search. |
| Endowment maturity proceeds | No CGT; fully exempt. Death benefit is also exempt. Do not confuse surrender value with maturity value — track both. |
| PMEX gold pricing | Cross-reference PMEX Commodities skill for live PKR/tola rate before computing gold PKR value. |

---

## Drive Paths

| File | Write Rule |
|------|-----------|
| `PSX_Research/Portfolio/total-wealth.md` | Overwrite each update. Drive version history = rollback. |
| `PSX_Research/Portfolio/total-wealth-history.md` | **Append-only.** One row per update — date, total net worth PKR, PSX %, risk %, liquidity ratio. Mirrors benchmark.md pattern. |
