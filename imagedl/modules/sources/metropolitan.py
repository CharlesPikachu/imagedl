'''
Function:
    Implementation of MetropolitanImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import json_repair
from ..utils import ImageInfo
from .base import BaseImageClient


'''MetropolitanImageClient'''
class MetropolitanImageClient(BaseImageClient):
    source = 'MetropolitanImageClient'
    def __init__(self, **kwargs):
        super(MetropolitanImageClient, self).__init__(**kwargs)
        self.default_search_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"}
        self.default_download_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        if not (download_url := search_result.get("primaryImage") or search_result.get("primaryImageSmall")): return []
        image_infos = [ImageInfo(source=self.source, raw_data=search_result, candidate_download_urls=[download_url], identifier=download_url)]
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, filters, base_url = request_overrides or {}, filters or {}, "https://collectionapi.metmuseum.org/public/collection/v1/search?"
        (params := {"q": keyword, "hasImages": "true"}).update(filters)
        (resp := self.get(base_url, params=params, **request_overrides)).raise_for_status()
        object_ids = (dict(resp.json()).get("objectIDs") or [])[:int(search_limits * 1.2)]
        search_urls = [f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obj_id}" for obj_id in object_ids]
        return search_urls