import asyncio
import aiohttp
from app.config import NAVER_API_ID, NAVER_API_SECRET, YOUTUBE_API_KEY
from pprint import pprint
from itertools import chain


class YoutubeVideosScraper:
    base_url = 'https://www.googleapis.com/youtube/v3'
    
    def __init__(self, n_display=1, n_pages=1) -> None:
        self.n_display = n_display
        self.n_pages = n_pages
    
    async def fetch(self, session, url):
        pass
    
    async def run(self, keyword):
        pass


class NaverImageScrapper:
    base_url = 'https://openapi.naver.com/v1/search/image'
    header = {
        'X-Naver-Client-Id': NAVER_API_ID,
        'X-Naver-Client-Secret': NAVER_API_SECRET
    }
    
    def _make_url(self, keyword, n_displays, start):
        """start 항목에 따라 api url이 바뀜"""
        url = f'{self.base_url}?query={keyword}&display={n_displays}&start={start}'
        return url
    
    async def fetch(self, session, url):
        async with session.get(url, headers=self.header) as response:
            if response.status == 200:
                result = await response.json()
                return result['items']
    
    async def search(self, keyword, n_displays, n_pages):
        urls = [
            self._make_url(keyword, n_displays, start=i * n_displays + 1)
            for i in range(n_pages)
        ]
        async with aiohttp.ClientSession() as session:
            all_data = await asyncio.gather(
                *[self.fetch(session, url) for url in urls]
            )
        return list(chain(*all_data))
    
    def run(self, keyword, n_displays, n_pages):
        return asyncio.run(self.search(keyword, n_displays, n_pages))


if __name__ == '__main__':
    scrapper = NaverImageScrapper()
    pprint(
        scrapper.run(
            keyword='twice',
            n_displays=10,
            n_pages=2
        )
    )
