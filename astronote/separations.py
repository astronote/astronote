# -*- coding: utf-8 -*-

###############################################################################
# Separations
###############################################################################

# Methods that are used to calculate interesting separations between bodies.

import ephem
from datetime import datetime
from . import helpers


def get_separation(body1, body2, time):
    """Returns the angular separation between any two bodies at a given time.

    Keyword arguments:
    body1 -- a PyEphem Body object (typically a planet).
    body2 -- a PyEphem Body object (typically a planet).
    time -- a PyEphem Date object.
    """

    body1.compute(time)
    body2.compute(time)
    return helpers.get_degrees(ephem.separation(body1, body2))


def is_min_separation(body1, body2, date):
    """Returns True if the two bodies reach their closet point (approaching and
    then shifting apart) on the given day.

    Keyword arguments:
    body1 -- a PyEphem Body object (typically a planet).
    body2 -- a PyEphem Body object (typically a planet).
    date -- a YYYY-MM-DD string.
    """

    time1 = ephem.Date(date)
    time2 = ephem.Date(time1 + 1)

    sep1a = get_separation(body1, body2, time1)
    sep1b = get_separation(body1, body2, time1 + ephem.minute)
    sep2a = get_separation(body1, body2, time2 - ephem.minute)
    sep2b = get_separation(body1, body2, time2)

    if (sep1a >= sep1b) and (sep2a <= sep2b):
        return True
    else:
        return False


def get_min_separation(body1, body2, date):
    """Returns a rough estimate of the minimum angular separation between two
    bodies on a given day by comparing the separations every 15 minutes
    throughout the day. Once the minimum has been found, the `for` loop cancels
    to avoid any unnecessary calculations.

    Keyword arguments:
    body1 -- a PyEphem Body object (typically a planet).
    body2 -- a PyEphem Body object (typically a planet).
    date -- a PyEphem Date object.
    """

    separations = []

    for hour in range(0, 95):

        offset = 0

        if hour > 0:
            offset = hour / 4

        time = ephem.Date(date) + (ephem.hour * offset)
        separation =  get_separation(body1, body2, time)

        # Check if the separation is increasing again so that we can break the
        # loop early.
        if separations and separation > separations[-1]:
            break
        else:
            separations.append(separation)

    # If the minimum separation is less than or equal to 4 degrees, return the
    # separation value.
    if separations[-1] <= 4:
        return separations[-1]
    else:
        return None


def get_min_separations(date):
    """Calculates any interesting, low angle separations between any two
    bodies.

    Keyword arguments:
    date -- a YYYY-MM-DD string.
    """

    separations = []

    bodies = [
        ephem.Moon(date),
        ephem.Mercury(date),
        ephem.Venus(date),
        ephem.Mars(date),
        ephem.Jupiter(date),
        ephem.Saturn(date),
        ephem.Neptune(date),
        ephem.Uranus(date),
        ephem.Pluto(date)
    ]

    for body1 in bodies:

        for body2 in bodies:

            if (body1 != body2):

                separation = is_min_separation(body1, body2, date)

                if separation:

                    separation_event = helpers.create_event('separation', {
                        'body1': body1.name.lower(),
                        'body2': body2.name.lower()
                    })

                    if separation < 1:
                        separation_event['data']['angle'] = round(separation, 2)
                    else:
                        separation_event['data']['angle'] = round(separation, 1)

                    separations.append(separation_event)

        # Remove the body from the list of bodies since it has been compared
        # against all other bodies, and duplicate comparisons/results are
        # undesired.
        bodies.pop(0)

    return separations
