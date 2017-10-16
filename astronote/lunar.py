# -*- coding: utf-8 -*-

###############################################################################
# Lunar
###############################################################################

import ephem
from datetime import datetime
from . import transits
from . import helpers


def is_major_phase(date):
    """Returns a code if the date coincides with a major Moon phase, i.e. first
    quarter, full Moon, last quarter or new Moon.

    Keyword arguments:
    date -- a PyEphem Date object.
    """

    # Calculate the exact date and time of each upcoming major Moon phase.
    next_new_moon = ephem.next_new_moon(date)
    next_first_quarter_moon = ephem.next_first_quarter_moon(date)
    next_full_moon = ephem.next_full_moon(date)
    next_last_quarter_moon = ephem.next_last_quarter_moon(date)

    # Format the major Moon phase dates by resetting their hour, minute and
    # second values to zero, positioning each day at midnight so that they can
    # be directly compared against the date argument.
    next_new_moon_date = helpers.set_date_to_midnight(next_new_moon)
    next_first_quarter_moon_date = helpers.set_date_to_midnight(next_first_quarter_moon)
    next_full_moon_date = helpers.set_date_to_midnight(next_full_moon)
    next_last_quarter_moon_date = helpers.set_date_to_midnight(next_last_quarter_moon)

    # Convert the `date` arugment to an Ephem Date for comparison.
    date = ephem.Date(date)

    # Return the appropriate code based on if there is a match. No matches will
    # return `None`.
    if (next_new_moon_date == date):
        return 'new_moon'

    if (next_first_quarter_moon_date == date):
        return 'first_quarter'

    if (next_full_moon_date == date):
        return 'full_moon'

    if (next_last_quarter_moon_date == date):
        return 'last_quarter'

    return None


def is_at_apogee(moon, date):
    """Returns True if the Moon is at apogee (i.e. farthest point from Earth in
    a cycle) on the specified day.

    Keyword arguments:
    moon -- a PyEphem Moon object.
    date -- a YYYY-MM-DD string.
    """

    moon.compute(date)
    time1 = ephem.Date(date)
    time2 = ephem.Date(time1 + 1)

    dist1a = helpers.get_distance_from_earth(moon, time1)
    dist1b = helpers.get_distance_from_earth(moon, time1 + ephem.minute)
    dist2a = helpers.get_distance_from_earth(moon, time2 - ephem.minute)
    dist2b = helpers.get_distance_from_earth(moon, time2)

    return (dist1a <= dist1b) and (dist2a >= dist2b)


def is_at_perigee(moon, date):
    """Returns True if the Moon is at perigee (i.e. closest point from Earth in
    a cycle) on the specified day.

    Keyword arguments:
    body -- a PyEphem Body object (typically a planet).
    date -- a YYYY-MM-DD string.
    """

    moon.compute(date)
    time1 = ephem.Date(date)
    time2 = ephem.Date(time1 + 1)

    dist1a = helpers.get_distance_from_earth(moon, time1)
    dist1b = helpers.get_distance_from_earth(moon, time1 + ephem.minute)
    dist2a = helpers.get_distance_from_earth(moon, time2 - ephem.minute)
    dist2b = helpers.get_distance_from_earth(moon, time2)

    return (dist1a >= dist1b) and (dist2a <= dist2b)
