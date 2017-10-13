# -*- coding: utf-8 -*-

import ephem
import math
from datetime import datetime


# A list of popular meteor showers, detailing the meteor shower name and the
# expected peak (expressed as a dictionary of the month and day).
meteor_showers = [
    {
        'name': 'Quadrantids',
        'peak': {
            'month': 1,
            'day': 3
        }
    },
    {
        'name': 'Lyrids',
        'peak': {
            'month': 4,
            'day': 22
        }
    },
    {
        'name': 'Eta Aquarids',
        'peak': {
            'month': 5,
            'day': 6
        }
    },
    {
        'name': 'Perseids',
        'peak': {
            'month': 8,
            'day': 13
        }
    },
    {
        'name': 'Draconids',
        'peak': {
            'month': 10,
            'day': 8
        }
    },
    {
        'name': 'Orionids',
        'peak': {
            'month': 10,
            'day': 21
        }
    },
    {
        'name': 'Leonids',
        'peak': {
            'month': 11,
            'day': 18
        }
    },
    {
        'name': 'Geminids',
        'peak': {
            'month': 12,
            'day': 14
        }
    },
    {
        'name': 'Ursids',
        'peak': {
            'month': 12,
            'day': 22
        }
    }
]


def get_events(date = datetime.now().strftime('%Y-%m-%d'), lat = '0', lon = '0'):
    """Calculates all astronomical events on a given day at a given location.
    The returned events containin information about:

    - the Sun;
    - the Moon;
    - visible planets for the night;
    - any oppositions, conjuctions and elongations;
    - any current meteor showers; and
    - if the given day is a solstice or equinox.

    Keyword arguments:
    date -- a YYYY-MM-DD string.
    lat -- a floating-point latitude string. (positive/negative = North/South)
    lon -- a floating-point longitude string. (positive/negative = East/West)
    """

    # Determine the hemisphere based on the latitude.
    if float(lat) > 0:
        hemisphere = 'north'
    else:
        hemisphere = 'south'

    # Calculate the event information for all key objects. These values with
    # contain either dictionaries or null values.
    sun = get_sun_events(date, lat, lon)
    moon = get_moon_events(date, lat, lon)
    planets = get_visible_planets(date, lat, lon)

    # Define a list to store all events that occur on the given day.
    events = []

    # Check if the day is the next solstice. If it is, create an event
    # specifying the type of solstice (i.e. June or December solstice) and
    # add it to the event list.
    if is_solstice(date):

        if datetime.strptime(date, '%Y-%m-%d').month == 6:
            solstice = create_event('solstice', True, {
                'type': 'june'
            })
        else:
            solstice = create_event('solstice', True, {
                'type': 'december'
            })

        events.append(solstice)

    # Check if the day is the next equinox. If it is, create an event
    # specifying the type of equinox (i.e. March or September equinox) and
    # add it to the event list.
    if is_equinox(date):

        if datetime.strptime(date, '%Y-%m-%d').month == 3:
            equinox = create_event('equinox', True, {
                'type': 'march'
            })
        else:
            equinox = create_event('equinox', True, {
                'type': 'september'
            })

        events.append(equinox)

    # Get a list of all other astronomical events that can occur and append
    # them all to the events list.
    oppositions = get_oppositions(date)
    conjunctions = get_conjunctions(date)
    elongations = get_elongations(date)
    min_separations = get_min_separations(date)
    meteor_showers = get_meteor_showers(date, lat, lon)
    events += oppositions + conjunctions + elongations + min_separations + meteor_showers

    return {
        'hemisphere': hemisphere,
        'sun': sun,
        'moon': moon,
        'planets': planets,
        'events': events
    }


