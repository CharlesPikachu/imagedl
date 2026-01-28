'''
Function:
    Implementation of FoodiesfeedImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import math
import json_repair
from .base import BaseImageClient
from urllib.parse import quote, urlencode


'''FoodiesfeedImageClient'''
class FoodiesfeedImageClient(BaseImageClient):
    source = 'FoodiesfeedImageClient'
    def __init__(self, **kwargs):
        super(FoodiesfeedImageClient, self).__init__(**kwargs)
        self.default_search_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str):
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos = []
        for item in search_result.get('images', []):
            if not isinstance(item, dict): continue
            candidate_urls = [ds['uri'] for ds in item['display_sizes']]
            candidate_urls = [url for url in candidate_urls if url and str(url).startswith('http')]
            candidate_urls = list(set(candidate_urls))
            if not candidate_urls: continue
            image_info = {
                'candidate_urls': candidate_urls, 'raw_data': item, 'identifier': item['id'] if 'id' in item else candidate_urls[0],
            }
            image_infos.append(image_info)
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword, search_limits=1000, filters: dict = None, request_overrides: dict = None):
        resp = self.get(f'https://www.foodiesfeed.com/?s={keyword}', **request_overrides)
        resp.raise_for_status()
        m = re.search(r'data-api-key\s*=\s*["\']([^"\']+)["\']', resp.text)
        api_key = m.group(1) if m else None
        request_overrides = request_overrides or {}
        base_url = 'https://api.gettyimages.com/v3/search/images/creative?'
        params = {
            'embed_content_only': 'false', 'exclude_nudity': 'true', 'fields': 'referral_destinations,preview,detail_set', 'graphical_styles': 'photography', 'include_related_searches': 'true', 
            'orientations': 'horizontal', 'page': 1, 'page_size': 20, 'phrase': keyword, 'safe_search': 'true', 'sort_order': 'best_match', 'facet_max_count': 300,
        }
        if filters is not None: params.update(filters)
        search_urls, page_size = [], int(params['page_size'])
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params['page'] = pn + 1
            search_url = base_url + urlencode(params, quote_via=quote)
            search_urls.append({'url': search_url, 'inputs': {'headers': {'api-key': api_key}}, 'method': 'get'})
        return search_urls