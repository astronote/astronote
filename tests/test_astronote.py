# -*- coding: utf-8 -*-

from .context import astronote
import unittest
import ephem


class SeasonMethods(unittest.TestCase):

    def test_is_solstice_return_value(self):
        jun_solstice = astronote.seasons.is_solstice('2016-06-20')
        dec_solstice = astronote.seasons.is_solstice('2016-12-21')
        not_solstice = astronote.seasons.is_solstice('2016-04-21')

        self.assertTrue(jun_solstice)
        self.assertTrue(dec_solstice)
        self.assertFalse(not_solstice)


    def test_get_solstice_type_return_value(self):
        jun_solstice = astronote.seasons.get_solstice_type('2016-06-20')
        dec_solstice = astronote.seasons.get_solstice_type('2016-12-21')
        not_solstice = astronote.seasons.get_solstice_type('2016-04-21')

        self.assertEqual('june', jun_solstice)
        self.assertEqual('december', dec_solstice)
        self.assertEqual(None, not_solstice)


    def test_is_equinox_return_value(self):
        mar_equinox = astronote.seasons.is_equinox('2016-03-20')
        sep_equinox = astronote.seasons.is_equinox('2016-09-22')
        not_equinox = astronote.seasons.is_equinox('2016-04-20')

        self.assertTrue(mar_equinox)
        self.assertTrue(sep_equinox)
        self.assertFalse(not_equinox)


    def test_get_equinox_type_return_value(self):
        mar_equinox = astronote.seasons.get_equinox_type('2016-03-20')
        sep_equinox = astronote.seasons.get_equinox_type('2016-09-22')
        not_equinox = astronote.seasons.get_equinox_type('2016-04-20')

        self.assertEqual('march', mar_equinox)
        self.assertEqual('september', sep_equinox)
        self.assertEqual(None, not_equinox)


class CelestialMethods(unittest.TestCase):

    def test_get_meteor_showers_return_value(self):
        meteor_showers = astronote.celestial.get_meteor_showers('2017-01-01')
        no_meteor_showers = astronote.celestial.get_meteor_showers('2017-01-20')

        self.assertEqual(meteor_showers, [
            {
                'name': 'Quadrantids',
                'peak': {
                    'month': 1,
                    'day': 3
                }
            }
        ])

        self.assertEqual(no_meteor_showers, [])


class TransitMethods(unittest.TestCase):

    def setUp(self):
        self.date = '2017-01-01'
        self.lat = '0'
        self.lon = '0'

        self.location = ephem.Observer()
        self.location.date = self.date
        self.location.lat = self.lat
        self.location.lon = self.lon


    def test_get_transit_times(self):
        sun_transit = astronote.transits.get_transit_times(ephem.Sun(), self.date, self.lat, self.lon)
        self.assertIn('year', sun_transit[0]['time'])
        self.assertIn('month', sun_transit[0]['time'])
        self.assertIn('day', sun_transit[0]['time'])
        self.assertIn('hour', sun_transit[0]['time'])
        self.assertIn('minute', sun_transit[0]['time'])
        self.assertIn('second', sun_transit[0]['time'])


    def test_get_transit(self):

        # This is a random callback made to test the invalid state of the
        # `get_transit` method.
        def test_callback():
            return True

        next_rise = astronote.transits.get_transit(self.location.next_rising, ephem.Sun())
        prev_rise = astronote.transits.get_transit(self.location.previous_rising, ephem.Sun())
        next_set = astronote.transits.get_transit(self.location.next_setting, ephem.Sun())
        prev_set = astronote.transits.get_transit(self.location.previous_setting, ephem.Sun())
        invalid = astronote.transits.get_transit(test_callback, ephem.Sun())

        self.assertIsInstance(next_rise, ephem.Date)
        self.assertIsInstance(prev_rise, ephem.Date)
        self.assertIsInstance(next_set, ephem.Date)
        self.assertIsInstance(next_set, ephem.Date)
        self.assertIsNone(invalid)


