'''
Function:
    Implementation of AICImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import json_repair
from ..utils import ImageInfo
from .base import BaseImageClient
from urllib.parse import urlencode, quote


'''AICImageClient'''
class AICImageClient(BaseImageClient):
    source = 'AICImageClient'
    def __init__(self, **kwargs):
        super(AICImageClient, self).__init__(**kwargs)
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
        base_url = (search_result.get("config", {}) or {}).get("iiif_url", "https://www.artic.edu/iiif/2")
        for item in search_result['data']:
            if not isinstance(item, dict) or not (image_id := item.get('image_id')): continue
            download_url = f"{base_url}/{image_id}/full/843,/0/default.jpg"
            image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=[download_url], identifier=image_id))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, filters, base_url = request_overrides or {}, filters or {}, 'https://api.artic.edu/api/v1/artworks/search?'
        (params := {"q": keyword, "query[term][is_public_domain]": "true", "fields": "id,title,image_id,is_public_domain", "limit": int(search_limits * 1.2)}).update(filters)
        return [base_url + urlencode(params, quote_via=quote)]