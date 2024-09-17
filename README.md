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

## Issues

### I'm getting a timeout

The tool relies on levels.fyi's site layout. This may change. Most of the time it's
just re-labelling of existing elements. The tool
- waits for a table with salaries to load
- then clicks a link to expand them for all salaries as the list is abbreviated first

To fix this, load the website in your favourite browser and then use the browser's web
development tool to locate the respective elements and adjust their names.

[Example commit](https://github.com/bjoernd/meeting-cost/commit/ed41f47891dafcf62b7a1ec562c6937a3d9ea47a)

### Loading takes long

Yes, we should perform some caching between runs.

### I'm not working for Amazon

Yup, we should support arbitrary companies with their job roles and levels.