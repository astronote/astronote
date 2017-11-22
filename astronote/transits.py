# -*- coding: utf-8 -*-

###############################################################################
# Transits
###############################################################################

# Methods that calculate transit information such as rise and set times.

import ephem
from datetime import datetime
from . import helpers


def format_transit_time(transit_type, date):
    """Returns a dictionary that defines a transit time, containing both the
    type of transit (i.e. a rise or set) and the datetime that it occurs.

    Keyword arguments:
    transit_type -- a string defining what the transit is, e.g. rise or set
    date -- a datetime object.
    """

    # Define a dictionary to hold all data, that will eventually be returned.
    transit = {'type': transit_type}

    # If the date is valid then the date is split into a dictionary. Otherwise,
    # the date is likely a "NeverUp" or "AlwaysUp" string and is stored as is.
    if helpers.is_date(date):
        transit['time'] = helpers.split_date(date)
    else:
        transit['time'] = date

    return transit


def get_transit_times(body, date, lat, lon):

    # Define an Observer.
    location = helpers.define_location(date, lat, lon)

    # Create a holder for all transit information.
    times = []

    # Set up all rise and set variables. The objective is to generate a set of
    # four rise and set times in either a rise/set/rise/set or
    # set/rise/set/rise pattern. Due to all dates and times being based on UTC,
    # the extra information is useful for applications that will convert from
    # UTC to a timezone/offset.
    prev_body_rise = None
    prev_body_set = None
    body_rise = None
    body_set = None
    next_body_rise = None
    next_body_set = None

    # Get the initial rise and set times for the body.
    body_rise = get_transit(location.next_rising, body)
    body_set = get_transit(location.next_setting, body)

    # If the rise and set times are both valid, get additional information.
    if helpers.is_date(body_rise) and helpers.is_date(body_set):

        # If the body sets after rising, get a previous set and future rise.
        if body_rise < body_set:
            prev_body_set = get_transit(location.previous_setting, body, start=body_rise)
            next_body_rise = get_transit(location.next_rising, body, start=body_set)

            times.append(format_transit_time('set', prev_body_set))
            times.append(format_transit_time('rise', body_rise))
            times.append(format_transit_time('set', body_set))
            times.append(format_transit_time('rise', next_body_rise))

        # If the body sets before rising, get a previous rise and future set.
        else:
            prev_body_rise = get_transit(location.previous_rising, body, start=body_set)
            next_body_set = get_transit(location.next_setting, body, start=body_rise)

            times.append(format_transit_time('rise', prev_body_rise))
            times.append(format_transit_time('set', body_set))
            times.append(format_transit_time('rise', body_rise))
            times.append(format_transit_time('set', next_body_set))

    # If the rise is undefined but the set is valid, get the previous and next
    # rise times based from the set time.
    elif not helpers.is_date(body_rise) and not helpers.is_date(body_set):

        times.append(format_transit_time('rise', body_rise))
        times.append(format_transit_time('set', body_set))

    else:

        if body_rise == 'AlwaysUp':
            prev_body_set = get_transit(location.previous_setting, body, start=body_set)
            next_body_rise = get_transit(location.next_rising, body, start=body_set)

            times.append(format_transit_time('set', prev_body_set))
            times.append(format_transit_time('rise', body_rise))
            times.append(format_transit_time('set', body_set))
            times.append(format_transit_time('rise', next_body_rise))

        elif body_rise == 'NeverUp':
            prev_body_rise = get_transit(location.previous_rising, body, start=body_set)
            next_body_set = get_transit(location.next_setting, body, start=body_set)

            times.append(format_transit_time('rise', prev_body_rise))
            times.append(format_transit_time('set', body_set))
            times.append(format_transit_time('rise', body_rise))
            times.append(format_transit_time('set', next_body_set))

        elif body_set == 'AlwaysUp':
            prev_body_set = get_transit(location.previous_setting, body, start=body_rise)
            next_body_rise = get_transit(location.next_rising, body, start=body_rise)

            times.append(format_transit_time('set', prev_body_set))
            times.append(format_transit_time('rise', body_rise))
            times.append(format_transit_time('set', body_set))
            times.append(format_transit_time('rise', next_body_rise))

        elif body_set == 'NeverUp':
            prev_body_rise = get_transit(location.previous_rising, body, start=body_rise)
            next_body_set = get_transit(location.next_setting, body, start=body_rise)

            times.append(format_transit_time('rise', prev_body_rise))
            times.append(format_transit_time('set', body_set))
            times.append(format_transit_time('rise', body_rise))
            times.append(format_transit_time('set', next_body_set))


    return times


def get_transit(callback, *args, **kwargs):
    """Returns the time of a transit using the specified callback function,
    args and kwargs. Exceptions are included to handle rise and set callback
    functions.

    Keyword arguments
    callback -- the transit function to use.
    *args -- arguments to pass to the callback.
    **kwargs -- keyword arguments to pass to the callback.
    """

    accepted_callbacks = [
        'previous_transit',
        'next_transit',
        'previous_antitransit',
        'next_antitransit',
        'previous_rising',
        'next_rising',
        'previous_setting',
        'next_setting'
    ]

    if callback.__name__ in accepted_callbacks:

        try:
            return callback(*args, **kwargs)
        except ephem.AlwaysUpError:
            return 'AlwaysUp'
        except ephem.NeverUpError:
            return 'NeverUp'
        except:
            return None

    else:
        return None
