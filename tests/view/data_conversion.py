import unittest

from strava_data_analyser.view.data_conversion import m_to_km, mps_to_kmh, mps_to_minpkm, seconds_to_hh_mm_ss

class DataConversion(unittest.TestCase):

    def test_m_to_km(self):
        self.assertEqual(m_to_km(10_000), 10)
        self.assertEqual(m_to_km(42_195), 42.195)

    def test_mps_to_kmh(self):
        self.assertEqual(mps_to_kmh(1), 3.6)
        self.assertEqual(mps_to_kmh(25), 90)

    def test_mps_to_mpkm(self):
        mpkm = mps_to_minpkm(3.33)
        minutes = mpkm[0]
        seconds = mpkm[1]
        self.assertEqual(minutes, 5)
        self.assertEqual(seconds, 0)

    def test_seconds_to_hh_mm_ss(self):
        hh_mm_ss = seconds_to_hh_mm_ss(191_235)
        self.assertEqual(hh_mm_ss[0], 53)
        self.assertEqual(hh_mm_ss[1], 7)
        self.assertEqual(hh_mm_ss[2], 15)


if __name__ == '__main__':
    unittest.main()
