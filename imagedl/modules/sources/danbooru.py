'''
Function:
    Implementation of DanbooruImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import json_repair
from ..utils import ImageInfo
from .base import BaseImageClient
from urllib.parse import quote, urlencode


'''DanbooruImageClient'''
class DanbooruImageClient(BaseImageClient):
    source = 'DanbooruImageClient'
    def __init__(self, **kwargs):
        super(DanbooruImageClient, self).__init__(**kwargs)
        self.default_search_headers = {}
        self.default_download_headers = {}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos: list[ImageInfo] = []
        for item in search_result:
            if not isinstance(item, dict) or (('file_url' not in item) and ('preview_file_url' not in item) and ('large_file_url' not in item)): continue
            if (file_url := item.get('file_url')) and (not str(file_url).startswith('http')): file_url = f"https:{file_url}"
            if (large_file_url := item.get('large_file_url')) and (not str(large_file_url).startswith('http')): large_file_url = f"https:{large_file_url}"
            if (preview_file_url := item.get('preview_file_url')) and (not str(preview_file_url).startswith('http')): preview_file_url = f"https:{preview_file_url}"
            candidate_urls = [url for url in [file_url, large_file_url, preview_file_url] if url]
            image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=candidate_urls, identifier=item.get('id') or item.get('md5') or candidate_urls[0]))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, filters = request_overrides or {}, filters or {}
        base_url = 'https://danbooru.donmai.us/posts.json?'
        (params := {'tags': keyword, 'limit': search_limits}).update(filters)
        search_urls = [base_url + urlencode(params, quote_via=quote)]
        return search_urls