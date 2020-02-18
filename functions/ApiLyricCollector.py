import asyncio
from aiohttp import ClientSession
import logging
import json
import re


class ApiLyricCollector:

    def __init__(self, artist, recs, logger):
        self.api_url = "https://api.lyrics.ovh/v1/"
        self.artist = artist
        self.recs = recs
        self.logger = logger
        self.count_arr = []

    def run_fetch_from_api_lyrics(self):

        urls = []

        for r in self.recs:
            _build_url = f"{self.api_url}{self.artist}/{r}"
            urls.append(_build_url)

        asyncio.run(self.work_through_urls(urls, self.logger))

    def count_words(self, url_content):

        _json = json.loads(url_content)

        _word_count = len(re.findall(r'\S+', _json["lyrics"]))

        return _word_count

    async def fetch_from_url(self, url: str, session: ClientSession, logger: logging.Logger):

        response = await session.get(url=url)
        url_content = await response.text()

        return url_content, response.status

    async def process_response(self, url: str, session: ClientSession, logger: logging.Logger):

        url_content, url_response = await self.fetch_from_url(url=url, session=session, logger=logger)

        if str(url_response) == "200":
            _wrd_count = self.count_words(url_content)

            self.count_arr.append(_wrd_count)

    async def work_through_urls(self, url_list, logger):

        async with ClientSession() as session:
            fetch_tasks = []
            for url in url_list:
                fetch_tasks.append(self.process_response(url=url, session=session, logger=logger))

            await asyncio.gather(*fetch_tasks)


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
