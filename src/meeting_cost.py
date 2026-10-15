#!/usr/bin/env python3

# Meeting cost calculator
#
# Use salary data from levels.fyi to compute the cost of a meeting
# based on its attendees.

# TODO:
#  - caching of salary data
#  - use logging
#  - support other countries than USA
#  - support other companies than Amazon
#  - support other job roles than SDM, SDE and TPM
#  - support other currencies
#  - support other meeting lengths

import json
import re
import sys
import urllib.request

SDE_URL="https://www.levels.fyi/companies/amazon/salaries/software-engineer?country=254"
SDM_URL="https://www.levels.fyi/companies/amazon/salaries/software-engineering-manager?country=254"
TPM_URL="https://www.levels.fyi/companies/amazon/salaries/technical-program-manager?country=254"

# levels.fyi serves an empty page to clients that do not look like a browser
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"

LEVELS = ["L4", "L5", "L6", "L7", "L8"]
WORK_DAYS_PER_YEAR = 238
HOURS_PER_DAY = 8


class SalaryDataNotFound(Exception):
    """The levels.fyi page did not contain salary data in the expected form."""


def fetch_page(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode()


def hourly_rates(page):
    """Map each supported level to an hourly rate in USD, using the salary
    data levels.fyi embeds in its pages for Next.js."""
    match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', page, re.S)
    if not match:
        raise SalaryDataNotFound("no embedded page data")

    try:
        props = json.loads(match.group(1))["props"]["pageProps"]
        currency = props["locationCurrency"]
        totals = {average["shortestLevelName"].split()[0]: average["rawValues"]["total"]
                  for average in props["averages"]}
    except (KeyError, ValueError) as error:
        raise SalaryDataNotFound(f"unexpected page data layout: {error!r}") from error

    if currency != "USD":
        raise SalaryDataNotFound(f"expected USD, got {currency}")

    return {level: total / WORK_DAYS_PER_YEAR / HOURS_PER_DAY
            for level, total in totals.items() if level in LEVELS}


def usage():
    print(f"{sys.argv[0]} ATTENDEE [ATTENDEE ...]")
    print()
    print("Compute meeting cost based on attendees. Attendee format is <role>-<level>.")
    print("Supported roles: SDM SDE TPM")
    print("Supported levels: L4 L5 L6 L7 L8")
    print()
    print("Example usage:")
    print(f"""   $> {sys.argv[0]} SDM-L7 SDE-L7 SDE-L5 SDE-L4 SDE-L5
   Getting salary data...
   Meeting cost:
     -  30 min:    516.02 €
     -  45 min:    774.03 €
     -  60 min:   1032.04 €
     -  90 min:   1548.06 €
     - 120 min:   2064.08 €
    """)


def main():
    salaries = {}

    if len(sys.argv) < 2:
        usage()
        sys.exit(0)

    print("Getting salary data...")
    for title, short, url in [ ("Software Engineering Managers", "SDM", SDM_URL),
                        ("Software Developers", "SDE", SDE_URL),
                        ("Technical Program Managers", "TPM", TPM_URL)]:
        salaries[short] = hourly_rates(fetch_page(url))

    hourly_cost = 0

    # Treat all cmd line args as attendees of the format <short>-<level>
    for attendee in sys.argv[1:]:
        job, level = attendee.split('-')

        try:
            hourly = salaries[job][level]
            hourly_cost += hourly
        except KeyError as ke:
            print(f"Skipping unknown attendee type {attendee}")

    print("Meeting cost:")
    for length in [0.5, 0.75, 1, 1.5, 2]:
        print(f"  - {int(length * 60):3d} min: {hourly_cost * length: 9.2f} USD")


if __name__ == "__main__":
    main()
