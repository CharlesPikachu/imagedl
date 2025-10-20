'''
Function:
    Implementation of I360ImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import math
import json_repair
from ..utils import Filter
from urllib.parse import quote
from .base import BaseImageClient


'''I360ImageClient'''
class I360ImageClient(BaseImageClient):
    source = 'I360ImageClient'
    def __init__(self, **kwargs):
        super(I360ImageClient, self).__init__(**kwargs)
        self.default_headers = {
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session.headers.update(self.default_headers)
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str):
        # parse json text in safety
        search_result = json_repair.loads(search_result)
        # parse search result
        image_infos = []
        for item in search_result['list']:
            candidate_urls = []
            if ('img' in item) and isinstance(item['img'], str) and item['img'].strip():
                candidate_urls.append(item['img'])
            if ('thumb_bak' in item) and isinstance(item['thumb_bak'], str) and item['thumb_bak'].strip():
                candidate_urls.append(item['thumb_bak'])
            if ('thumb' in item) and isinstance(item['thumb'], str) and item['thumb'].strip():
                candidate_urls.append(item['thumb'])
            if ('_thumb_bak' in item) and isinstance(item['_thumb_bak'], str) and item['_thumb_bak'].strip():
                candidate_urls.append(item['_thumb_bak'])
            if ('_thumb' in item) and isinstance(item['_thumb'], str) and item['_thumb'].strip():
                candidate_urls.append(item['_thumb'])
            image_info = {
                'candidate_urls': candidate_urls, 'raw_data': item, 'identifier': item['id'],
            }
            image_infos.append(image_info)
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword, search_limits=1000, filters: dict = None):
        base_url = 'https://image.so.com/j?pn={}&q={}&sn={}'
        filter_str = self.getfilter().apply(filters, sep='&')
        search_urls, page_size = [], 60
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            search_url = base_url.format(page_size, quote(keyword), pn * page_size)
            if filter_str: search_url += f'&{filter_str}'
            search_urls.append(search_url)
        return search_urls
    '''getfilter'''
    def getfilter(self):
        search_filter = Filter()
        # TODO: add valid filters for I360ImageClient
        # return
        return search_filter