'''
Function:
    Implementation of FreeImagesImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import math
import json_repair
from ..utils import ImageInfo
from .base import BaseImageClient
from urllib.parse import urlencode, quote


'''FreeImagesImageClient'''
class FreeImagesImageClient(BaseImageClient):
    source = 'FreeImagesImageClient'
    def __init__(self, **kwargs):
        super(FreeImagesImageClient, self).__init__(**kwargs)
        self.default_search_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36", "accept": "application/json", "referer": "https://www.istockphoto.com/search/2/image-film"}
        self.default_download_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36", "referer": "https://www.istockphoto.com/"}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos: list[ImageInfo] = []
        for item in (search_result.get('gallery', {}) or {}).get('assets', []):
            if not isinstance(item, dict) or item.get('assetType') != 'image' or not str(item.get('thumbUrl', '')).startswith('http'): continue
            image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=[item.get('thumbUrl')], identifier=item.get('assetId') or item.get('id') or item.get('thumbUrl')))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, filters, base_url = request_overrides or {}, filters or {}, 'https://www.istockphoto.com/search/2/image-film?'
        (params := {'phrase': keyword, 'page': 1}).update(filters)
        search_urls, page_size = [], 60
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params['page'] = pn + 1
            search_urls.append(base_url + urlencode(params, quote_via=quote))
        return search_urls