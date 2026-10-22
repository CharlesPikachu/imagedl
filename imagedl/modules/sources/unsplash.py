'''
Function:
    Implementation of UnsplashImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import math
import json_repair
from ..utils import ImageInfo
from typing_extensions import Unpack
from urllib.parse import quote, urlencode
from .base import BaseImageClient, BaseImageClientKwargs


'''UnsplashImageClient'''
class UnsplashImageClient(BaseImageClient):
    source = 'UnsplashImageClient'
    def __init__(self, **kwargs: Unpack[BaseImageClientKwargs]):
        super(UnsplashImageClient, self).__init__(**kwargs)
        self.default_search_headers = {"Pragma": "no-cache", "Priority": "u=1, i", "Referer": "https://unsplash.com/", "Sec-Ch-Ua": '"Google Chrome";v="155", "Chromium";v="155", "Not(A:Brand";v="24"', "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": '"Windows"', "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36", "X-Client-Version": "f8090b35b87ce58e923e2159590d30a40cb6935a", "Accept": "*/*", "Accept-Encoding": "gzip, deflate, br, zstd", "Accept-Language": "en-US", "Cache-Control": "no-cache", "Client-Geo-Region": "us",}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos: list[ImageInfo] = []
        for item in (search_result.get('results', []) or []):
            if not isinstance(item, dict) or not (candidate_urls := list((item.get('urls', {}) or {}).values())): continue
            if not (candidate_urls := [c for c in candidate_urls if c and str(c).startswith('http')]): continue
            image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=candidate_urls, identifier=item.get('id') or candidate_urls[0]))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, base_url, filters = request_overrides or {}, 'https://unsplash.com/napi/search/photos?', filters or {}
        (params := {'query': keyword, 'page': 1, 'per_page': 20}).update(filters)
        search_urls, page_size = [], int(params['per_page'])
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params['page'] = pn + 1
            search_urls.append(base_url + urlencode(params, quote_via=quote))
        return search_urls