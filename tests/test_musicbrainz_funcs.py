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
        _test_artist_count = "2731"

        _check_ret = mbf.fetch_recording_count(_test_artist_id)

        self.assertEqual(_check_ret, _test_artist_count)

    def test_fetch_recording_count_nonid(self):
        _test_nonid = "aaa"

        with self.assertRaises(KeyError) as err:
            mbf.fetch_recording_count(_test_nonid)


if __name__ == '__main__':
    unittest.main()
