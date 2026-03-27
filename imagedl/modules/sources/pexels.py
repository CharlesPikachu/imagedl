'''
Function:
    Implementation of PexelsImageClient
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


'''PexelsImageClient'''
class PexelsImageClient(BaseImageClient):
    source = 'PexelsImageClient'
    def __init__(self, **kwargs):
        super(PexelsImageClient, self).__init__(**kwargs)
        self.default_search_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36", "secret-key": "H2jk9uKnhRmL6WPwh89zBezWvr"}
        self.default_download_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36", "secret-key": "H2jk9uKnhRmL6WPwh89zBezWvr"}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)['data']
        # parse search result
        image_infos: list[ImageInfo] = []
        for item in search_result:
            if (not isinstance(item, dict)) or ('attributes' not in item) or ('image' not in item['attributes']): continue
            if not (image_attribute := item['attributes']['image']) or not isinstance(image_attribute, dict): continue
            candidate_urls = [image_attribute.get('download_link'), image_attribute.get('large'), image_attribute.get('medium'), image_attribute.get('small')]
            if not (candidate_urls := [c for c in candidate_urls if c and str(c).startswith('http')]): continue
            image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=candidate_urls, identifier=item.get('id') or candidate_urls[0]))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, filters, base_url = request_overrides or {}, filters or {}, 'https://www.pexels.com/en-us/api/v3/search/photos?'
        (params := {'query': keyword, 'page': 1, 'per_page': 24, 'seo_tags': 'true'}).update(filters)
        search_urls, page_size = [], int(params['per_page'])
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params['page'] = pn + 1
            search_urls.append(base_url + urlencode(params, quote_via=quote))
        return search_urls