import logging
import time
import functions.musicbrainz_funcs as mbf
import functions.ApiLyricCollector as alf
import musicbrainzngs as mb
import numpy as np


# global variables #
# format for log
_LOG_FMT = "%(asctime)s %(levelname)s:%(name)s: %(message)s"


class Director:
    """
    Class for putting together pulling the lyrics summary from the APIs
    """
    def __init__(self, logger):
        self.dict = {}
        self._builder = None
        self.logger = logger

    @property
    def builder(self):
        return self._builder

    @builder.setter
    def builder(self, builder):
        self._builder = builder

    def add_to_dict(self, key, value):
        self.dict[key] = value

    def add_user_input(self):
        print("Welcome to the artist's lyric info collector. Enter 'QUIT' to leave.")
        while True:
            t = input("Enter artist: ")
            if t not in self.dict:
                if not (t.upper() == "QUIT"):
                    if self._builder.build_lyrics_fetch(t):
                        self.dict = self._builder.dict
                    else:
                        break
                else:
                    break
            else:
                self.print_from_dict(t, self.dict)

    def print_from_dict(self, artist, _dict):
        print(f"Summary of lyrics by {artist}:")
        print(f"Average: {_dict[artist]['avg_lyrics']}")
        print(f"Min: {_dict[artist]['min']}")
        print(f"Max: {_dict[artist]['max']}")


class BuildFetchLyrics(Director):
    """
    Put together specific jobs to fetch from the functions and classes built for pulling from APIs
    Allows reseting of class for rebuilding the lyrics summary object
    """
    def __int__(self):
        Director.__init__(self, self.logger)
        self.reset()
        self._fab = None

    def reset(self):
        self._fab = FetchArtistBuilder(self.logger)

    def build_lyrics_fetch(self, artist):
        self.reset()
        self._fab = FetchArtistBuilder(self.logger)
        if self._fab.verify_artist(artist):
            self._fab.fetch_song_details()
            if self._fab.lyric_count_arr.size > 0:
                self._fab.summarise_lyrics()
                self.add_to_dict(self._fab.artist, self._fab.ret_dict)
                self.print_from_dict(self._fab.artist, self.dict)
                return True
            

class FetchArtistBuilder:
    """
    Build process for pulling lyrics in right order
    """
    def __init__(self, logger):
        self.logger = logger
        self.artist = None
        self.artist_id = None
        self.recs = None
        self.lyric_count_arr = None
        self.ret_dict = {}

    def verify_artist(self, artist):
        self.set_artist_id(artist)

        while self.artist_id is None:
            print(f"No artist found with name {artist}")
            artist = input("Enter artist: ")
            if artist.upper() == "QUIT":
                return False
            self.set_artist_id(artist)
        # set the artist name on legit artist id return
        self.artist = artist
        return True

    def set_artist_id(self, artist):
        self.artist_id = mbf.fetch_artist_id(artist)

    def fetch_song_details(self):
        if self.artist_id is not None:
            _rec_count = mbf.fetch_recording_count(self.artist_id)
            _rec_arr = mbf.fetch_recording_list_module(self.artist_id, _rec_count)

            ovh_api = alf.ApiLyricCollector(self.artist, _rec_arr, self.logger)
            ovh_api.run_fetch_from_api_lyrics()
            arr = np.array(ovh_api.count_arr)
            self.lyric_count_arr = np.delete(arr, np.argwhere(arr == None))
        else:
            print(f"No artist found with name: {self.artist}")

    def summarise_lyrics(self):
        self.ret_dict = {
            "sum": np.sum(self.lyric_count_arr),
            "song_count": len(self.lyric_count_arr),
            "avg_lyrics": round(np.sum(self.lyric_count_arr)/len(self.lyric_count_arr)),
            "min": np.amin(self.lyric_count_arr),
            "max": np.amax(self.lyric_count_arr)
        }


def setup_log():
    """
    Sets up basic log and be turned on for debugging if needed
    :return:
    """
    logging.basicConfig(
        format=_LOG_FMT,
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    return logger


def run_job():
    """
    script to run the job in the right order
    :return:
    """
    _logger = setup_log()

    director = Director(_logger)
    builder = BuildFetchLyrics(_logger)
    director.builder = builder

    director.add_user_input()


if __name__ == '__main__':

    run_job()
