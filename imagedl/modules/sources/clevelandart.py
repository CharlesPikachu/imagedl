'''
Function:
    Implementation of ClevelandArtImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import math
import json_repair
from ..utils import ImageInfo
from contextlib import suppress
from .base import BaseImageClient
from urllib.parse import quote, urlencode


'''ClevelandArtImageClient'''
class ClevelandArtImageClient(BaseImageClient):
    source = 'ClevelandImageClient'
    def __init__(self, **kwargs):
        super(ClevelandArtImageClient, self).__init__(**kwargs)
        self.default_search_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"}
        self.default_download_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos: list[ImageInfo] = []
        for item in search_result['data']:
            if not isinstance(item, dict) or not item.get('images') or not isinstance(item.get('images'), dict): continue
            with suppress(Exception): candidate_urls = []; candidate_urls = [item['images']['full']['url'], item['images']['print']['url'], item['images']['web']['url']]
            if not (candidate_urls := [u for u in candidate_urls if u and str(u).startswith('http')]): continue
            image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=candidate_urls, identifier=item.get('id') or candidate_urls[0]))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, filters, base_url = request_overrides or {}, filters or {}, "https://openaccess-api.clevelandart.org/api/artworks/?"
        (params := {"q": keyword, "has_image": 1, "limit": 50, "skip": 0}).update(filters)
        search_urls, page_size = [], int(params['limit'])
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params['skip'] = pn * page_size
            search_urls.append(base_url + urlencode(params, quote_via=quote))
        return search_urls