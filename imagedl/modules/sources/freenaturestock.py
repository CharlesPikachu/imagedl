'''
Function:
    Implementation of FreeNatureStockImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import math
from bs4 import BeautifulSoup
from ..utils import ImageInfo
from urllib.parse import urljoin
from .base import BaseImageClient


'''FreeNatureStockImageClient'''
class FreeNatureStockImageClient(BaseImageClient):
    source = 'FreeNatureStockImageClient'
    def __init__(self, **kwargs):
        super(FreeNatureStockImageClient, self).__init__(**kwargs)
        self.default_search_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"}
        self.default_download_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        # parse with bs4
        soup, base_url = BeautifulSoup(search_result, "lxml"), "https://freenaturestock.com/"
        urls = [urljoin(base_url, img["src"]) for img in soup.select("#photo-previews img[src]") if img and img.get('src')]
        # parse search result
        image_infos: list[ImageInfo] = []
        for item in urls:
            if not isinstance(item, str) or (not item.startswith('http')): continue
            image_infos.append(ImageInfo(source=self.source, raw_data=search_result, candidate_download_urls=[item], identifier=item))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, search_urls, page_size, filters = request_overrides or {}, [], 40, filters or {}
        base_url = 'https://freenaturestock.com/page/{pn}/?s={keyword}'
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            search_urls.append(base_url.format(pn=pn, keyword=keyword))
        return search_urls