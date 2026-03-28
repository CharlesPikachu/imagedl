'''
Function:
    Implementation of SogouImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import math
import time
import json_repair
from ..utils import ImageInfo
from .base import BaseImageClient
from urllib.parse import quote, urlencode


'''SogouImageClient'''
class SogouImageClient(BaseImageClient):
    source = 'SogouImageClient'
    def __init__(self, **kwargs):
        super(SogouImageClient, self).__init__(**kwargs)
        self.default_search_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', 'Host': 'pic.sogou.com', 'Sec-Ch-Ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"', 'Sec-Fetch-Site': 'same-origin', 
            'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'X-Time4p': str(int(time.time() * 1000)), 'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7', 
        }
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos: list[ImageInfo] = []
        if ('data' not in search_result) or ('items' not in (search_result.get('data') or {})): return image_infos
        for item in ((search_result.get('data', {}) or {}).get('items', []) or []):
            if not isinstance(item, dict): continue
            candidate_urls = [item.get('picUrl'), item.get('oriPicUrl'), item.get('locImageLink'), item.get('thumbUrl')]
            if not (candidate_urls := [c for c in candidate_urls if c and str(c).startswith('http')]): continue
            image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=candidate_urls, identifier=item.get('mf_id') or candidate_urls[0]))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, filters, base_url = request_overrides or {}, filters or {}, 'https://pic.sogou.com/napi/pc/searchList?'
        (params := {'mode': '1', 'start': '384', 'xml_len': '48', 'query': keyword, 'channel': 'pc_pic', 'scene': 'pic_result'}).update(filters)
        search_urls, page_size = [], int(params['xml_len'])
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params['start'] = str(int(page_size * pn))
            search_urls.append(base_url + urlencode(params, quote_via=quote))
        return search_urls