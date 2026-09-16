# Weekly Playbook — Sunday evening

Runs in a fresh session. Assume no memory. Work in this order.

## 1. Load state

Read `subscriptions.md`. That is the ground truth from last week.

## 2. Pull the week's signal from Gmail

    from:rocketmoney.com newer_than:8d
    {subject:receipt subject:invoice subject:"auto-renew" subject:renews} newer_than:8d
    from:no.reply.alerts@chase.com newer_than:8d

Open the Rocket Money "upcoming bills", "Subscription increase alert", and
"Large transaction detected" threads in full — the search preview truncates and
the numbers live in the body.

## 3. Diff against the register

For each recurring charge found:

- Not in the register → new row, status `SUSPECT` until Joel confirms.
- In the register at a different amount → **price increase, always flag.**
- In the register, unchanged → no news, stay quiet.
- Marked `KILL` and charged anyway → the cancellation failed. Escalate.

## 4. Report

Keep it short. Only these three things:

1. **Needs a decision** — new or increased charges.
2. **Needs action** — `KILL` items still billing, refund windows closing.
3. **Nothing else.** No recap of things that did not change. A quiet week
   should produce a one-line report.

## 5. Drafting and sending

For anything `KILL`:

- Research the actual cancellation path. Many merchants deliberately hide it.
- Where the merchant accepts **email** cancellation → draft it, show Joel,
  send from his Gmail on his confirmation. Never send unconfirmed.
- Where it is a **web form or live chat** → he has to click it. Give him a
  paste-ready script with the specific facts (dates, amounts, last-use) filled
  in, so the chat takes two minutes rather than twenty.

Refund asks land better when they are specific and narrow. Ask for the last
1–2 unused cycles, not "all of it". Cite: no usage, and no renewal notice sent
where that is true.

## 6. Commit

Update `subscriptions.md` and commit. If this step is skipped, next week
starts blind.
