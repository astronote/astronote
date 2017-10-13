# -*- coding: utf-8 -*-

from .context import astronote
import unittest
import ephem


class TimeMethods(unittest.TestCase):

    location = ephem.Observer()


    def setUp(self):
        self.location.date = '2017/01/01'
        self.location.lat = 0
        self.location.lon = 0

        self.date = self.location.date
        self.lat = self.location.lat
        self.lon = self.location.lon


    def test_next_set_return_value(self):
        moon = ephem.Moon()
        moon.compute(self.location)
        next_set = self.location.next_setting(moon)
        next_set_date = astronote.split_date(next_set)

        self.assertEqual(next_set_date, {
            'year': 2017,
            'month': 1,
            'day': 1,
            'hour': 20,
            'minute': 52,
            'second': 47
        })


    def test_next_rise_return_value(self):
        moon = ephem.Moon()
        moon.compute(self.location)
        next_rise = self.location.next_rising(moon)
        next_rise_date = astronote.split_date(next_rise)

        self.assertEqual(next_rise_date, {
            'year': 2017,
            'month': 1,
            'day': 1,
            'hour': 8,
            'minute': 28,
            'second': 44
        })


class DistanceMethods(unittest.TestCase):

    location = ephem.Observer()


    def setUp(self):
        self.location.date = '2017/01/01'
        self.location.lat = 0
        self.location.lon = 0

        self.date = self.location.date
        self.lat = self.location.lat
        self.lon = self.location.lon


    def test_get_distance_from_earth_return_value(self):
        moon = ephem.Moon()
        moon.compute(self.location)

        distance = astronote.get_distance_from_earth(moon, '2017/01/01')
        self.assertAlmostEqual(distance, 0.0026, places=4)





class DateMethods(unittest.TestCase):

    def test_set_date_to_midnight_after_noon_return_value(self):
        date = ephem.Date('2017/01/01 15:15:15')
        date = astronote.set_date_to_midnight(date)
        self.assertEqual(date, ephem.Date('2017/01/01 00:00:00'))


    def test_set_date_to_midnight_before_noon_return_value(self):
        date = ephem.Date('2017/01/01 05:05:05')
        date = astronote.set_date_to_midnight(date)
        self.assertEqual(date, ephem.Date('2017/01/01 00:00:00'))


    def test_is_solstice_december_return_value(self):
        solstice = astronote.is_solstice('2016/12/21')
        self.assertTrue(solstice)


    def test_is_solstice_june_return_value(self):
        solstice = astronote.is_solstice('2017/06/21')
        self.assertTrue(solstice)


    def test_is_solstice_empty_return_value(self):
        solstice = astronote.is_solstice('2017/01/01')
        self.assertFalse(solstice)


    def test_is_equinox_autumn_return_value(self):
        equinox = astronote.is_equinox('2016/03/20')
        self.assertTrue(equinox)


    def test_is_equinox_spring_return_value(self):
        equinox = astronote.is_equinox('2017/09/22')
        self.assertTrue(equinox)


    def test_is_equinox_empty_return_value(self):
        equinox = astronote.is_equinox('2017/01/01')
        self.assertFalse(equinox)


    def test_split_date_return_value(self):
        date = ephem.Date('2017/01/01')
        split_date = astronote.split_date(date)
        self.assertEqual(split_date, {
            'year': 2017,
            'month': 1,
            'day': 1,
            'hour': 0,
            'minute': 0,
            'second': 0
        })





class SunMethods(unittest.TestCase):

    location = ephem.Observer()
    sun = ephem.Sun()


    def setUp(self):
        self.location.date = '2017/01/01'
        self.location.lat = 0
        self.location.lon = 0

        self.date = self.location.date
        self.lat = self.location.lat
        self.lon = self.location.lon

        self.sun.compute(self.location)


    def test_get_sun_events_return_value(self):
        sun_events = astronote.get_sun_events(self.date, self.lat, self.lon)
        self.assertEqual(sun_events, {
            'rise': {
                'year': 2017,
                'month': 1,
                'day': 1,
                'hour': 5,
                'minute': 59,
                'second': 41
            },
            'set': {
                'year': 2017,
                'month': 1,
                'day': 1,
                'hour': 18,
                'minute': 7,
                'second': 39
            }
        })



class MoonMethods(unittest.TestCase):

    location = ephem.Observer()
    moon = ephem.Moon()


    def setUp(self):
        self.date = '2017/01/01'
        self.lat = 0
        self.lon = 0

        self.location.date = self.date
        self.location.lat = self.lat
        self.location.lon = self.lon

        self.moon.compute(self.location)


    def test_is_moon_apogee_return_value(self):
        self.date = '2017/01/22'
        self.assertTrue(astronote.is_moon_apogee(self.moon, self.date))


    def test_is_moon_apogee_empty_return_value(self):
        self.assertFalse(astronote.is_moon_apogee(self.moon, self.date))


    def test_is_moon_perigee_return_value(self):
        self.date = '2017/01/10'
        self.assertTrue(astronote.is_moon_perigee(self.moon, self.date))


    def test_is_moon_perigee_empty_return_value(self):
        self.assertFalse(astronote.is_moon_perigee(self.moon, self.date))


    def test_get_major_moon_phase_return_value(self):
        self.assertTrue(astronote.get_major_moon_phase('2017/01/05'))


    def test_get_major_moon_phase_empty_return_value(self):
        self.assertFalse(astronote.get_major_moon_phase('2017/01/01'))


    def test_get_moon_events_return_value(self):
        moon_events = astronote.get_moon_events(self.date, self.lat, self.lon)
        self.assertEqual(moon_events, {
            'rise': {
                'year': 2017,
                'month': 1,
                'day': 1,
                'hour': 8,
                'minute': 28,
                'second': 44
            },
            'set': {
                'year': 2017,
                'month': 1,
                'day': 1,
                'hour': 20,
                'minute': 52,
                'second': 47
            },
            'phase': {
                'percent': 13
            }
        })





