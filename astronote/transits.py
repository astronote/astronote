# -*- coding: utf-8 -*-

###############################################################################
# Transits
###############################################################################

# Methods that calculate transit information such as rise and set times.

import ephem
from datetime import datetime
from . import helpers


def get_transit_times(body, date, lat, lon):

    # Define an Observer.
    location = helpers.define_location(date, lat, lon)

    # Create a holder for all transit information.
    times = {}

    # Set up all rise and set variables.
    prev_body_rise = None
    body_rise = None
    body_set = None
    next_body_rise = None

    # Check to see if the body is setting that day.
    body_rise = get_transit(location.next_rising, body)
    body_set = get_transit(location.next_setting, body)

    # If the object sets before it rises, retrive the previous rise time as
    # well to provide context to the set time.
    if helpers.is_date(body_rise) and helpers.is_date(body_set) and body_set < body_rise or \
       isinstance(body_rise, str) and isinstance(body_set, str):

        prev_body_rise = get_transit(location.previous_rising, body)


    # Check to see if the next rise occurs on the same day as the set. If it
    # doesn't, clear the next rise time so that it is excluded from future
    # calculations.
    if helpers.is_date(body_rise) and helpers.is_date(body_set) and body_rise < body_set or \
       isinstance(body_rise, str) and isinstance(body_set, str):

        if helpers.is_date(body_set):
            next_body_rise = get_transit(location.next_rising, body, start=body_set)
        else:
            next_body_rise = get_transit(location.next_rising, body)

        if helpers.is_date(next_body_rise):

            next_body_rise_day = next_body_rise.datetime().day
            current_day = datetime.strptime(date, '%Y-%m-%d').day

            if next_body_rise_day != current_day:
                next_body_rise = None


    # Populate the transit times dictionary.
    if body_rise:
        if helpers.is_date(body_rise):
            body_rise = helpers.split_date(body_rise)
        times['rise'] = body_rise

    if body_set:
        if helpers.is_date(body_set):
            body_set = helpers.split_date(body_set)
        times['set'] = body_set

    if prev_body_rise:
        if helpers.is_date(prev_body_rise):
            prev_body_rise = helpers.split_date(prev_body_rise)
        times['prev_rise'] = prev_body_rise

    if next_body_rise:
        if helpers.is_date(next_body_rise):
            next_body_rise = helpers.split_date(next_body_rise)
        times['next_rise'] = next_body_rise

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
