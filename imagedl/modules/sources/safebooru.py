'''
Function:
    Implementation of SafebooruImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import json_repair
from .base import BaseImageClient
from urllib.parse import quote, urlencode


'''SafebooruImageClient'''
class SafebooruImageClient(BaseImageClient):
    source = 'SafebooruImageClient'
    def __init__(self, **kwargs):
        super(SafebooruImageClient, self).__init__(**kwargs)
        self.default_search_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str):
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos = []
        for item in search_result:
            if not isinstance(item, dict) or (('file_url' not in item) and ('preview_url' not in item) and ('sample_url' not in item)): continue
            file_url: str = item.get('file_url')
            if file_url and not file_url.startswith('http'): file_url = f"https:{file_url}"
            sample_url: str = item.get('sample_url')
            if sample_url and not sample_url.startswith('http'): sample_url = f"https:{sample_url}"
            preview_url: str = item.get('preview_url')
            if preview_url and not preview_url.startswith('http'): preview_url = f"https:{preview_url}"
            image_info = {
                'candidate_urls': [file_url, sample_url, preview_url], 'raw_data': item, 'identifier': item.get('id') or item.get('image') or item.get('hash') or file_url,
            }
            image_infos.append(image_info)
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits=1000, filters: dict = None, request_overrides: dict = None):
        request_overrides = request_overrides or {}
        base_url = 'https://safebooru.org/index.php?'
        params = {'page': 'dapi', 's': 'post', 'q': 'index', 'json': '1', 'tags': keyword, 'limit': search_limits}
        if filters is not None: params.update(filters)
        search_urls = [base_url + urlencode(params, quote_via=quote)]
        return search_urls