class PlanetMethods(unittest.TestCase):

    location = ephem.Observer()
    mercury = ephem.Mercury()
    venus = ephem.Venus()
    mars = ephem.Mars()
    jupiter = ephem.Jupiter()
    saturn = ephem.Saturn()
    uranus = ephem.Uranus()
    neptune = ephem.Neptune()
    pluto = ephem.Pluto()


    def setUp(self):
        self.date = '2017/01/01'
        self.lat = 0
        self.lon = 0

        self.location.date = self.date
        self.location.lat = self.lat
        self.location.lon = self.lon


    def test_get_planet_mars_return_value(self):
        self.mars.compute(self.location)
        mars_events = astronote.get_planet_events(self.mars, self.date, self.lat, self.lon)
        self.assertEqual(mars_events, {
            'rise': {
                'year': 2017,
                'month': 1,
                'day': 1,
                'hour': 9,
                'minute': 59,
                'second': 36
            },
            'set': {
                'year': 2017,
                'month': 1,
                'day': 1,
                'hour': 22,
                'minute': 3,
                'second': 33
            },
            'visible': True
        })





class AlignmentMethods(unittest.TestCase):

    location = ephem.Observer()


    def setUp(self):
        self.date = '2017/01/01'


    def test_get_oppositions_return_value(self):
        self.date = '2017/04/07'
        oppositions = astronote.get_oppositions(self.date)
        self.assertEqual(oppositions, [
            {
                'event': 'opposition',
                'highlight': False,
                'data': {
                    'body': 'jupiter'
                }
            }
        ])


    def test_get_oppositions_empty_return_value(self):
        oppositions = astronote.get_oppositions(self.date)
        self.assertEqual(oppositions, [])


    def test_get_conjunctions_return_value(self):
        self.date = '2017/04/14'
        conjunctions = astronote.get_conjunctions(self.date)
        self.assertEqual(conjunctions, [
            {
                'event': 'conjunction',
                'highlight': False,
                'data': {
                    'body': 'uranus',
                    'type': 'conjuction'
                }
            }
        ])


    def test_get_conjunctions_superior_return_value(self):
        self.date = '2017/03/07'
        conjunctions = astronote.get_conjunctions(self.date)
        self.assertEqual(conjunctions, [
            {
                'event': 'conjunction',
                'highlight': False,
                'data': {
                    'body': 'mercury',
                    'type': 'superior'
                }
            }
        ])


    def test_get_conjunctions_inferior_return_value(self):
        self.date = '2017/03/25'
        conjunctions = astronote.get_conjunctions(self.date)
        self.assertEqual(conjunctions, [
            {
                'event': 'conjunction',
                'highlight': False,
                'data': {
                    'body': 'venus',
                    'type': 'inferior'
                }
            }
        ])


    def test_get_conjunctions_empty_return_value(self):
        conjunctions = astronote.get_conjunctions(self.date)
        self.assertEqual(conjunctions, [])


    def test_get_elongations_east_return_value(self):
        self.date = '2017/01/12'
        elongations = astronote.get_elongations(self.date)
        self.assertEqual(elongations, [
            {
                'event': 'elongation',
                'highlight': False,
                'data': {
                    'body': 'venus',
                    'type': 'east'
                }
            }
        ])


    def test_get_elongations_west_return_value(self):
        self.date = '2017/01/19'
        elongations = astronote.get_elongations(self.date)
        self.assertEqual(elongations, [
            {
                'event': 'elongation',
                'highlight': False,
                'data': {
                    'body': 'mercury',
                    'type': 'west'
                }
            }
        ])


    def test_get_elongations_empty_return_value(self):
        elongations = astronote.get_elongations(self.date)
        self.assertEqual(elongations, [])


    def test_get_min_separations_return_value(self):
        self.date = '2017/01/02'
        separations = astronote.get_min_separations(self.date)
        self.assertEqual(separations, [
            {
                'event': 'separation',
                'highlight': False,
                'data': {
                    'body1': 'moon',
                    'body2': 'venus',
                    'angle': 1.8,
                }
            }
        ])


    def test_get_min_separations_empty_return_value(self):
        self.date = '2017/01/04'
        separations = astronote.get_min_separations(self.date)
        self.assertEqual(separations, [])



class MeteorShowerMethods(unittest.TestCase):

    location = ephem.Observer()


    def setUp(self):
        self.date = '2017/01/01'
        self.lat = 0
        self.lon = 0


    def test_get_meteor_showers_return_value(self):
        meteor_showers = astronote.get_meteor_showers(self.date, self.lat, self.lon)
        self.assertEqual(meteor_showers, [
            {
                'event': 'meteor_shower',
                'highlight': True,
                'data': {
                    'name': 'Quadrantids',
                    'peak': {
                        'month': 1,
                        'day': 3
                    }
                }
            }
        ])


    def test_get_meteor_showers_empty_return_value(self):
        self.date = '2017/01/20'
        meteor_showers = astronote.get_meteor_showers(self.date, self.lat, self.lon)
        self.assertEqual(meteor_showers, [])


if __name__ == '__main__':

    unittest.main()
