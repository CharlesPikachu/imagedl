'''
Function:
    Implementation of INaturalistImageClient
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


'''INaturalistImageClient'''
class INaturalistImageClient(BaseImageClient):
    source = 'INaturalistImageClient'
    def __init__(self, **kwargs):
        super(INaturalistImageClient, self).__init__(**kwargs)
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
        for item in search_result['results']:
            if not isinstance(item, dict) or not (photos := item.get('photos')) or not isinstance(item.get('photos'), list): continue
            for photo in photos:
                if not isinstance(photo, dict): continue
                candidate_urls = [(photo.get("url", "") or "").replace("square", "large"), (photo.get("url", "") or "").replace("square", "medium"), item.get("url")]
                if not (candidate_urls := [c for c in candidate_urls if c and str(c).startswith('http')]): continue
                image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=candidate_urls, identifier=item.get('id') or candidate_urls[0]))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, filters, base_url = request_overrides or {}, filters or {}, "https://api.inaturalist.org/v1/observations?"
        (params := {"q": keyword, "photos": "true", "quality_grade": "research", "per_page": 50, "order": "desc", "order_by": "votes", "page": 1}).update(filters)
        search_urls, page_size = [], int(params["per_page"])
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params['page'] = pn + 1
            search_urls.append(base_url + urlencode(params, quote_via=quote))
        return search_urls