class MoonMethods(unittest.TestCase):

    def setUp(self):
        self.moon = ephem.Moon()


    def test_is_major_phase(self):
        full_moon = astronote.lunar.is_major_phase('2017-10-05')
        self.assertEqual(full_moon, 'full_moon')


    def test_is_moon_at_apogee(self):
        is_at_apogee = astronote.lunar.is_at_apogee(self.moon, '2017-10-25')
        is_not_apogee = astronote.lunar.is_at_apogee(self.moon, '2017-10-15')
        self.assertTrue(is_at_apogee)
        self.assertFalse(is_not_apogee)


    def test_is_moon_at_perigee(self):
        is_at_perigee = astronote.lunar.is_at_perigee(self.moon, '2017-10-09')
        is_not_perigee = astronote.lunar.is_at_perigee(self.moon, '2017-10-15')
        self.assertTrue(is_at_perigee)
        self.assertFalse(is_not_perigee)


class BodyMethods(unittest.TestCase):

    def test_is_opposition(self):
        opposition1 = astronote.bodies.is_opposition(ephem.Pluto(), '2017-07-10')
        opposition2 = astronote.bodies.is_opposition(ephem.Pluto(), '2017-07-20')
        self.assertTrue(opposition1)
        self.assertFalse(opposition2)


    def test_is_conjunction(self):
        conjunction1 = astronote.bodies.is_conjunction(ephem.Mercury(), '2017-10-08')
        conjunction2 = astronote.bodies.is_conjunction(ephem.Mercury(), '2017-07-20')
        self.assertTrue(conjunction1)
        self.assertFalse(conjunction2)

    def test_is_elongation(self):
        elongation1 = astronote.bodies.is_elongation(ephem.Mercury(), '2017-07-30')
        elongation2 = astronote.bodies.is_elongation(ephem.Mercury(), '2017-07-20')
        self.assertTrue(elongation1)
        self.assertFalse(elongation2)


class SeparationMethods(unittest.TestCase):

    def test_get_separation(self):
        body1 = ephem.Venus()
        body2 = ephem.Mars()
        time = ephem.Date('2017-10-06')
        separation = astronote.separations.get_separation(body1, body2, time)
        self.assertAlmostEqual(separation, 0.3, places=1)


    def test_is_min_separation(self):
        body1 = ephem.Venus()
        body2 = ephem.Mars()
        time1 = ephem.Date('2017-10-05')
        time2 = ephem.Date('2017-10-01')
        separation1 = astronote.separations.is_min_separation(body1, body2, time1)
        separation2 = astronote.separations.is_min_separation(body1, body2, time2)

        self.assertTrue(separation1)
        self.assertFalse(separation2)


    def test_get_min_separation(self):
        body1 = ephem.Venus()
        body2 = ephem.Mars()
        time = ephem.Date('2017-10-05')
        separation = astronote.separations.get_min_separation(body1, body2, time)
        self.assertAlmostEqual(separation, 0.2, places=1)



class HelperMethods(unittest.TestCase):

    def test_get_degrees(self):
        angle = ephem.degrees('14:12:45.77')
        angle = astronote.helpers.get_degrees(angle)
        self.assertAlmostEqual(angle, 14.2127, places=4)


    def test_is_date(self):
        date = ephem.Date('2017-01-01')
        self.assertTrue(astronote.helpers.is_date(date))
        self.assertFalse(astronote.helpers.is_date('string'))
        self.assertFalse(astronote.helpers.is_date(15))


    def test_split_date(self):
        date = ephem.Date('2017-01-01 14:53:45')
        date = astronote.helpers.split_date(date)

        self.assertEqual(date, {
            'year': 2017,
            'month': 1,
            'day': 1,
            'hour': 14,
            'minute': 53,
            'second': 44
        })


    def test_set_date_to_midnight(self):
        date = ephem.Date('2017-01-01 14:53:45')
        midnight = ephem.Date('2017-01-01 00:00:00')

        self.assertEqual(midnight, astronote.helpers.set_date_to_midnight(date))


    def test_get_distance_from_earth_return_value(self):
        distance = astronote.helpers.get_distance_from_earth(ephem.Moon(), '2017-01-01')
        self.assertAlmostEqual(distance, 0.0026, places=4)


    def test_create_event(self):
        event = astronote.helpers.create_event('event', {
            'foo': 'bar'
        })

        self.assertEqual(event, {
            'type': 'event',
            'data': {
                'foo': 'bar'
            }
        })



if __name__ == '__main__':

    unittest.main()