def get_moon_events(date, lat, lon):
    """Calculates the events for the Moon on a given day at a given location.
    The following events are calculated:

    - Moonrise and Moonset times;
    - Moon phase; and
    - Whether the Moon is at perigee or apogee.

    Keyword arguments:
    date -- a YYYY-MM-DD string.
    lat -- a floating-point latitude string. (positive/negative = North/South)
    lon -- a floating-point longitude string. (positive/negative = East/West)
    """

    location = define_location(date, lat, lon)
    moon = ephem.Moon()
    moon.compute(location)

    moonrise = get_next_rise(moon, date, lat, lon)
    moonset = get_next_set(moon, moonrise, lat, lon)

    # Prepopulate a dictionary with event that will always have return data..
    events = {
        'rise': split_date(moonrise),
        'set': split_date(moonset),
        'phase': {
            'percent': int(round(moon.moon_phase * 100, 0))
        }
    }

    # Add a flag is the Moon is at perigee or apogee.
    if is_moon_perigee(moon, date):
        events['perigee'] = True
    elif is_moon_apogee(moon, date):
        events['apogee'] = True

    # Check if the Moon is at a major Moon phase (e.g. full Moon, first
    # quarter). If it is, append a `name` property to the Moon's `phase`
    # property.
    major_moon_phase = get_major_moon_phase(date)

    if major_moon_phase:
        events['phase']['name'] = major_moon_phase

    # Return the list of Moon events for the day.
    return events


def get_sun_events(date, lat, lon):
    """Calculates the events for the Sun on a given day at a given location.
    The following events are calculated:

    - Sunrise and Sunset times;

    Keyword arguments:
    date -- a YYYY-MM-DD string.
    lat -- a floating-point latitude string. (positive/negative = North/South)
    lon -- a floating-point longitude string. (positive/negative = East/West)
    """

    location = define_location(date, lat, lon)
    sun = ephem.Sun()
    sun.compute(location)

    sunrise = get_next_rise(sun, date, lat, lon)
    sunset = get_next_set(sun, sunrise, lat, lon)

    # Prepopulate a dictionary with all recurring events.
    events = {
        'rise': split_date(sunrise),
        'set': split_date(sunset)
    }

    # Return a list of Sun events for the day.
    return events


def get_visible_planets(date, lat, lon):
    """Calculates the planets that will be visible on the evening of a given
    day at a given location.

    Keyword arguments:
    date -- a YYYY-MM-DD string.
    lat -- a floating-point latitude string. (positive/negative = North/South)
    lon -- a floating-point longitude string. (positive/negative = East/West)
    """

    mercury = ephem.Mercury()
    venus = ephem.Venus()
    mars = ephem.Mars()
    jupiter = ephem.Jupiter()
    saturn = ephem.Saturn()
    uranus = ephem.Uranus()
    neptune = ephem.Neptune()
    pluto = ephem.Pluto()

    planets = {
        'mercury': get_planet_events(mercury, date, lat, lon),
        'venus': get_planet_events(venus, date, lat, lon),
        'mars': get_planet_events(mars, date, lat, lon),
        'jupiter': get_planet_events(jupiter, date, lat, lon),
        'saturn': get_planet_events(saturn, date, lat, lon),
        'uranus': get_planet_events(uranus, date, lat, lon),
        'neptune': get_planet_events(neptune, date, lat, lon),
        'pluto': get_planet_events(pluto, date, lat, lon)
    }

    visible_planets = []

    for planet, events in planets.items():
        if planets[planet]['visible']:
            events['name'] = planet
            visible_planets.append(events)

    return visible_planets


def get_planet_events(planet, date, lat, lon):
    """Return the rise and set times and visibility of a planet.

    Keyword arguments:
    planet -- a PyEphem planetary object, e.g. Mars.
    date -- a YYYY-MM-DD string.
    lat -- a floating-point latitude string. (positive/negative = North/South)
    lon -- a floating-point longitude string. (positive/negative = East/West)
    """

    planet_rise = get_next_rise(planet, date, lat, lon)
    planet_set = get_next_set(planet, date, lat, lon)
    twilight_start = get_twilight_start(date, lat, lon)
    twilight_end = get_twilight_end(date, lat, lon, twilight_start)

    location = define_location(twilight_end, lat, lon)
    sun = ephem.Sun()
    sun.compute(location)

    planet_in_twilight = is_planet_visible(date, lat, lon, planet_rise, planet_set, twilight_start, twilight_end)
    planet_distance_to_sun = ephem.degrees(ephem.separation(planet, sun)).znorm * (180 / math.pi)

    if planet_in_twilight and planet_distance_to_sun > 15:
        planet_is_visible = True
    else:
        planet_is_visible = False

    events = {
        'rise': split_date(planet_rise),
        'set': split_date(planet_set),
        'visible': planet_is_visible
    }

    return events


