# meeting-cost
Demo tool to calculate the cost of a meeting based on online salary data

The tool downloads current salary data from
[levels.fyi](https://www.levels.fyi) (currently: Amazon, USA) and then computes
the cost of a given meeting based on the hourly salaries of the attendees.

## Usage

```
./meeting-cost ATTENDEE [ATTENDEE ...]

Compute meeting cost based on attendees. Attendee format is <role>-<level>.
Supported roles: SDM SDE TPM
Supported levels: L4 L5 L6 L7 L8

Example usage:
   $> ./meeting-cost SDM-L7 SDE-L7 SDE-L5 SDE-L4 TPM-L6
   Getting salary data...
   Meeting cost:
     -  30 min:    518.12 €
     -  45 min:    777.18 €
     -  60 min:   1036.24 €
     -  90 min:   1554.36 €
     - 120 min:   2072.48 €
```
