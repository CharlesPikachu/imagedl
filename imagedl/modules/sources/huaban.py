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
from urllib.parse import quote, urlencode
from ..utils import searchdictbykey, ImageInfo


'''HuabanImageClient'''
class HuabanImageClient(BaseImageClient):
    source = 'HuabanImageClient'
    def __init__(self, **kwargs):
        kwargs['enable_search_curl_cffi'] = True
        super(HuabanImageClient, self).__init__(**kwargs)
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
        for file_dict in searchdictbykey(search_result, 'file'):
            if (not isinstance(file_dict, dict)) or (not (file_url := file_dict.get('url'))) or (not str(file_url).startswith('http')): continue
            image_infos.append(ImageInfo(source=self.source, raw_data=file_dict, candidate_download_urls=[file_url], identifier=file_url))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, filters, base_url = request_overrides or {}, filters or {}, 'https://huaban.com/v3/search/file?'
        (params := {'text': keyword, 'sort': 'all', 'limit': 40, 'page': 1, 'position': 'search_pins', 'fields': 'pins:PIN|total,facets,split_words,relations,rec_topic_material,topics'}).update(filters)
        search_urls, page_size = [], int(params['limit'])
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params['page'] = pn + 1
            search_urls.append(base_url + urlencode(params, quote_via=quote))
        return search_urls