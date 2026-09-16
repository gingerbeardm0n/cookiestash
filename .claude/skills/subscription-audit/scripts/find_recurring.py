#!/usr/bin/env python3
"""Find recurring charges in a Chase CSV export.

Chase exports two layouts (credit card and checking); both are handled. Usage:

    python3 find_recurring.py statement.csv [statement2.csv ...]

Merchants are grouped by a normalized name, then any group whose charges repeat
on a recognizable cadence is reported, highest annual cost first. Amount drift
is called out because a price that moved is a decision point even for a service
the user still wants.
"""

import csv
import re
import sys
from collections import defaultdict
from datetime import datetime

# Chase headers vary by account type; these are the aliases seen in exports.
DATE_KEYS = ("Transaction Date", "Posting Date", "Post Date", "Date")
DESC_KEYS = ("Description",)
AMOUNT_KEYS = ("Amount",)

# Cadence buckets: label -> (low, high) days between charges, and periods/year.
CADENCES = (
    ("weekly", 6, 8, 52.0),
    ("biweekly", 13, 16, 26.0),
    ("monthly", 27, 32, 12.0),
    ("bimonthly", 57, 64, 6.0),
    ("quarterly", 86, 96, 4.0),
    ("semiannual", 175, 190, 2.0),
    ("annual", 350, 380, 1.0),
)

# Noise that varies between otherwise-identical charges from one merchant.
NOISE = re.compile(
    r"""
      \b\d{4,}\b                 # order/reference numbers
    | \b[A-Z]{2}\b\s*$           # trailing state code
    | \*+                        # asterisk separators
    | \s+\#\s*\S+                # "#12345"
    | \b(RECURRING|PURCHASE|PAYMENT|DEBIT|CARD|POS|ACH|WEB\s*ID|PPD\s*ID)\b
    | \b\d{3}-\d{3}-\d{4}\b      # phone numbers
    | \bHTTPSWWW\S*|\bWWW\.\S+|\b\S+\.COM\b
    """,
    re.VERBOSE | re.IGNORECASE,
)


def normalize(desc):
    """Collapse a raw description to a stable merchant key."""
    s = desc.upper()
    s = NOISE.sub(" ", s)
    s = re.sub(r"[^A-Z0-9 ]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    # Most merchant identity lives in the first few tokens; the tail is location.
    return " ".join(s.split()[:3]) or desc.upper().strip()


def parse_date(raw):
    for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%m/%d/%y"):
        try:
            return datetime.strptime(raw.strip(), fmt).date()
        except ValueError:
            continue
    return None


def load(paths):
    charges = defaultdict(list)
    skipped = 0
    for path in paths:
        with open(path, newline="", encoding="utf-8-sig") as fh:
            for row in csv.DictReader(fh):
                row = {(k or "").strip(): (v or "").strip() for k, v in row.items()}
                raw_date = next((row[k] for k in DATE_KEYS if row.get(k)), None)
                desc = next((row[k] for k in DESC_KEYS if row.get(k)), None)
                raw_amt = next((row[k] for k in AMOUNT_KEYS if row.get(k)), None)
                if not (raw_date and desc and raw_amt):
                    skipped += 1
                    continue
                date = parse_date(raw_date)
                try:
                    amount = float(raw_amt.replace("$", "").replace(",", ""))
                except ValueError:
                    skipped += 1
                    continue
                # Chase writes charges as negative; ignore credits and refunds.
                if date is None or amount >= 0:
                    continue
                charges[normalize(desc)].append((date, abs(amount), desc))
    return charges, skipped


def classify(gaps):
    """Return (label, periods_per_year) if gaps look regular, else None."""
    if not gaps:
        return None
    median = sorted(gaps)[len(gaps) // 2]
    for label, low, high, per_year in CADENCES:
        if low <= median <= high:
            # Regular enough if most gaps sit in the same bucket.
            hits = sum(1 for g in gaps if low <= g <= high)
            if hits >= max(1, len(gaps) // 2):
                return label, per_year
    return None


def analyze(charges):
    """Split candidates into subscription-like and variable-amount groups.

    Two guards keep grocery runs and other routine retail out of the results.
    First, two charges is a coincidence, not a cadence -- sub-annual patterns
    need three. Annual charges are exempt because two is all a 24-month export
    can show. Second, real subscriptions bill a stable amount; when the amount
    swings, it is usually a merchant visited on a habit rather than a plan, so
    those are reported separately instead of being asserted as subscriptions.
    """
    stable, variable = [], []
    for key, items in charges.items():
        if len(items) < 2:
            continue
        items.sort()
        dates = [d for d, _, _ in items]
        gaps = [(b - a).days for a, b in zip(dates, dates[1:])]
        cadence = classify(gaps)
        if not cadence:
            continue
        label, per_year = cadence
        if len(items) < (2 if label == "annual" else 3):
            continue

        amounts = [a for _, a, _ in items]
        latest, low, high = amounts[-1], min(amounts), max(amounts)
        spread = high - low
        # Allow for tax and small plan changes before calling an amount unstable.
        is_stable = spread <= max(1.00, 0.20 * latest)

        row = {
            "merchant": key,
            "example": items[-1][2],
            "cadence": label,
            "count": len(items),
            "latest": latest,
            "low": low,
            "high": high,
            "annual": latest * per_year,
            "last_seen": dates[-1],
            "drift": spread > 0.01,
        }
        (stable if is_stable else variable).append(row)

    key_fn = lambda r: r["annual"]
    return (sorted(stable, key=key_fn, reverse=True),
            sorted(variable, key=key_fn, reverse=True))


def report(row):
    flag = "  <-- PRICE CHANGED" if row["drift"] else ""
    print(f"{row['merchant']}{flag}")
    print(f"  ${row['latest']:.2f} {row['cadence']} -> ${row['annual']:,.2f}/yr")
    if row["drift"]:
        print(f"  ranged ${row['low']:.2f} to ${row['high']:.2f}")
    print(f"  {row['count']} charges, last on {row['last_seen']}")
    print(f"  on the statement: {row['example'][:70]}")
    print()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    charges, skipped = load(sys.argv[1:])
    stable, variable = analyze(charges)

    if not stable and not variable:
        print("No recurring charges detected.")
        print("A single statement may not span enough time to see a cadence --")
        print("monthly detection needs at least three months of data.")
        return 0

    if stable:
        total = sum(r["annual"] for r in stable)
        print(f"{len(stable)} likely subscriptions | "
              f"~${total:,.2f}/yr | ~${total / 12:,.2f}/mo\n")
        for row in stable:
            report(row)

    if variable:
        print("-" * 60)
        print("Repeating, but the amount varies -- more likely a merchant visited")
        print("on a habit than a subscription. Check before acting on these.\n")
        for row in variable:
            report(row)

    if skipped:
        print(f"({skipped} rows skipped -- unexpected columns or bad amounts)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
