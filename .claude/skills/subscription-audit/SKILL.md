---
name: subscription-audit
description: Audit recurring charges and subscriptions to find money being wasted on unused services, then draft cancellation and refund requests. Use this whenever Joel asks about subscriptions, recurring charges, wasted money, what he's paying for, cancelling something, getting a refund, reviewing his spending, or checking his bank/credit card activity for things he forgot about — and also when he mentions a specific merchant he thinks he's still being billed by, or hands over a bank statement, CSV export, or Rocket Money email. Trigger it even if he doesn't say the word "subscription" — "am I still paying for X", "what's hitting my card", "I never use this anymore", and "help me cancel" all mean this skill.
---

# Subscription Audit

Find recurring charges Joel isn't getting value from, and turn each one into a
completed cancellation — ideally with a refund.

## Why this exists

Joel already has Rocket Money connected to his Chase accounts, and it already
emails him alerts. The charges are not hidden. The failure mode is that **201
alert emails arrived in 180 days and nearly all went unread** — a Meta/Oculus
subscription ran 6+ months unnoticed despite that.

So the bottleneck is not detection. It is triage and follow-through. Optimize
for *decisions made and cancellations completed*, not for coverage of things
he already knows about. A report that lists every subscription he's happy with
is a report he won't read, and you'll have recreated the exact problem.

## State lives in the repo

Read `subscriptions.md` at the repo root first, every time. Sessions are
ephemeral; that file is the only memory between runs. Update and commit it at
the end, or the next run starts blind and re-asks questions he already answered.

Status values: `ACTIVE` (wanted) · `SUSPECT` (possibly unused) · `KILL`
(decided, not yet cancelled) · `CANCELLED` · `REFUND-PENDING`

## Step 1 — Pick your data source

Check what's actually available rather than assuming. See
`references/data-sources.md` for the details of each. In short:

- **Gmail** — works right now, no setup. Rocket Money alerts plus merchant
  receipts. Fastest start, but **blind to any merchant that doesn't email**,
  which is exactly how the Meta charge survived.
- **A Chase CSV/QFX export** — if he's provided one, or can. This is the only
  source that sees *everything*, including silent merchants. Run
  `scripts/find_recurring.py` on it.
- **A Plaid MCP server** — if `mcp__plaid__*` tools exist in the session, use
  them; that's the automated version of the CSV.

If you only have Gmail, say so in the report and name what you might be missing.
Quietly producing a partial audit while sounding complete is the worst outcome
here, because it manufactures false confidence.

## Step 2 — Find the recurring charges

With a CSV, run the script — don't eyeball it:

    python3 scripts/find_recurring.py <path-to-csv>

It normalizes merchant names, groups by merchant, and reports repeating charges
with their cadence and amount drift. Amount drift matters: a price that moved
is a decision point even for a service he wants.

With Gmail, search these and open promising threads in full with `get_thread` —
search previews truncate and the numbers live in the message body:

    from:rocketmoney.com newer_than:30d
    {subject:receipt subject:invoice subject:"auto-renew" subject:renews} newer_than:30d

## Step 3 — Triage honestly

For each charge, the question is not "is this recurring" but **"is he getting
value"**. You usually can't answer that from data alone, so:

- Evidence he *isn't* using it (no login emails, no activity, he's said so) →
  propose `KILL` with your reasoning.
- Genuinely unclear → ask, but batch the questions into one list. Don't
  interrogate him one merchant at a time.
- Obviously in use → leave it alone and don't mention it.

A price increase on something he uses is still worth surfacing, because the
decision he made at the old price isn't the one he's living with now.

## Step 4 — Report

Lead with what needs a decision. Keep it short enough to read on a phone.

    ## Needs a decision
    - [Merchant] — $X/mo, [why it's suspect]. Kill it?

    ## Needs action
    - [Merchant] — marked KILL on [date], still charging. Cancellation failed.

    ## Done since last time
    - [Merchant] — cancelled, $X/mo recovered.

Then a single line: total monthly recurring, and monthly savings identified.

Omit any section that's empty. A quiet week should produce one line, and that's
a success, not a failure to find something.

## Step 5 — Cancel and pursue refunds

This is the part that actually saves money, and the part Rocket Money doesn't
do. See `references/cancellation-playbooks.md` for merchant-specific paths and
refund tactics.

Two rules that matter:

**On sending email.** Joel has authorized sending cancellation emails from his
Gmail, but show him the draft and get explicit confirmation in that same
conversation first. An email sent on his behalf is irreversible and goes out
under his name — that's worth ten seconds of his attention every time.

**On what you can't do.** Most cancellations are a web form or a live chat
widget, and you cannot operate those. Don't pretend otherwise or leave it
vague. Give him a paste-ready script with the specific facts already filled in
— dates, amounts, last-use — so his chat takes two minutes instead of twenty.
Being clear about the handoff is more useful than appearing more capable.

## Step 6 — Commit

Update `subscriptions.md` with everything learned, including questions he
answered, and commit. Next run depends on it.
