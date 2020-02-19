import unittest
import functions.ApiLyricCollector as alf
import numpy as np


class MyTestCase(unittest.TestCase):
    def test_legit_api_call(self):
        # set up a legit lyric collector api
        test_artist = "Lewis Capaldi"
        test_song = "Before You Go"
        test_arr = []
        test_arr.append(test_song)

        self.alc = alf.ApiLyricCollector(test_artist, test_arr, None)

        exp_ret = 321
        self.alc.run_fetch_from_api_lyrics()
        arr = np.array(self.alc.count_arr)
        check_ret = arr[0]

        self.assertEqual(exp_ret, check_ret)

    def test_non_legit_call(self):
        # set up a non-legit lyric collector api
        test_artist = "Lewis Capaldiiii"
        test_song = "Before You Gooo"
        test_arr = []
        test_arr.append(test_song)

        self.alc_non = alf.ApiLyricCollector(test_artist, test_arr, None)

        exp_ret = []
        self.alc_non.run_fetch_from_api_lyrics()

        self.assertEqual(exp_ret, self.alc_non.count_arr)


if __name__ == '__main__':
    unittest.main()
