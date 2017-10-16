# -*- coding: utf-8 -*-

###############################################################################
# Bodies
###############################################################################

# Methods that calculate information for planetary bodies, including
# oppositions, conjunctions, elongations and visibility times.

import ephem
from datetime import datetime
from . import helpers


def is_visible(body, date):
    return True


def is_opposition(body, date):
    """Returns True if the body is at opposition (i.e. its elongation from the
    Sun passes 180 degrees, placing it behind the Earth).

    Keyword arguments:
    body -- a PyEphem Body object (typically a planet).
    date -- a YYYY-MM-DD string.
    """

    time1 = ephem.Date(date)
    time2 = ephem.Date(time1 + 1)

    body.compute(time1)
    elong1 = body.elong.norm

    body.compute(time2)
    elong2 = body.elong.norm

    return ((elong1 <= ephem.pi) and (elong2 >= ephem.pi)) or \
           ((elong1 >= ephem.pi) and (elong2 <= ephem.pi))



def is_conjunction(body, date):
    """Returns True if the body is at conjunction (i.e. its elongation from the
    Sun passes 360 degrees, placing it behind the Sun).

    Keyword arguments:
    body -- a PyEphem Body object (typically a planet).
    date -- a YYYY-MM-DD string.
    """

    time1 = ephem.Date(date)
    time2 = ephem.Date(time1 + 1)

    body.compute(time1)
    elong1 = body.elong.norm

    body.compute(time2)
    elong2 = body.elong.norm

    # Due to the value of elongation crossing the 0-360 degree (e.g. 0 and 2 Pi
    # radians), the elongation has to check if it transitions from the fourth
    # quadrant to the first quadrant (or vice versa) to truly know if the 2 Pi
    # point has been crossed.
    return ((ephem.pi * 1.5 <= elong1 <= ephem.pi * 2) and (0 <= elong2 <= ephem.pi / 2)) or \
           ((0 <= elong1 <= ephem.pi / 2) and (ephem.pi * 1.5 <= elong2 <= ephem.pi * 2))


def get_conjunction_type(body, date):
    """Returns a string indicating the type of conjunction, based on whether it
    is an inferior or superior body.

    Keyword arguments:
    body -- a PyEphem Body object (typically a planet).
    date -- a YYYY-MM-DD string.
    """

    time = ephem.Date(date) + 1
    body.compute(time)
    elong = body.elong.norm

    if body.name == 'Mercury' or body.name == 'Venus':

        if ephem.pi * 1.5 < elong < ephem.pi * 2:
            return 'inferior'
        else:
            return 'superior'

    else:
        return 'conjunction'


def is_elongation(body, date):
    """Returns True if the body is at its greatest elongation (i.e. it is at a
    point where it is farthest away from the Sun when viewed from Earth).

    Keyword arguments:
    body -- a PyEphem Body object (typically a planet).
    date -- a YYYY-MM-DD string.
    """

    time1 = ephem.Date(date)
    time2 = ephem.Date(time1 + 1)

    body.compute(time1)
    elong1a = body.elong.znorm

    # Hours are used over minutes due to the values being too close and
    # constantly misfiring positives.
    body.compute(time1 + ephem.hour)
    elong1b = body.elong.znorm

    body.compute(time2 - ephem.hour)
    elong2a = body.elong.znorm

    body.compute(time2)
    elong2b = body.elong.znorm

    if abs(helpers.get_degrees(elong1a)) > 5 and abs(helpers.get_degrees(elong2b)) > 5:

        return (elong1a <= elong1b) and (elong2a >= elong2b) or \
               (elong1a >= elong1b) and (elong2a <= elong2b)

    else:

        return False


def get_elongation_type(body, date):
    """Returns a string indicating the type of elongation, based on whether it
    is a Western or Eastern elongation.

    Keyword arguments:
    body -- a PyEphem Body object (typically a planet).
    date -- a YYYY-MM-DD string.
    """

    time = ephem.Date(date) + 1
    body.compute(time)
    elong = body.elong.znorm

    if elong < 0:
        return 'west'
    elif elong > 0:
        return 'east'
