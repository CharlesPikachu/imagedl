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
from .base import BaseImageClient
from urllib.parse import quote, urlencode


'''PexelsImageClient'''
class PexelsImageClient(BaseImageClient):
    source = 'PexelsImageClient'
    def __init__(self, **kwargs):
        super(PexelsImageClient, self).__init__(**kwargs)
        self.default_search_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
            "secret-key": "H2jk9uKnhRmL6WPwh89zBezWvr"
        }
        self.default_download_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
            "secret-key": "H2jk9uKnhRmL6WPwh89zBezWvr"
        }
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str):
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)['data']
        # parse search result
        image_infos = []
        for item in search_result:
            if not isinstance(item, dict) or ('attributes' not in item) or ('image' not in item['attributes']): continue
            image_attribute: dict = item['attributes']['image']
            if not (image_attribute.get('download_link') or image_attribute.get('large') or image_attribute.get('medium') or image_attribute.get('small')): continue
            candidate_urls = [image_attribute.get('download_link'), image_attribute.get('large'), image_attribute.get('medium'), image_attribute.get('small')]
            candidate_urls = [c for c in candidate_urls if c]
            image_info = {
                'candidate_urls': candidate_urls, 'raw_data': item, 'identifier': item.get('id') or item['attributes'].get('id') or candidate_urls[0],
            }
            image_infos.append(image_info)
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword, search_limits=1000, filters: dict = None, request_overrides: dict = None):
        request_overrides = request_overrides or {}
        base_url = 'https://www.pexels.com/en-us/api/v3/search/photos?'
        params = {'query': keyword, 'page': 1, 'per_page': 24, 'seo_tags': 'true'}
        if filters is not None: params.update(filters)
        search_urls, page_size = [], int(params['per_page'])
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params['page'] = pn + 1
            search_url = base_url + urlencode(params, quote_via=quote)
            search_urls.append(search_url)
        return search_urls