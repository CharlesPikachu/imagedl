'''
Function:
    Implementation of YandexImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import math
import html
from ..utils import Filter
from urllib.parse import quote
from .base import BaseImageClient


'''YandexImageClient'''
class YandexImageClient(BaseImageClient):
    source = 'YandexImageClient'
    def __init__(self, **kwargs):
        if 'maintain_session' not in kwargs: kwargs['maintain_session'] = True
        super(YandexImageClient, self).__init__(**kwargs)
        self.default_search_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str):
        # parse
        search_result = html.unescape(search_result)
        # image urls
        image_urls = set()
        for u in re.findall(r'"img_href"\s*:\s*"([^"]+)"', search_result):
            if not u.strip(): continue
            image_urls.add(u)
        for u in re.findall(r'"dups"\s*:\s*\[[^\]]*?"url"\s*:\s*"([^"]+)"', search_result):
            if not u.strip(): continue
            image_urls.add(u)
        # construct valid returns
        image_infos = []
        for url in list(image_urls):
            image_info = {
                'candidate_urls': [url], 'raw_data': str(search_result), 'identifier': url,
            }
            image_infos.append(image_info)
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword, search_limits=1000, filters: dict = None, request_overrides: dict = {}):
        candidate_domains = ['https://yandex.com', 'https://yandex.ru', 'https://yandex.kz', 'https://yandex.by', 'https://yandex.com.tr']
        for domain in candidate_domains:
            resp = self.session.get(domain)
            if resp.status_code == 200: break
        base_url = '{domain}/images/search?text={keyword}&p={page}'
        filter_str = self._getfilter().apply(filters, sep='&')
        search_urls, page_size = [], 60
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            search_url = base_url.format(domain=domain, keyword=quote(keyword), page=pn+1)
            if filter_str: search_url += f'&{filter_str}'
            search_urls.append(search_url)
        return search_urls
    '''_getfilter'''
    def _getfilter(self):
        search_filter = Filter()
        # TODO: add valid filters for YandexImageClient
        # return
        return search_filter