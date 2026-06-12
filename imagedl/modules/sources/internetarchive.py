'''
Function:
    Implementation of InternetArchiveImageClient
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


'''InternetArchiveImageClient'''
class InternetArchiveImageClient(BaseImageClient):
    source = 'InternetArchiveImageClient'
    def __init__(self, **kwargs):
        super(InternetArchiveImageClient, self).__init__(**kwargs)
        self.default_search_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36", "Accept": "application/json,text/plain,*/*"}
        self.default_download_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos: list[ImageInfo] = []
        for item in ((search_result.get("response") or {}).get("docs") or []):
            if not isinstance(item, dict) or not (identifier := item.get("identifier")): continue
            candidate_urls = [f"https://archive.org/services/img/{identifier}"]
            image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=candidate_urls, identifier=str(identifier)))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, filters, base_url = request_overrides or {}, filters or {}, "https://archive.org/advancedsearch.php?"
        (params := {"q": f"({keyword}) AND mediatype:image", "fl[]": ["identifier", "title", "creator", "date", "mediatype"], "rows": 50, "page": 1, "output": "json"}).update(filters)
        search_urls, page_size = [], int(params['rows'])
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params['page'] = pn + 1
            search_urls.append(base_url + urlencode(params, doseq=True, quote_via=quote))
        return search_urls