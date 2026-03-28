'''
Function:
    Implementation of SafebooruImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import json_repair
from ..utils import ImageInfo
from .base import BaseImageClient
from urllib.parse import quote, urlencode


'''SafebooruImageClient'''
class SafebooruImageClient(BaseImageClient):
    source = 'SafebooruImageClient'
    def __init__(self, **kwargs):
        super(SafebooruImageClient, self).__init__(**kwargs)
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
        for item in search_result:
            if not isinstance(item, dict) or not any(k in item for k in ('file_url', 'preview_url', 'sample_url')): continue
            file_url, sample_url, preview_url = (u if not u or str(u).startswith('http') else f'https:{u}' for u in (item.get('file_url'), item.get('sample_url'), item.get('preview_url')))
            if not (candidate_urls := [u for u in [file_url, sample_url, preview_url] if u]): continue
            image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=candidate_urls, identifier=item.get('id') or item.get('image') or item.get('hash') or candidate_urls[0]))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, base_url, filters = request_overrides or {}, 'https://safebooru.org/index.php?', filters or {}
        (params := {'page': 'dapi', 's': 'post', 'q': 'index', 'json': '1', 'tags': keyword, 'limit': search_limits}).update(filters)
        return [base_url + urlencode(params, quote_via=quote)]