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
import os
import re
import sys
import urllib.request

SDE_URL="https://www.levels.fyi/companies/amazon/salaries/software-engineer?country=254"
SDM_URL="https://www.levels.fyi/companies/amazon/salaries/software-engineering-manager?country=254"
TPM_URL="https://www.levels.fyi/companies/amazon/salaries/technical-program-manager?country=254"
ROLE_URLS = {"SDM": SDM_URL, "SDE": SDE_URL, "TPM": TPM_URL}

LEVELS = ["L4", "L5", "L6", "L7", "L8"]
WORK_DAYS_PER_YEAR = 238
HOURS_PER_DAY = 8


class SalaryDataNotFound(Exception):
    """The levels.fyi page did not contain salary data in the expected form."""


def fetch_page(url):
    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read().decode()


def hourly_rates(page):
    """Map each supported level to an hourly rate in USD, using the salary
    data levels.fyi embeds in its pages for Next.js."""
    match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', page, re.DOTALL)
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


def parse_attendee(attendee):
    """Split an attendee given as <role>-<level> into role and level."""
    role, _, level = attendee.upper().partition("-")
    if role not in ROLE_URLS or level not in LEVELS:
        raise ValueError(f"invalid attendee {attendee!r}, expected <role>-<level>")
    return role, level


def usage():
    program = os.path.basename(sys.argv[0])
    print(f"""{program} ATTENDEE [ATTENDEE ...]

Compute meeting cost based on attendees. Attendee format is <role>-<level>.
Supported roles: {" ".join(ROLE_URLS)}
Supported levels: {" ".join(LEVELS)}

Example usage:
   $> {program} SDM-L7 SDE-L7 SDE-L5 SDE-L4 TPM-L6
   Getting salary data...
   Meeting cost:
     -  30 min:    539.31 USD
     -  45 min:    808.97 USD
     -  60 min:   1078.62 USD
     -  90 min:   1617.94 USD
     - 120 min:   2157.25 USD""", file=sys.stderr)


def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(2)

    try:
        attendees = [parse_attendee(attendee) for attendee in sys.argv[1:]]
    except ValueError as error:
        print(error, file=sys.stderr)
        sys.exit(2)

    print("Getting salary data...")
    try:
        salaries = {role: hourly_rates(fetch_page(ROLE_URLS[role]))
                    for role in {role for role, _ in attendees}}
    except SalaryDataNotFound as error:
        print(f"Could not read salary data from levels.fyi ({error}). "
              "The site may have changed, see README.md.", file=sys.stderr)
        sys.exit(1)

    hourly_cost = 0
    for role, level in attendees:
        if level in salaries[role]:
            hourly_cost += salaries[role][level]
        else:
            print(f"Skipping {role}-{level}: levels.fyi has no salary data for it")

    print("Meeting cost:")
    for length in [0.5, 0.75, 1, 1.5, 2]:
        print(f"  - {int(length * 60):3d} min: {hourly_cost * length: 9.2f} USD")


if __name__ == "__main__":
    main()
