# -*- coding: utf-8 -*-

###############################################################################
# Seasons
###############################################################################

# Methods relating to astronomical events (things that occur no more than a few
# times each year).

import ephem
import math
from datetime import datetime
from . import helpers


def is_solstice(date):
    """Returns a Boolean if the given day does not land on a solstice, or a
    PyEphem Date if the given day does land on a solstice.

    Keyword arguments:
    date -- a YYYY-MM-DD string.
    """

    next_solstice = ephem.next_solstice(date)
    return helpers.set_date_to_midnight(next_solstice) == ephem.Date(date)


def get_solstice_type(date):
    """Returns a string representing the type of solstice based on what month
    the solstice occurs on. It is assumed the date being passed has been
    confirmed to be a solstice.

    Keyword arguments:
    date -- a YYYY-MM-DD string.
    """

    month = datetime.strptime(date, '%Y-%m-%d').month

    if month == 6:
        return 'june'
    elif month == 12:
        return 'december'
    else:
        return None


def is_equinox(date):
    """Returns a Boolean if the given day does not land on a equinox, or a
    PyEphem Date if the given day does land on a equinox.

    Keyword arguments:
    date -- a YYYY-MM-DD string.
    """

    next_equinox = ephem.next_equinox(date)
    return helpers.set_date_to_midnight(next_equinox) == ephem.Date(date)


def get_equinox_type(date):
    """Returns a string representing the type of equinox based on what month
    the equinox occurs on. It is assumed the date being passed has been
    confirmed to be a equinox.

    Keyword arguments:
    date -- a YYYY-MM-DD string.
    """

    month = datetime.strptime(date, '%Y-%m-%d').month

    if month == 3:
        return 'march'
    elif month == 9:
        return 'september'
    else:
        return None
