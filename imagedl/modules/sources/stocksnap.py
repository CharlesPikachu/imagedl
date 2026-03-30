'''
Function:
    Implementation of StockSnapImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import math
import json_repair
from ..utils import ImageInfo
from .base import BaseImageClient
from urllib.parse import quote, urlencode


'''StockSnapImageClient'''
class StockSnapImageClient(BaseImageClient):
    source = 'StockSnapImageClient'
    def __init__(self, **kwargs):
        super(StockSnapImageClient, self).__init__(**kwargs)
        self.default_search_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos: list[ImageInfo] = []
        for item in (search_result.get('images', []) or []):
            if not isinstance(item, dict) or not (preview_urls := item.get('preview_urls', {}) or {}): continue
            candidate_urls = [preview_urls.get('large'), preview_urls.get('medium'), preview_urls.get('small')]
            if not (candidate_urls := [c for c in candidate_urls if c and str(c).startswith('http')]): continue
            image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=candidate_urls, identifier=item.get('id') or candidate_urls[0], description=item.get('caption')))
        for item in (search_result.get('results', []) or []):
            if not isinstance(item, dict) or not (img_id := item.get('img_id')): continue
            image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=[f'https://cdn.stocksnap.io/img-thumbs/280h/{img_id}.jpg'], identifier=img_id))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, base_url, filters = request_overrides or {}, 'https://api.gettyimages.com/v3/affiliates/search/images?', filters or {}
        (resp := self.get(f'https://stocksnap.io/search/{keyword}', **request_overrides)).raise_for_status()
        api_key, search_urls, page_size = re.search(r"\b(?:apiKey|api_key|API_KEY)\b\s*[:=]\s*['\"]([^'\"]+)['\"]", resp.text, re.I).group(1), [], 40
        if 'Api-Key' not in self.default_headers: self.default_headers['Api-Key'] = api_key
        if 'Api-Key' not in self.default_search_headers: self.default_search_headers['Api-Key'] = api_key
        if 'Api-Key' not in self.default_download_headers: self.default_download_headers['Api-Key'] = api_key
        search_urls.append(base_url + urlencode({'style': 'photography', 'phrase': keyword}, quote_via=quote))
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            search_urls.append(f"https://stocksnap.io/api/search-photos/{quote(keyword, safe='')}/relevance/desc/{pn+1}")
        return search_urls