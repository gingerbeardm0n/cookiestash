# Subscription Register

Last updated: 2026-09-16 (first audit)

Status values: `ACTIVE` (wanted) · `SUSPECT` (possibly unused) · `KILL` (decided,
not yet cancelled) · `CANCELLED` · `REFUND-PENDING`

## Open items

| Merchant | Amount | Cadence | Status | Notes |
|---|---|---|---|---|
| Meta / Oculus | unknown | unknown | **KILL** | Unused 6+ months. **No billing email ever sent to this address** — see below. Need line item from Rocket Money. |
| YouTube Premium | $17.15 | monthly | SUSPECT | Rocket Money flagged a price increase 2026-06-14. Was lower before. Confirm still wanted at new price. |
| Google Cloud Storage | unknown | monthly | SUSPECT | Renewal reminder 2026-05-25. Likely Google One photo storage. Check tier vs. actual usage. |
| Anthropic | unknown | monthly | ACTIVE | Receipts on the 3rd of each month. In use. |
| Amazon Subscribe & Save | varies | recurring | ACTIVE | DHM electrolyte auto-delivery added 2026-07-29. Gum subscription auto-cancelled 2026-09-15. Consumables, not a trap. |

## The Meta finding

Searched all of Gmail for `meta.com`, `oculus.com`, `facebookmail.com` billing
mail. Four hits, all Nov 2021 – Aug 2022, all about the Quest 2 hardware order.
**Zero subscription receipts, ever.**

Two consequences:

1. This is why it ran unnoticed. There was nothing in the inbox to notice.
2. Email scanning alone will never catch it. Only the Chase feed sees it.

It is also the strongest argument in a refund request: Meta charged a recurring
fee for six-plus months without sending a single renewal notice to the account
email on file.

**Blocked on:** exact merchant string, amount, and billing date from
Rocket Money → Recurring.

## Known accounts

- Chase Freedom Unlimited Visa (...5744) — primary card, autopay on
- Chase (...4421), Chase (...8639) — statements only, no line items in email
- US Bank Home Mortgage — large recurring, not a subscription
- Rocket Money — the sensor; its own fee is itself worth auditing

## Recurring-charge volume

Rocket Money's weekly "upcoming bills" emails report 1–4 recurring charges per
week. Over ~18 weeks that is a steady baseline; spikes are worth a look.
