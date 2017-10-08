# AstroNote

AstroNote is a Python package that leverages Python's PyEphem package to
calculate and return a list of astronomical events the occur on any given date.

AstroNote returns data on:

- Sunrise and sunset times;
- Moonrise and moonset times;
- Moon phase information;
- visible planets on a given night;
- oppositions, conjunctions and elongations;
- current meteor showers; and
- solstice and equinox checks.


## Acknowledgements

AstroNote borrows functions found in Don Cross' JavaScript astronomy engine,
[astronomy.js](http://cosinekitty.com/astronomy.js), as well as calculations
used in his [Astronomy Calendar](http://cosinekitty.com/astro_calendar.html).
These functions include the methods for finding Moon perigees and apogees, and
when two bodies reach an interesting minimum angular separation.
