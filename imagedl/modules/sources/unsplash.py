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
from .base import BaseImageClient
from urllib.parse import quote, urlencode


'''UnsplashImageClient'''
class UnsplashImageClient(BaseImageClient):
    source = 'UnsplashImageClient'
    def __init__(self, **kwargs):
        super(UnsplashImageClient, self).__init__(**kwargs)
        self.default_search_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US',
        }
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str):
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos = []
        for item in search_result.get('results', []):
            if not isinstance(item, dict): continue
            candidate_urls = list(item.get('urls', {}).values())
            if not candidate_urls: continue
            image_info = {
                'candidate_urls': candidate_urls, 'raw_data': item, 'identifier': item['id'] if 'id' in item else candidate_urls[0],
            }
            image_infos.append(image_info)
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword, search_limits=1000, filters: dict = None, request_overrides: dict = None):
        request_overrides = request_overrides or {}
        base_url = 'https://unsplash.com/napi/search/photos?'
        params = {'query': keyword, 'page': 1, 'per_page': 20}
        if filters is not None: params.update(filters)
        search_urls, page_size = [], int(params['per_page'])
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params['page'] = pn + 1
            search_url = base_url + urlencode(params, quote_via=quote)
            search_urls.append(search_url)
        return search_urls