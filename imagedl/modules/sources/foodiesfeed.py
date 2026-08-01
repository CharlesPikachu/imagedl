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
from ..utils import ImageInfo
from .base import BaseImageClient
from urllib.parse import quote, urlencode


'''FoodiesfeedImageClient'''
class FoodiesfeedImageClient(BaseImageClient):
    source = 'FoodiesfeedImageClient'
    def __init__(self, **kwargs):
        kwargs.setdefault('enable_search_curl_cffi', True)
        super(FoodiesfeedImageClient, self).__init__(**kwargs)
        self.default_search_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
            'Accept': '*/*', 'Accept-Language': 'en-US,en;q=0.9', 'Referer': 'https://www.foodiesfeed.com/',
        }
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36', 'Referer': 'https://www.foodiesfeed.com/',}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos: list[ImageInfo] = []
        for item in (search_result.get('photos', []) or []):
            if not isinstance(item, dict): continue
            candidate_urls = [item.get('master_url'), item.get('webp_url'), item.get('thumbnail_url')]
            if not (candidate_urls := list(dict.fromkeys([url for url in candidate_urls if url and str(url).startswith('http')]))): continue
            image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=candidate_urls, identifier=item.get('id') or candidate_urls[0]))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, filters, base_url = request_overrides or {}, filters or {}, 'https://www.foodiesfeed.com/api/hybrid-photos?'
        (params := {'page': 1, 'limit': 24, 'locale': 'en', 'sort': 'relevance', 'requireTagMatch': 'false', 'apiLocation': 'hybrid-search', 'localExhausted': 'false', 'istockOffset': 4, 'totalLoaded': 48, 'searchQuery': keyword, 'istockSearchQuery': keyword}).update(filters)
        search_urls, page_size = [], int(params['limit'])
        for pn in range((page_num := math.ceil(search_limits * 1.2 / page_size))):
            params['page'] = pn + 1; search_urls.append(search_url := base_url + urlencode(params, quote_via=quote))
            if pn == page_num - 1: continue # no need to request the current page if there is no next page
            try:
                (resp := self.get(search_url, **request_overrides)).raise_for_status()
                search_result: dict = json_repair.loads(resp.text)
                params['localExhausted'] = str(search_result.get('localExhausted', params['localExhausted'])).lower()
                params['istockOffset'] = search_result.get('istockOffset', params['istockOffset'])
                params['totalLoaded'] = search_result.get('totalLoaded', params['totalLoaded'])
                resp.close()
            except Exception: break
        return search_urls