import asyncio
import aiohttp
from aiohttp import ClientSession
import logging


def setup_log():
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    return logger


async def fetch_from_url(url: str, session: ClientSession, logger: logging.Logger, **kwargs):

    response = await session.get(url=url, **kwargs)

    logger.info(f"Response code for {url}: {response.status}")
    url_content = await response.text()

    return url_content


async def process_response(url: str, session: ClientSession, logger: logging.Logger, **kwargs):

    url_content = await fetch_from_url(url=url, session=session, logger=logger, **kwargs)

    print(f"Content for {url} is: {url_content}")

    return None


async def work_through_urls(url_list, logger, **kwargs):

    async with ClientSession() as session:
        fetch_tasks = []
        for url in url_list:
            fetch_tasks.append(process_response(url=url, session=session, logger=logger, **kwargs))

        await asyncio.gather(*fetch_tasks)


if __name__ == '__main__':

    _logger = setup_log()

    _logger.info("Starting process")

    urls = []
    urls.append('https://api.lyrics.ovh/v1/Coldplay/Yellow')
    urls.append('https://api.lyrics.ovh/v1/Coldplay/Trouble')
    urls.append('https://api.lyrics.ovh/v1/Green Day/American Idiot')
    urls.append('https://api.lyrics.ovh/v1/Green Day/Basket Case')
    urls.append('https://api.lyrics.ovh/v1/Green Day/Warning')
    urls.append('https://api.lyrics.ovh/v1/Green Day/Minority')
    urls.append('https://api.lyrics.ovh/v1/Green Day/When I Come Around')
    urls.append('https://api.lyrics.ovh/v1/Green Day/She')
    urls.append('https://api.lyrics.ovh/v1/Green Day/King For A Day')
    urls.append('https://api.lyrics.ovh/v1/Green Day/Holiday')

    asyncio.run(work_through_urls(urls, _logger))
