'''
Function:
    Implementation of CaraImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import math
import json_repair
from ..utils import ImageInfo
from typing_extensions import Unpack
from urllib.parse import quote, urlencode, urljoin
from .base import BaseImageClient, BaseImageClientKwargs


'''CaraImageClient'''
class CaraImageClient(BaseImageClient):
    source = 'CaraImageClient'
    def __init__(self, **kwargs: Unpack[BaseImageClientKwargs]):
        super(CaraImageClient, self).__init__(**kwargs)
        self.default_search_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36", "Accept": "application/json", "Referer": "https://cara.app/"}
        self.default_download_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36", "Referer": "https://cara.app/"}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        # parse json text in safety
        search_result: list = json_repair.loads(search_result)
        # parse search result
        image_infos: list[ImageInfo] = []
        for item in search_result:
            if not isinstance(item, dict): continue
            for idx, image in enumerate(item.get('images', [])):
                if not isinstance(image, dict) or not (image_url := image.get('src')): continue
                if not (image_url := urljoin('https://images.cara.app/', str(image_url))).startswith('http'): continue
                image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=[image_url], identifier=f"{item.get('id') or image_url}:{idx}"))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, filters, base_url = request_overrides or {}, filters or {}, 'https://cara.app/api/search/portfolio-posts?'
        (params := {'q': keyword, 'sortBy': 'Top', 'take': 24, 'skip': 0}).update(filters)
        search_urls, page_size = [], min(max(int(params['take']), 1), 24); params['take'] = page_size
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params['skip'] = pn * page_size
            search_urls.append(base_url + urlencode(params, quote_via=quote))
        return search_urls