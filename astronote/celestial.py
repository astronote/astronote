# -*- coding: utf-8 -*-

###############################################################################
# Celestial
###############################################################################

# Methods relating to celestial events that are too small for their own module.

import ephem
import math
from datetime import datetime
from . import helpers


def get_meteor_showers(date):
    """Return a list of all meteor showers that are nearby a location based on
    the date.

    Keyword arguments:
    date -- a YYYY-MM-DD string.
    """

    # A list of popular meteor showers, detailing the meteor shower name and the
    # expected peak.
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

    # Retrieve the year by splitting the date of the current location.
    year = helpers.split_date(ephem.Date(date))['year']

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

            visible_meteor_showers.append({
                'name': meteor_shower['name'],
                'peak': meteor_shower['peak']
            })

        elif end_date < peak_date:

            break

    return visible_meteor_showers

