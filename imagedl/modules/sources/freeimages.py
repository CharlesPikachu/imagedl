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
        for item in search_result['data']['results']:
            if not isinstance(item, dict) or not (display_sizes := item.get('display_sizes', []) or []): continue
            candidate_urls = [ds.get('uri') for ds in display_sizes if isinstance(ds, dict) and str(ds.get('uri')).startswith('http')]
            if not candidate_urls: continue
            image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=candidate_urls, identifier=item.get('id') or candidate_urls[0]))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, filters, base_url = request_overrides or {}, filters or {}, 'https://geoapi.freeimages.com/istock/search/?'
        (params := {'phrase': keyword, 'page': 1, 'page_size': 18, 'graphical_styles': 'photography', 'lang': 'en-US'}).update(filters)
        search_urls, page_size = [], int(params['page_size'])
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params['page'] = pn + 1
            search_urls.append(base_url + urlencode(params, quote_via=quote))
        return search_urls