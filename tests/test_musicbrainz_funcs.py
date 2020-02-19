import unittest
import functions.musicbrainz_funcs as mbf


class MyTestCase(unittest.TestCase):
    def test_fetch_artist_id(self):
        _test_artist = "Coldplay"
        _test_artist_id = "cc197bad-dc9c-440d-a5b5-d52ba2e14234"

        _check_ret = mbf.fetch_artist_id(_test_artist)

        self.assertEqual(_check_ret, _test_artist_id)

    def test_fetch_artist_id_nonexistent(self):
        _test_artist = "Ccoldplay"

        _check_ret = mbf.fetch_artist_id(_test_artist)

        self.assertEqual(_check_ret, None)

    def test_fetch_recording_count(self):
        _test_artist_id = "cc197bad-dc9c-440d-a5b5-d52ba2e14234"
        _test_artist_count = "2730"

        _check_ret = mbf.fetch_recording_count(_test_artist_id)

        self.assertEqual(_check_ret, _test_artist_count)

    def test_fetch_recording_count_nonid(self):
        _test_nonid = "aaa"

        with self.assertRaises(KeyError) as err:
            mbf.fetch_recording_count(_test_nonid)

    def test1_check_brackets_in_arr(self):
        test_str = "song"
        _arr = ["song2"]
        check_ret = mbf.check_brackets_in_arr(test_str, _arr)
        exp_ret = True

        self.assertEqual(exp_ret, check_ret)

    def test2_check_brackets_in_arr(self):
        test_str = "song"
        _arr = ["song"]
        check_ret = mbf.check_brackets_in_arr(test_str, _arr)
        exp_ret = None

        self.assertEqual(exp_ret, check_ret)

    def test3_check_brackets_in_arr(self):
        test_str = "song (live)"
        arr = ["song"]
        check_ret = mbf.check_brackets_in_arr(test_str, arr)
        exp_ret = None

        self.assertEqual(exp_ret, check_ret)

    def test_fetch_recording_list_module(self):
        # accurate as of feb 2020
        lc_test_id = "526aab94-697f-44a9-b630-41d1c0505953"
        lc_rec_count = 68
        first_ret = "BEFORE YOU GO"
        second_ret = "BRUISES"
        third_ret = "DAYS GONE QUIET"

        check_ret = mbf.fetch_recording_list_module(lc_test_id, lc_rec_count)
        print(check_ret)

        self.assertEqual(check_ret[0], first_ret)
        self.assertEqual(check_ret[1], second_ret)
        self.assertEqual(check_ret[2], third_ret)

    def test_fetch_recording_list_module_nonid(self):
        # nonid for testing
        test_id = "aa"
        rec_count = 1

        check_ret = mbf.fetch_recording_list_module(test_id, rec_count)

        self.assertEqual(check_ret, None)


if __name__ == '__main__':
    unittest.main()
