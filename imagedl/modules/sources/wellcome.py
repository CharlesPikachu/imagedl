'''
Function:
    Implementation of WellcomeImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import math
import json_repair
from ..utils import ImageInfo
from .base import BaseImageClient
from urllib.parse import urlencode


'''WellcomeImageClient'''
class WellcomeImageClient(BaseImageClient):
    source = 'WellcomeImageClient'
    def __init__(self, **kwargs):
        super(WellcomeImageClient, self).__init__(**kwargs)
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
        wellcome_info_url_to_image_url_func = lambda info_url, max_size=1200: ("" if not info_url else (f"{info_url[:-len('/info.json')]}/full/!{max_size},{max_size}/0/default.jpg" if str(info_url).endswith("/info.json") else (f"{str(info_url[:-len('info.json')]).rstrip('/')}/full/!{max_size},{max_size}/0/default.jpg" if str(info_url).endswith("info.json") else info_url)))
        for item in search_result['results']:
            if not isinstance(item, dict) or not (image_id := item.get("id")): continue
            candidate_urls = [wellcome_info_url_to_image_url_func((item.get("thumbnail") or {}).get("url"))]
            image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=candidate_urls, identifier=image_id))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        base_url = "https://api.wellcomecollection.org/catalogue/v2/images?"
        request_overrides, search_urls, page_size, filters = request_overrides or {}, [], 25, filters or {}
        (params := {"query": keyword, "page": 1, "pageSize": page_size}).update(filters)
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params["page"] = pn + 1
            search_urls.append(base_url + urlencode(params))
        return search_urls