def get_next_rise(body, date, lat, lon, start=None):
    """Return the date and time when an object will next rise above the horizon.

    Keyword arguments:
    body -- the planetary body to check the next rise time for.
    date -- a YYYY-MM-DD string.
    lat -- a floating-point latitude string. (positive/negative = North/South)
    lon -- a floating-point longitude string. (positive/negative = East/West)
    start -- a date and time to start the search from.
    """

    location = define_location(date, lat, lon)

    if start:
        next_rise = location.next_rising(body, start=start)
    else:
        next_rise = location.next_rising(body)

    return next_rise


def get_next_set(body, date, lat, lon, start=None):
    """Return the date and time when an object will next set below the horizon.

    Keyword arguments:
    body -- the planetary body to check the next set time for.
    date -- a YYYY-MM-DD string.
    lat -- a floating-point latitude string. (positive/negative = North/South)
    lon -- a floating-point longitude string. (positive/negative = East/West)
    start -- a date and time to start the search from.
    """

    location = define_location(date, lat, lon)

    if start:
        next_set = location.next_setting(body, start=start)
    else:
        next_set = location.next_setting(body)

    return next_set


def is_planet_visible(date, lat, lon, planet_rise, planet_set, twilight_start, twilight_end):
    """Return a Boolean indicating if the planet will be visible at night. This
    is determined by one of two ways, depending on if the planet rises and
    sets, or sets and then rises, on the given day.

    If the planet rises and then sets, a check will be done to see if the
    planet's time above the horizon intersects with twilight.

    If the planet sets and then rises, a check will be done to see if the
    planet rises during twilight or sets during twilight.

    Keyword arguments:
    planet_rise -- the date and time that a planet will rise.
    planet_set -- the date and time that a planet will set.
    date -- a YYYY-MM-DD string.
    lat -- a floating-point latitude string. (positive/negative = North/South)
    lon -- a floating-point longitude string. (positive/negative = East/West)
    """

    # Determine what kind of check should be made, and rearrange the dates if
    # the planet sets before it rises on the given day.
    if planet_rise <= planet_set:
        date1a = planet_rise
        date1b = planet_set
        check_overlap = True
    else:
        date1a = planet_set
        date1b = planet_rise
        check_overlap = False

    # An hour leeway is given either side of twilight to account for visibility
    # restrictions as a result of trees, hills and other objects.
    date2a = twilight_start + ephem.hour
    date2b = twilight_end - ephem.hour

    if check_overlap:
        # This will check if the planet's above horizon time intersects with
        # twilight.
        return (date1a <= date2b) and (date2a <= date1b)
    else:
        # This will check if the planet rises or sets during twilight.
        return (date2a <= date1a <= date2b) or (date2a <= date1b <= date2b)


def get_oppositions(date):
    """Calculates the planets that will be at opposition on a given date.

    Keyword arguments:
    date -- a YYYY-MM-DD string.
    """

    oppositions = []

    planets = [
        ephem.Mars(date),
        ephem.Jupiter(date),
        ephem.Saturn(date),
        ephem.Neptune(date),
        ephem.Uranus(date),
        ephem.Pluto(date)
    ]

    # Loop through each planet, appending it to a list if an opposition is
    # found.
    for planet in planets:

        opposition = is_opposition(planet, date)

        if (opposition):

            opposition_event = create_event('opposition', False, {
                'body': planet.name.lower()
            })

            oppositions.append(opposition_event)

    return oppositions


def get_conjunctions(date):
    """Calculates the planets that will be at a conjuction on a given date.

    Keyword arguments:
    date -- a YYYY-MM-DD string.
    """

    conjunctions = []

    planets = [
        ephem.Mercury(date),
        ephem.Venus(date),
        ephem.Mars(date),
        ephem.Jupiter(date),
        ephem.Saturn(date),
        ephem.Neptune(date),
        ephem.Uranus(date),
        ephem.Pluto(date)
    ]

    # Loop through each planet, appending it to a list if an opposition is
    # found. The type of conjuction is also included.
    for planet in planets:

        conjunction = is_conjunction(planet, date)

        if (conjunction):

            conjunction_event = create_event('conjunction', False, {
                'body': planet.name.lower(),
                'type': conjunction
            })

            conjunctions.append(conjunction_event)

    return conjunctions


