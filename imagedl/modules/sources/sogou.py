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
from .base import BaseImageClient
from urllib.parse import quote, urlencode


'''SogouImageClient'''
class SogouImageClient(BaseImageClient):
    source = 'SogouImageClient'
    def __init__(self, **kwargs):
        super(SogouImageClient, self).__init__(**kwargs)
        self.default_search_headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
            'Host': 'pic.sogou.com',
            'Sec-Ch-Ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Time4p': str(int(time.time() * 1000)),
        }
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str):
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos = []
        for item in search_result.get('data', {}).get('items', []):
            candidate_urls = []
            if ('picUrl' in item) and isinstance(item['picUrl'], str) and item['picUrl'].strip():
                candidate_urls.append(item['picUrl'])
            if ('oriPicUrl' in item) and isinstance(item['oriPicUrl'], str) and item['oriPicUrl'].strip():
                candidate_urls.append(item['oriPicUrl'])
            if ('locImageLink' in item) and isinstance(item['locImageLink'], str) and item['locImageLink'].strip():
                candidate_urls.append(item['locImageLink'])
            if ('thumbUrl' in item) and isinstance(item['thumbUrl'], str) and item['thumbUrl'].strip():
                candidate_urls.append(item['thumbUrl'])
            image_info = {
                'candidate_urls': candidate_urls, 'raw_data': item, 'identifier': item['mf_id'] if 'mf_id' in item else candidate_urls[0],
            }
            image_infos.append(image_info)
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword, search_limits=1000, filters: dict = None):
        base_url = 'https://pic.sogou.com/napi/pc/searchList?'
        params = {'mode': '1', 'start': '384', 'xml_len': '48', 'query': keyword, 'channel': 'pc_pic', 'scene': 'pic_result'}
        if filters is not None: params.update(filters)
        search_urls, page_size = [], int(params['xml_len'])
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params['start'] = str(int(page_size * pn))
            search_url = base_url + urlencode(params, quote_via=quote)
            search_urls.append(search_url)
        return search_urls