# meeting-cost
Demo tool to calculate the cost of a meeting based on online salary data

The tool downloads current salary data from
[levels.fyi](https://www.levels.fyi) (currently: Amazon, USA) and then computes
the cost of a given meeting based on the hourly salaries of the attendees.

## Installation

The tool needs Python 3.12 or later and [Poetry](https://python-poetry.org):

```
poetry install
```

## Usage

```
poetry run meeting-cost ATTENDEE [ATTENDEE ...]

Compute meeting cost based on attendees. Attendee format is <role>-<level>.
Supported roles: SDM SDE TPM
Supported levels: L4 L5 L6 L7 L8

Example usage:
   $> meeting-cost SDM-L7 SDE-L7 SDE-L5 SDE-L4 TPM-L6
   Getting salary data...
   Meeting cost:
     -  30 min:    539.31 USD
     -  45 min:    808.97 USD
     -  60 min:   1078.62 USD
     -  90 min:   1617.94 USD
     - 120 min:   2157.25 USD
```

## How the cost is calculated

Each attendee's hourly rate is the average yearly total compensation
(base salary, bonus and stock) that levels.fyi reports for their role and
level, divided by 238 work days of 8 hours. This is what the attendees
earn, not what the employer pays: benefits, taxes and overhead are not
included.

## Issues

### "Could not read salary data from levels.fyi"

The tool relies on salary data that levels.fyi embeds in its pages. If the
site changes the format of this data, the tool can no longer find it. Run
the tool again first, as levels.fyi occasionally returns empty pages. If the
error persists, the tool needs to be adapted to the new format.

### "Skipping SDM-L4: levels.fyi has no salary data for it"

levels.fyi does not list every level for every role. Attendees without
salary data do not count towards the meeting cost.

### I'm not working for Amazon

Yup, we should support arbitrary companies with their job roles and levels.
