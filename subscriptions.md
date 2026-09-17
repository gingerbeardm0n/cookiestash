# Subscription Register

Last updated: 2026-09-17

Status values: `ACTIVE` (wanted) · `SUSPECT` (possibly unused) · `KILL` (decided,
not yet cancelled) · `CANCELLED` · `REFUND-PENDING`

## Open items

| Merchant | Amount | Cadence | Status | Notes |
|---|---|---|---|---|
| Meta / Oculus (A) | $10.79 | monthly (~14th) | **KILL** | Confirmed via Chase mobile app 2026-09-17. Descriptor `OCULUS *<token>`, card ...5744, category Entertainment/Digital games. Most recent: Sep 14, 2026, ref 24692166257400785163241. **No billing email ever sent to this address** — see below. |
| Meta / Oculus (B) | $8.63 | monthly (~28th) | **KILL** | Second, separate Oculus line item — different amount/cycle day than (A), same generic descriptor. Confirmed 2026-09-17. Most recent: Aug 28, 2026, ref 24692166240404432711774. Same no-email finding applies. |
| YouTube Premium | $17.15 (was $15.00) | monthly | SUSPECT | Confirmed via full thread (2026-06-14): increased $15.00 → $17.15 June 13. Still want it at the new price? |
| Coinbase One | $4.99 | monthly | SUSPECT | New to the register — surfaced in 2026-09-13 "upcoming bills" email, charges again 2026-09-14. Not previously tracked. Still using it? |
| Anthropic | unknown | monthly | ACTIVE | Receipts on the 3rd of each month. In use. |
| Amazon Subscribe & Save | varies | recurring | ACTIVE | DHM electrolyte auto-delivery added 2026-07-29. Gum subscription auto-cancelled 2026-09-15. Consumables, not a trap. |
| Google Cloud Storage | $21.44 | **annual** (not monthly) | ACTIVE | Corrected 2026-09-17: full thread showed $21.44/yr (~$1.79/mo), not monthly as previously logged. Too small to be worth cancellation friction either way — downgraded off the decision list. |

## Not subscriptions (seen in Rocket Money mail, correctly out of scope)

- Ameriprise investment auto-contribution, $625.00 — recurring ACH debit ("AEIS DEBIT PPD..."), flagged by both the 2026-09-16 large-transaction alert and the 2026-09-13 upcoming-bills email. Investment, not a subscription.
- American Electric Power, $361.05 — electric utility, charges 2026-09-19.

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

**Unblocked 2026-09-17.** Line items pulled from Joel's Chase mobile app
transaction history (not Rocket Money — no CSV export was available; Chase
directly had what was needed). Turns out to be **two** separate recurring
Oculus charges under one generic descriptor, not one — see table above. Both
show the descriptor pattern `OCULUS *<random-token>`, always card ...5744,
category Entertainment / Digital games, method "Online, mail or phone". The
token changes every charge so it can't be used to distinguish Quest+ from
Horizon from in-app — Meta just doesn't expose that at the card-network level.
Next: cancel both via secure.oculus.com (can't be automated — web-only,
see cancellation-playbooks.md), then pursue refund on last 1-2 cycles each.

## Known accounts

- Chase Freedom Unlimited Visa (...5744) — primary card, autopay on
- Chase (...4421), Chase (...8639) — statements only, no line items in email
- US Bank Home Mortgage — large recurring, not a subscription
- Rocket Money — the sensor; its own fee is itself worth auditing

## Recurring-charge volume

Rocket Money's weekly "upcoming bills" emails report 1–4 recurring charges per
week. Over ~18 weeks that is a steady baseline; spikes are worth a look.
