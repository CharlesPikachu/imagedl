'''
Function:
    Implementation of FoodiesfeedImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
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
        for item in search_result.get('photos', []):
            if not isinstance(item, dict): continue
            candidate_urls = [item.get('master_url'), item.get('webp_url'), item.get('thumbnail_url')]
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
    def _constructsearchurls(self, keyword, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides = request_overrides or {}
        base_url = 'https://www.foodiesfeed.com/api/hybrid-photos?'
        params = {'page': 1, 'limit': 24, 'locale': 'zh', 'sort': 'relevance', 'requireTagMatch': 'false', 'apiLocation': 'hybrid-search', 'localExhausted': 'true', 'istockOffset': 24, 'totalLoaded': 24, 'searchQuery': keyword}
        if filters is not None: params.update(filters)
        search_urls, page_size = [], int(params['limit'])
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params['page'] = pn + 1
            params['istockOffset'] = pn * page_size
            params['totalLoaded'] = (pn + 1) * page_size
            search_url = base_url + urlencode(params, quote_via=quote)
            search_urls.append(search_url)
        return search_urls