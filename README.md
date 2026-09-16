# cookiestash

Subscription and recurring-spend watch for Joel Birdsall.

## Why this repo exists

Claude sessions are ephemeral — each weekly run starts in a fresh container with
no memory of the last one. This repo *is* the memory. Every run reads
`subscriptions.md` for state, does its work, and commits what it learned.

## Architecture

    Chase accounts
         |
         v
    Rocket Money  (already connected via Plaid; the sensor)
         |  emails alerts
         v
       Gmail
         |  read by
         v
    Weekly Claude run  -->  updates subscriptions.md
         |
         v
    Report + drafted cancellation / refund messages

No Plaid integration of our own. No stored bank credentials. Rocket Money
already holds that connection and there is no reason to build a second one.

## Files

| File | Purpose |
|---|---|
| `subscriptions.md` | The register. Running state of every recurring charge. |
| `WEEKLY-PLAYBOOK.md` | What the Sunday run does, step by step. |
| `refunds/` | Drafted cancellation and refund requests, one per merchant. |
