# Cancellation and Refund Playbooks

## How to ask for a refund

Refund requests succeed on specificity and restraint. Three things matter:

**Ask narrowly.** Request the last 1-2 unused billing cycles, not "everything
you've ever charged me". A small, clearly-justified ask lands inside what a
front-line agent can approve without escalating. A large one gets refused by
policy and ends the conversation.

**Lead with verifiable facts.** Exact dates, exact amounts, last date of actual
use. Agents have account records in front of them; matching their data builds
credibility instantly.

**Name the strongest lever you actually have**, in rough order of force:

1. *No renewal notice was ever sent.* Very strong. Several US states require
   advance notice for auto-renewals, and merchants know it.
2. *Zero usage across the period.* Strong and usually verifiable on their side.
3. *Cancellation was attempted and the flow failed.* Strong if true.
4. *Long-standing customer, first request.* Mild, but free to include.

Be courteous and non-accusatory. The agent didn't charge him and has discretion
they can choose not to exercise.

**Escalation.** If the first agent refuses, ask once for a supervisor or the
billing team — that's often where refund authority actually sits. If that also
fails, a card chargeback through Chase is the real backstop, but it can close
the merchant account. Mention it to Joel as a decision, never threaten it in
the chat.

## Meta / Oculus

**Open item. Unused 6+ months, marked KILL.**

Cancel at: `secure.oculus.com` → Settings → Subscriptions. Also check the Meta
Quest mobile app, since some subscriptions only surface there. Cancelling stops
renewal but does not refund the current period.

Meta's published stance: no refunds on subscription periods already consumed.
So the realistic ask is **cancel + refund the last 1-2 cycles**, not all six
months.

**Joel's strongest lever here is unusually good:** Meta has never sent a single
billing email to his address on file. Not one renewal notice in the entire
period. That is lever #1 above, and it is why the charge went unnoticed. Lead
with it.

Blocked on: exact merchant string, amount, and billing date from Rocket Money →
Recurring, or from a Chase CSV export. Don't draft a generic letter — the
argument differs for Quest+, Horizon, and in-app subscriptions. Get the line
item first.

## General patterns

**Apple / Google in-app subscriptions.** If the charge shows as `APPLE.COM/BILL`
or `GOOGLE *`, the merchant can't cancel it — the platform bills it. Apple:
Settings → Apple Account → Subscriptions. Google: Play Store → Subscriptions.
Apple's refund path is reportaproblem.apple.com and is often surprisingly
generous for unused services.

**Annual plans** are where the real money sits and where refund windows close
hard. Prioritize them.

**Retention offers.** Cancellation flows frequently counter with 50% off or a
free month. That's sometimes a genuinely good deal — surface it to Joel rather
than declining on his behalf. But if he doesn't use the service, a discount on
nothing is still nothing.

**Dark patterns.** Some merchants require phone or chat specifically because it
suppresses cancellations. Note when you hit one — it's useful evidence for a
chargeback and worth him knowing.

## Verify the cancellation actually worked

A cancellation isn't done until a charge fails to appear. Record the date in
`subscriptions.md` and check the following cycle. If it charges again, the
cancellation failed — that's a `KILL` item still billing and belongs at the top
of the next report under "Needs action". This happens more than people expect.
