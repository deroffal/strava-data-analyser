import unittest

from strava_data_analyser.view.data_format import seconds_as_hhmmss, m_as_km, mps_as_kmh, mps_as_minpkm, bpm, m


class DataFormat(unittest.TestCase):

    def test_seconds_as_hhmmss(self):
        self.assertEqual(seconds_as_hhmmss(1), '00:00:01')
        self.assertEqual(seconds_as_hhmmss(83), '00:01:23')
        self.assertEqual(seconds_as_hhmmss(317018), '88:03:38')

    def test_m_as_km(self):
        self.assertEqual(m_as_km(1234), '1.23km')

    def test_mps_as_kmh(self):
        self.assertEqual(mps_as_kmh(25), '90.0km/h')

    def test_mps_as_minpkm(self):
        self.assertEqual(mps_as_minpkm(3.33), '5:00min/km')

    def test_bpm(self):
        self.assertEqual(bpm(180), '180bpm')

    def test_m(self):
        self.assertEqual(m(238), '238m')


if __name__ == '__main__':
    unittest.main()
