import asyncio
from aiohttp import ClientSession
import logging
import json
import re


# global variables #
# url for api lyrics
_API_URL = "https://api.lyrics.ovh/v1/"

# class LyricCollector:
#
#     def __init__(self):
#         self.api_url = "https://api.lyrics.ovh/v1/"


async def fetch_from_url(url: str, session: ClientSession, logger: logging.Logger):

    response = await session.get(url=url)

    # logger.info(f"Response code for {url}: {response.status}")
    url_content = await response.text()

    return url_content, response.status


async def process_response(url: str, session: ClientSession, logger: logging.Logger):

    url_content, url_response = await fetch_from_url(url=url, session=session, logger=logger)

    # print(f"Content for {url} is: {url_content}")

    if str(url_response) == "200":
        _wrd_count = count_words(url_content)

        return _wrd_count


def count_words(url_content):

    _json = json.loads(url_content)

    _word_count = len(re.findall(r'\S+', _json["lyrics"]))

    return _word_count


async def work_through_urls(url_list, logger):

    async with ClientSession() as session:
        fetch_tasks = []
        for url in url_list:
            fetch_tasks.append(process_response(url=url, session=session, logger=logger))

        arr = await asyncio.gather(*fetch_tasks)

        return arr


def run_fetch_from_api_lyrics(artist, recs, logger):
    """
    given an artist name, array of recordings fetch the lyrics for the songs
    :param artist:
    :param recs:
    :param logger:
    :return:
    """
    urls = []

    for r in recs:
        _build_url = f"{_API_URL}{artist}/{r}"
        urls.append(_build_url)

    wrd_counts = asyncio.run(work_through_urls(urls, logger))

    return wrd_counts


if __name__ == '__main__':
    def setup_log():
        logging.basicConfig(
            format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
            level=logging.INFO
        )
        logger = logging.getLogger(__name__)

        return logger

    _logger = setup_log()

    _logger.info("Starting process")

    urlsa = []
    urlsa.append('https://api.lyrics.ovh/v1/Coldplay/Yellow')
    urlsa.append('https://api.lyrics.ovh/v1/Coldplay/Trouble')
    urlsa.append('https://api.lyrics.ovh/v1/Green Day/American Idiot')
    urlsa.append('https://api.lyrics.ovh/v1/Green Day/Basket Case')
    urlsa.append('https://api.lyrics.ovh/v1/Green Day/Warning')
    urlsa.append('https://api.lyrics.ovh/v1/Green Day/Minority')
    urlsa.append('https://api.lyrics.ovh/v1/Green Day/When I Come Around')
    urlsa.append('https://api.lyrics.ovh/v1/Green Day/She')
    urlsa.append('https://api.lyrics.ovh/v1/Green Day/King For A Day')
    urlsa.append('https://api.lyrics.ovh/v1/Green Day/Holiday')

    asyncio.run(work_through_urls(urlsa, _logger))
