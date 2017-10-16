# -*- coding: utf-8 -*-

###############################################################################
# Helpers
###############################################################################

# Assorted methods used to aid in repeated calculations.

import ephem
import math
from datetime import datetime


def get_degrees(angle):
    """Returns the value of a PyEphem angle (which is expressed in
    radians) as a floating point number.

    Keyword arguments:
    angle -- a PyEphem Angle object.
    """

    return ephem.degrees(angle).znorm * (180 / math.pi)


def define_location(date, lat, lon):
    """Creates a PyEphem Observer object, setting the date, latitude and
    longitude using the arguments provided.

    Keyword arguments:
    date -- a YYYY-MM-DD string.
    lat -- a floating-point latitude string. (positive/negative = North/South)
    lon -- a floating-point longitude string. (positive/negative = East/West)
    """

    location = ephem.Observer()
    location.date = date
    location.lat = lat
    location.lon = lon

    return location


def is_date(value):
    """ Return a Boolean indicating if the value is a PyEphem Date object.

    Keyword arguments:
    value -- the value to check.
    """

    return isinstance(value, ephem.Date)


def split_date(date):
    """Return a dictionary containing year, month, day, hour, minute and second
    keys (with values) to represent a date.

    Keyword arguments:
    date -- a PyEphem Date object.
    """

    # Split the PyEphem Date object into pieces.
    date = date.tuple()

    # Adjust the 'second' value to be a rounded down integer representation.
    # This is because initially the second value is a floating point (likely to
    # account for milliseconds). This level of specificity isn't required so
    # things are kept simple with an integer.
    return {
        'year': date[0],
        'month': date[1],
        'day': date[2],
        'hour': date[3],
        'minute': date[4],
        'second': int(math.ceil(date[5]))
    }
    return set_date_to_midnight(next_equinox) == ephem.Date(date)


def get_distance_from_earth(body, date):
    """Return the distance of a body from the Earth (in AU) at a given date.

    Keyword arguments:
    body -- the planetary body to measure the distance between.
    date -- a PyEphem Date object.
    """

    body.compute(date)
    return body.earth_distance


def set_date_to_midnight(date):
    """Return a 'floor' version of PyEphem Date object, resetting the time to
    00:00:00 so that the day is reset to midnight.

    Keyword arguments:
    date -- a PyEphem Date object.
    """

    # Because PyEphem measures dates in Dublin Julian Day (number of days that
    # have passed since the last day of 1899 at noon), half a day (12 hours)
    # needs to be subtracted from the date.
    #
    # `math.floor` rounds off the number of days (expressed by `date.real`) so
    # that the day can be subtracted by 12 hours to reach the beginning of the
    # day, i.e. midnight.
    return ephem.Date(round(date.real) - 0.5)


def create_event(event, data):
    """Return a dictionary containing the properties required when defining an
    event.

    Keyword arguments:
    event -- the type of event, used to distinguish multiple events apart.
    data -- a dictionary of key/value pairs containing custom data.
    """

    return {
        'event': event,
        'data': data
    }
