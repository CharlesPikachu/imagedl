'''
Function:
    Implementation of FinnaImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import math
import json_repair
from ..utils import ImageInfo
from typing_extensions import Unpack
from urllib.parse import quote, urlencode, urljoin
from .base import BaseImageClient, BaseImageClientKwargs


'''FinnaImageClient'''
class FinnaImageClient(BaseImageClient):
    source = 'FinnaImageClient'
    def __init__(self, **kwargs: Unpack[BaseImageClientKwargs]):
        super(FinnaImageClient, self).__init__(**kwargs)
        self.default_search_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36", "Accept": "application/json"}
        self.default_download_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos: list[ImageInfo] = []
        for item in search_result.get('records', []):
            if not isinstance(item, dict): continue
            candidate_urls = []
            for image in item.get('images', []):
                if not (image_url := image.get('url') if isinstance(image, dict) else image): continue
                if (image_url := urljoin('https://api.finna.fi/', str(image_url))).startswith('http'): candidate_urls.append(image_url)
            if not (candidate_urls := list(dict.fromkeys(candidate_urls))): continue
            image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=candidate_urls, identifier=item.get('id') or candidate_urls[0]))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, filters, base_url = request_overrides or {}, filters or {}, 'https://api.finna.fi/v1/search?'
        (params := {'lookfor': keyword, 'type': 'AllFields', 'page': 1, 'limit': 100, 'field[]': ['id', 'title', 'images'], 'filter[]': ['online_boolean:"1"', 'format:"0/Image/"']}).update(filters)
        search_urls, page_size = [], min(max(int(params['limit']), 1), 100); params['limit'] = page_size
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params['page'] = pn + 1
            search_urls.append(base_url + urlencode(params, doseq=True, quote_via=quote))
        return search_urls