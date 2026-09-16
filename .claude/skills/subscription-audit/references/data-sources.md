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

## 2. Rocket Money CSV export -- best source, already paid for

Joel has Rocket Money Premium ($6/mo), and **data export is a Premium feature**
he is already entitled to. Prefer this over the Chase export.

rocketmoney.com -> sign in -> Transactions -> export. Rocket Money emails a
**Download File** link, and that link only opens on a desktop or laptop.

Three reasons this beats exporting from Chase directly:

- Every linked account lands in one file -- both Chase cards, checking, and
  anything else he has connected. No merging exports by hand.
- Transactions arrive already categorized.
- It carries Rocket Money's own recurring-charge detection, which is the
  analysis he is paying them for. Use it rather than re-deriving it.

`scripts/find_recurring.py` reads whatever columns it finds via the date /
description / amount aliases, so it handles this export too. If the layout has
drifted and rows get skipped, read the header and adjust rather than guessing.

## 3. Chase CSV export -- fallback

Useful when the Rocket Money export is unavailable, or to check an account
Rocket Money is not linked to.

chase.com -> account -> **More** -> **Download account activity** -> pick a date
range -> CSV. **Desktop site only** -- the mobile app cannot do this.

Limits: about 24 months and 1,000 rows, per account, so multiple accounts mean
multiple files. Pass them all to the script at once; it merges them. Older
statements are PDF only, with no structured export.

Two column layouts, both handled:

    Credit card: Transaction Date, Post Date, Description, Category, Type, Amount, Memo
    Checking:    Details, Posting Date, Description, Amount, Type, Balance, Check or Slip #

## 4. Plaid MCP — if it ever gets set up

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

## Not a source: cookie-based Rocket Money MCP servers

A community MCP server (`312-dev/rocketmoney-mcp`) exposes Rocket Money data by
having the user extract their `tb.auth0.sid` session cookie from a logged-in
browser tab and paste it into the server.

Do not steer Joel toward this, and push back if it comes up again. A session
cookie is not a scoped read-only token -- it is his logged-in identity, carrying
every permission the account has, including management of the Plaid links to his
bank. Nothing constrains such a server to reading. It also breaks whenever the
cookie expires and almost certainly violates Rocket Money's terms, which puts
the bank connections themselves at risk.

Rocket Money has no official API or MCP server as of September 2026. There are
open feature requests on rocketmoney.canny.io asking for a read-only MCP / Claude
connector; that is the legitimate path, and voting on them is worth more than
working around the gap.