def get_elongations(date):
    """Calculates the planets that will be at a elongation on a given date.
    Note that only Mercury and Venus (interior planets) can only ever be at
    elongation.

    Keyword arguments:
    date -- a YYYY-MM-DD string.
    """

    elongations = []

    # Only inferior planets have elongations
    planets = [
        ephem.Mercury(date),
        ephem.Venus(date),
    ]

    # Loop through each planet, appending it to a list if an elongation is
    # found. The type of elongation is also included.
    for planet in planets:

        elongation = is_elongation(planet, date)

        if (elongation):

            elongation_event = create_event('elongation', False, {
                'body': planet.name.lower(),
                'type': elongation
            })

            elongations.append(elongation_event)

    return elongations


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

                    separation_event = create_event('separation', False, {
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



def get_twilight_start(date, lat, lon, start=None):
    """Return the time of which nautical twilight will start on a given day at
    a given location.

    Keyword arguments:
    date -- a YYYY-MM-DD string.
    lat -- a floating-point latitude string. (positive/negative = North/South)
    lon -- a floating-point longitude string. (positive/negative = East/West)
    start -- a date and time to start the search from.
    """

    location = define_location(date, lat, lon)
    location.horizon = '-6'

    if start:
        twilight_start = location.next_setting(ephem.Sun(), use_center=True, start=start)
    else:
        twilight_start = location.next_setting(ephem.Sun(), use_center=True)

    return twilight_start


def get_twilight_end(date, lat, lon, start=None):
    """Return a PyEphem Date object for when nautical twilight ends at the
    given location.

    Keyword arguments:
    date -- a YYYY-MM-DD string.
    lat -- a floating-point latitude string. (positive/negative = North/South)
    lon -- a floating-point longitude string. (positive/negative = East/West)
    start -- a date and time to start the search from.
    """

    location = define_location(date, lat, lon)
    location.horizon = '-6'

    if start:
        twilight_end = location.next_rising(ephem.Sun(), use_center=True, start=start)
    else:
        twilight_end = location.next_rising(ephem.Sun(), use_center=True)

    return twilight_end


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
        'second': int(math.floor(date[5]))
    }


def get_major_moon_phase(date):
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
    next_new_moon_date = set_date_to_midnight(next_new_moon)
    next_first_quarter_moon_date = set_date_to_midnight(next_first_quarter_moon)
    next_full_moon_date = set_date_to_midnight(next_full_moon)
    next_last_quarter_moon_date = set_date_to_midnight(next_last_quarter_moon)

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


def is_moon_apogee(moon, date):
    """Returns True if the Moon is at apogee (i.e. farthest point from Earth in
    a cycle) on the specified day.

    Keyword arguments:
    moon -- a PyEphem Moon object.
    date -- a YYYY-MM-DD string.
    """

    time1 = ephem.Date(date)
    time2 = ephem.Date(time1 + 1)

    dist1a = get_distance_from_earth(moon, time1)
    dist1b = get_distance_from_earth(moon, time1 + ephem.minute)
    dist2a = get_distance_from_earth(moon, time2 - ephem.minute)
    dist2b = get_distance_from_earth(moon, time2)

    return (dist1a <= dist1b) and (dist2a >= dist2b)


def is_moon_perigee(moon, date):
    """Returns True if the Moon is at perigee (i.e. closest point from Earth in
    a cycle) on the specified day.

    Keyword arguments:
    body -- a PyEphem Body object (typically a planet).
    date -- a YYYY-MM-DD string.
    """

    time1 = ephem.Date(date)
    time2 = ephem.Date(time1 + 1)

    dist1a = get_distance_from_earth(moon, time1)
    dist1b = get_distance_from_earth(moon, time1 + ephem.minute)
    dist2a = get_distance_from_earth(moon, time2 - ephem.minute)
    dist2b = get_distance_from_earth(moon, time2)

    return (dist1a >= dist1b) and (dist2a <= dist2b)


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
    """Returns True if the body is at conjuction (i.e. its elongation from the
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
    if ((ephem.pi * 1.5 <= elong1 <= ephem.pi * 2) and (0 <= elong2 <= ephem.pi / 2)) or \
           ((0 <= elong1 <= ephem.pi / 2) and (ephem.pi * 1.5 <= elong2 <= ephem.pi * 2)):

        if body.name == 'Mercury' or body.name == 'Venus':
            if ephem.pi * 1.5 < elong2 < ephem.pi * 2:
                return 'inferior'
            else:
                return 'superior'
        else:
            return 'conjuction'

    else:

        return False


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

    if abs(get_degrees(elong1a)) > 5 and abs(get_degrees(elong2b)) > 5:

        if (elong1a <= elong1b) and (elong2a >= elong2b) or \
           (elong1a >= elong1b) and (elong2a <= elong2b):

            if elong2b < 0:
                return 'west'
            elif elong2b > 0:
                return 'east'

    else:

        return False


def get_separation(body1, body2, time):
    """Returns the angular separation between any two bodies at a given time.

    Keyword arguments:
    body1 -- a PyEphem Body object (typically a planet).
    body2 -- a PyEphem Body object (typically a planet).
    time -- a PyEphem Date object.
    """

    body1.compute(time)
    body2.compute(time)
    return get_degrees(ephem.separation(body1, body2))


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
        return find_min_separation(body1, body2, date)
    else:
        return False


def find_min_separation(body1, body2, date):
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


def get_meteor_showers(date, lat, lon):
    """Return a list of all meteor showers that are nearby a location based on
    the date.

    Keyword arguments:
    date -- a YYYY-MM-DD string.
    lat -- a floating-point latitude string. (positive/negative = North/South)
    lon -- a floating-point longitude string. (positive/negative = East/West)
    """

    # Retrieve the year by splitting the date of the current location.
    year = split_date(ephem.Date(date))['year']

    # Calculate the start and end date range that will be used to compare
    # against the peaks of all meteor showers.
    start_date = ephem.Date(date) - 3
    end_date = ephem.Date(date) + 3

    # Create an empty list that will be populated if any meteor showers are
    # nearby.
    visible_meteor_showers = []

    # Check each meteor shower, stopping the check after a meteor shower later
    # than the location date is checked. This prevents us from checking things
    # that will never return a value.
    for meteor_shower in meteor_showers:

        month = meteor_shower['peak']['month']
        day = meteor_shower['peak']['day']
        peak_date = ephem.Date(datetime(year, month, day))

        if peak_date > start_date and peak_date < end_date:

            meteor_shower_event = create_event('meteor_shower', True, {
                'name': meteor_shower['name'],
                'peak': meteor_shower['peak']
            })

            visible_meteor_showers.append(meteor_shower_event)

        elif start_date > peak_date:
            break

    return visible_meteor_showers


def is_solstice(date):
    """Returns a Boolean if the given day does not land on a solstice, or a
    PyEphem Date if the given day does land on a solstice.

    Keyword arguments:
    date -- a YYYY-MM-DD string.
    """

    next_solstice = ephem.next_solstice(date)
    return set_date_to_midnight(next_solstice) == ephem.Date(date)


def is_equinox(date):
    """Returns a Boolean if the given day does not land on a equinox, or a
    PyEphem Date if the given day does land on a equinox.

    Keyword arguments:
    date -- a YYYY-MM-DD string.
    """

    next_equinox = ephem.next_equinox(date)
    return set_date_to_midnight(next_equinox) == ephem.Date(date)


def get_degrees(angle):
    """Returns the value of a PyEphem angle (which is expressed in
    radians) as a floating point number.

    Keyword arguments:
    angle -- a PyEphem Angle object.
    """

    return ephem.degrees(angle).znorm * (180 / math.pi)


def define_location(date = datetime.now().strftime("%Y-%m-%d"), lat = '0', lon = '0'):
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


def create_event(event, highlight, data):
    """Return a dictionary containing the properties required when defining an
    event.

    Keyword arguments:
    event -- the type of event, used to distinguish multiple events apart.
    highlight -- whether or not the event is of significant importance.
    data -- a dictionary of key/value pairs containing custom data.
    """

    return {
        'event': event,
        'highlight': highlight,
        'data': data
    }
