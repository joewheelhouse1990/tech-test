import functions.musicbrainz_funcs as mbf
import functions.ApiLyricCollector as alf
import musicbrainzngs as mb
import numpy as np


class FetchArtistBuilder:

    def __init__(self, logger):
        self.logger = logger
        self.artist = None
        self.artist_id = None
        self.recs = None
        self.lyric_count_arr = None
        self.lyrics_sum = None
        self.song_count = None
        self.avg_lyrics = None
        self.avg_lyrics_fl = None

        # set legit artist and artist id from user input
        self.fetch_artist_id()

    def fetch_artist_id(self):

        print("Enter artist below")
        artist = input("")

        self.set_artist_id(artist)

        while self.artist_id is None:
            print(f"No artist found with name {artist}")
            print("Enter artist name below...")
            artist = input("")

            self.set_artist_id(artist)

        # set the artist name on legit artist id return
        self.artist = artist

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

        self.lyrics_sum = np.sum(self.lyric_count_arr)
        self.song_count = len(self.lyric_count_arr)
        self.avg_lyrics = round(self.lyrics_sum/self.song_count, 1)
        self.avg_lyrics_fl = self.lyrics_sum//self.song_count

    def print_to_console(self):

        print(f"Average lyrics in songs by {self.artist}: {self.avg_lyrics}")

