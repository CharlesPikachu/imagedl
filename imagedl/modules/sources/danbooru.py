'''
Function:
    Implementation of DanbooruImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import json_repair
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
    def _parsesearchresult(self, search_result: str):
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos = []
        for item in search_result:
            if not isinstance(item, dict) or (('file_url' not in item) and ('preview_file_url' not in item) and ('large_file_url' not in item)): continue
            file_url: str = item.get('file_url')
            if file_url and not file_url.startswith('http'): file_url = f"https:{file_url}"
            large_file_url: str = item.get('large_file_url')
            if large_file_url and not large_file_url.startswith('http'): large_file_url = f"https:{large_file_url}"
            preview_file_url: str = item.get('preview_file_url')
            if preview_file_url and not preview_file_url.startswith('http'): preview_file_url = f"https:{preview_file_url}"
            image_info = {
                'candidate_urls': [file_url, large_file_url, preview_file_url], 'raw_data': item, 'identifier': item.get('id') or item.get('md5') or file_url,
            }
            image_infos.append(image_info)
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits=1000, filters: dict = None, request_overrides: dict = None):
        request_overrides = request_overrides or {}
        base_url = 'https://danbooru.donmai.us/posts.json?'
        params = {'tags': keyword, 'limit': search_limits}
        if filters is not None: params.update(filters)
        search_urls = [base_url + urlencode(params, quote_via=quote)]
        return search_urls