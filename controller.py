import logging
import functions.FetchArtistBuilder as fad
import time


# global variables #
# format for log
_LOG_FMT = "%(asctime)s %(levelname)s:%(name)s: %(message)s"


def setup_log():
    logging.basicConfig(
        format=_LOG_FMT,
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    return logger


def run_job():

    logger = setup_log()
    run_fad = fad.FetchArtistBuilder(logger)
    run_fad.fetch_song_details()
    if run_fad.lyric_count_arr.size > 0:
        run_fad.summarise_lyrics()
        run_fad.print_to_console()
    else:
        print("No songs fetched from API")


if __name__ == '__main__':

    run_job()
