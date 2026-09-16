# Data Sources

Ordered by effort. Use the best one available; say which one you used.

## 1. Gmail — available now, zero setup

Rocket Money is connected to Joel's Chase accounts and emails alerts to
joel.birdsall@gmail.com. Useful queries:

    from:rocketmoney.com newer_than:30d
    from:no.reply.alerts@chase.com newer_than:30d
    {subject:receipt subject:invoice subject:"auto-renew" subject:renews} newer_than:30d

Rocket Money subject lines worth knowing:

| Subject | Contains |
|---|---|
| `🗓️ This week's upcoming bills` | Recurring charges due in 7 days |
| `Subscription increase alert 📈` | A price went up — always flag |
| `⚠️ Large transaction detected` | Unusual charge |
| `Your <Month> spending update` | Month-to-date total |
| `🕒 Time for a check-in` | RM's own unused-subscription nudge |

**Search previews truncate.** They show roughly the 5 oldest messages per thread
with no truncation marker. Always `get_thread` before quoting a number.

**The blind spot that matters:** this only sees merchants that send email.
Meta/Oculus has never sent a billing email to this address — searching all of
Gmail for `meta.com`, `oculus.com`, `facebookmail.com` returns only 2021-22
hardware order mail. A Gmail-only audit will miss silent merchants entirely.
Chase statement emails don't help; they carry balances, not line items.

## 2. Chase CSV export — the complete picture

Joel exports it; it takes about two minutes.

chase.com → account → **More** → **Download account activity** → pick a date
range → CSV. **Desktop site only** — the mobile app can't do this.

Limits: about 24 months and 1,000 rows. No structured export exists for older
statements; those are PDF only.

Two column layouts, both handled by `scripts/find_recurring.py`:

    Credit card: Transaction Date, Post Date, Description, Category, Type, Amount, Memo
    Checking:    Details, Posting Date, Description, Amount, Type, Balance, Check or Slip #

This is the only source that sees silent merchants. When the goal is "find what
I forgot about", ask for this rather than working around its absence.

## 3. Plaid MCP — if it ever gets set up

Check for `mcp__plaid__*` tools in the session. If present, pull transactions
directly and skip the manual export.

Context if it comes up: since 2026-04-15 Plaid offers a **Trial plan** —
auto-approved for most developers, real production data, up to 10 Items,
includes Transactions and Statements, and covers most OAuth institutions
(Chase included). Free.

The catch is that Plaid issues an access token, not a service. Something must
hold that token and serve MCP continuously. A Claude session cannot — it is
ephemeral and gets reclaimed. So this only pays off if Joel runs a persistent
server, and its advantage is continuous polling. For on-demand audits the CSV
gets the same data with no infrastructure and no stored credentials. Don't push
him toward Plaid unless he wants unattended monitoring.

## Known accounts

- Chase Freedom Unlimited Visa (...5744) — primary card, autopay on
- Chase (...4421) and (...8639) — statements only
- US Bank Home Mortgage — large recurring, not a subscription
- Rocket Money — the sensor; its own fee is fair game for the audit too
