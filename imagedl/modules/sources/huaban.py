'''
Function:
    Implementation of HuabanImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import math
import json_repair
from .base import BaseImageClient
from ..utils import searchdictbykey
from urllib.parse import quote, urlencode


'''HuabanImageClient'''
class HuabanImageClient(BaseImageClient):
    source = 'HuabanImageClient'
    def __init__(self, **kwargs):
        kwargs['enable_search_curl_cffi'] = True
        super(HuabanImageClient, self).__init__(**kwargs)
        self.default_search_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str):
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos, file_dicts = [], searchdictbykey(search_result, 'file')
        for file_dict in file_dicts:
            if not isinstance(file_dict, dict): continue
            file_url = file_dict.get('url')
            if not file_url or not str(file_url).startswith('http'): continue
            image_info = {
                'candidate_urls': [file_url], 'raw_data': file_dict, 'identifier': file_url,
            }
            image_infos.append(image_info)
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword, search_limits=1000, filters: dict = None, request_overrides: dict = None):
        request_overrides = request_overrides or {}
        base_url = 'https://huaban.com/v3/search/file?'
        params = {'text': keyword, 'sort': 'all', 'limit': 40, 'page': 1, 'position': 'search_pins', 'fields': 'pins:PIN|total,facets,split_words,relations,rec_topic_material,topics'}
        if filters is not None: params.update(filters)
        search_urls, page_size = [], int(params['limit'])
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params['page'] = pn + 1
            search_url = base_url + urlencode(params, quote_via=quote)
            search_urls.append(search_url)
        return search_urls