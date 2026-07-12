'''
Function:
    Implementation of WallhavenImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import math
import json_repair
from ..utils import ImageInfo
from .base import BaseImageClient
from urllib.parse import quote, urlencode


'''WallhavenImageClient'''
class WallhavenImageClient(BaseImageClient):
    source = 'WallhavenImageClient'
    def __init__(self, **kwargs):
        super(WallhavenImageClient, self).__init__(**kwargs)
        self.default_search_headers = {'Accept': 'application/json, text/plain, */*', 'Referer': 'https://wallhaven.cc/', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',}
        self.default_download_headers = {'Referer': 'https://wallhaven.cc/', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos: list[ImageInfo] = []
        for item in search_result.get('data', []) or []:
            if not isinstance(item, dict): continue
            candidate_download_urls = [item.get('path'), (thumbs := item.get('thumbs', {}) or {}).get('original'), thumbs.get('large'), thumbs.get('small'),]
            candidate_download_urls = [str(url) for url in candidate_download_urls if url and str(url).startswith('http')]
            if not (candidate_download_urls := list(dict.fromkeys(candidate_download_urls))): continue
            image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=candidate_download_urls, identifier=str(item.get('id') or candidate_download_urls[0])))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None) -> list[str]:
        filters, request_overrides, base_url = dict(filters or {}), request_overrides or {}, 'https://wallhaven.cc/api/v1/search?'
        (params := {'q': keyword, 'categories': '111', 'purity': '100', 'sorting': 'relevance', 'order': 'desc', 'page': 1,}).update(filters)
        search_urls, num_pages = [], math.ceil(search_limits * 1.2 / 24)
        for page_idx in range(num_pages):
            params['page'] = page_idx + 1
            search_urls.append(base_url + urlencode(params, quote_via=quote, doseq=True))
        return search_urls