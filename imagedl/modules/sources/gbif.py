'''
Function:
    Implementation of GBIFImageClient
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


'''GBIFImageClient'''
class GBIFImageClient(BaseImageClient):
    source = 'GBIFImageClient'
    def __init__(self, **kwargs):
        super(GBIFImageClient, self).__init__(**kwargs)
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
        image_urls = [img for result in search_result.get("results", []) if isinstance(result, dict) and (img := next((m["identifier"] for m in result.get("media", []) if isinstance(m, dict) and m.get("type") == "StillImage" and "identifier" in m), None)) is not None]
        for item in image_urls:
            image_infos.append(ImageInfo(source=self.source, raw_data=search_result, candidate_download_urls=[item], identifier=item))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, filters, base_url = request_overrides or {}, filters or {}, "https://api.gbif.org/v1/occurrence/search?"
        (params := {"q": keyword, "mediaType": "StillImage", "limit": 20, "offset": 0}).update(filters)
        search_urls, page_size = [], int(params['limit'])
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params['offset'] = pn * page_size
            search_urls.append(base_url + urlencode(params, quote_via=quote))
        return search_urls