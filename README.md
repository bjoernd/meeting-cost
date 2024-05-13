# meeting-cost
Demo tool to calculate the cost of a meeting based on online salary data

The tool downloads current salary data from levels.fyi (currently: Amazon, USA)
and then computes the cost of a given meeting based on the hourly salaries of
the attendees.

## Usage

```
./meeting-cost ATTENDEE [ATTENDEE ...]

Compute meeting cost based on attendees. Attendee format is <role>-<level>.
Supported roles: SDM SDE
Supported levels: L4 L5 L6 L7 L8

Example usage:
   $> ./meeting-cost SDM-L7 SDE-L7 SDE-L5 SDE-L4 SDE-L5
   Getting salary data...
   Meeting cost:
     -  30 min:    516.02 €
     -  45 min:    774.03 €
     -  60 min:   1032.04 €
     -  90 min:   1548.06 €
     - 120 min:   2064.08 €
```
