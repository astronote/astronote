# -*- coding: utf-8 -*-

###############################################################################
# AstroNote
###############################################################################

import ephem
import math
from datetime import datetime
from . import lunar
from . import bodies
from . import seasons
from . import celestial
from . import transits
from . import separations
from . import helpers


def get_events(date = datetime.now().strftime('%Y-%m-%d'), lat = '0', lon = '0'):
    """Calculates all astronomical events on a given day at a given location.
    The returned events containin information about:

    - the Sun;
    - the Moon;
    - visible planets for the night;
    - any oppositions, conjunctions and elongations;
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


    # Create a location and all body objects.
    location = helpers.define_location(date, lat, lon)

    # Create all of the PyEphem objects that will be used.
    sun = ephem.Sun(location)
    moon = ephem.Moon(location)
    mercury = ephem.Mercury(location)
    venus = ephem.Venus(location)
    mars = ephem.Mars(location)
    jupiter = ephem.Jupiter(location)
    saturn = ephem.Saturn(location)
    uranus = ephem.Uranus(location)
    neptune = ephem.Neptune(location)
    pluto = ephem.Pluto(location)

    # Create lists for referencing in later loops.
    planets = [mercury, venus, mars, jupiter, saturn, uranus, neptune, pluto]
    bodies = [moon] + planets


    # Define a list to store all events that occur on the given day.
    events = {
        'sun': get_sun_data(sun, date, lat, lon),
        'moon': get_moon_data(moon, date, lat, lon),
        'planets': get_planet_data(planets, date, lat, lon),
        'events': []
    }


    events['events'] += get_planetary_events(planets, date, lat, lon)
    events['events'] += get_separation_events(bodies, date)
    events['events'] += get_celestial_events(date)


    return events


def get_sun_data(sun, date, lat, lon):

    data = {
        'transits': transits.get_transit_times(sun, date, lat, lon)
    }

    return data


def get_moon_data(moon, date, lat, lon):

    data = {
        'transits': transits.get_transit_times(moon, date, lat, lon),
        'phase': {
            'percent': int(round(moon.moon_phase * 100, 0)),
            'name': lunar.is_major_phase(date)
        }
    }

    if lunar.is_at_perigee(moon, date):
        data['perigee'] = True
    elif lunar.is_at_apogee(moon, date):
        data['apogee'] = True

    return data


def get_planet_data(planets, date, lat, lon):

    data = []

    for planet in planets:

        if bodies.is_visible(planet, date):

            planet_data = {
                'name': planet.name,
                'transits': transits.get_transit_times(planet, date, lat, lon)
            }

            data.append(planet_data)

    return data


def get_planetary_events(planets, date, lat, lon):

    events = []

    for planet in planets:

        if planet.name != 'Mercury' and planet.name != 'Venus':

            if bodies.is_opposition(planet, date):

                opposition = helpers.create_event('opposition', {
                    'body': planet.name.lower()
                })

                events.append(opposition)

        if bodies.is_conjunction(planet, date):

            conjunction = helpers.create_event('conjunction', {
                'body': planet.name.lower(),
                'type': bodies.get_conjunction_type(planet, date)
            })

            events.append(conjunction)

        if bodies.is_elongation(planet, date):

            elongation = helpers.create_event('elongation', {
                'body': planet.name.lower(),
                'type': bodies.get_elongation_type(planet, date)
            })

            events.append(elongation)

    return events


def get_celestial_events(date):

    events = []

    meteor_showers = celestial.get_meteor_showers(date)

    for meteor_shower in meteor_showers:

        events.append(helpers.create_event('meteor_shower', {
            'name': meteor_shower['name'],
            'peak': meteor_shower['peak']
        }))

    return events


def get_separation_events(bodies, date):

    events = []

    # Create a new list that is essentially a copy of the `bodies` list. The
    # purpose of this is so that one list can have items removed while the list
    # used for the main loop remains intact.
    comparators = list(bodies)

    for body1 in bodies:

        for body2 in comparators:

            if (body1 != body2):

                if separations.is_min_separation(body1, body2, date):

                    separation = separations.get_min_separation(body1, body2, date)

                    # If the separation is small enough to be notable, the
                    # separation will be a numerical value. If the separation
                    # is too large, the value will be `None`.
                    if separation:

                        events.append(helpers.create_event('separation', {
                            'body1': body1.name.lower(),
                            'body2': body2.name.lower(),
                            'angle': round(separation, 2)
                        }))

        # Remove the first element from the list which is used for comparisons
        # only. This means that any duplicate checks are avoided because the
        # same check will not be run twice, i.e. Jupiter will not check against
        # Venus because Venus will have already checked against Jupiter.
        comparators.pop(0)

    return events
