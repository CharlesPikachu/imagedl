'''
Function:
    Implementation of DuckduckgoImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import math
import requests
import json_repair
from .base import BaseImageClient
from alive_progress import alive_bar
from urllib.parse import quote, urlencode


'''DuckduckgoImageClient'''
class DuckduckgoImageClient(BaseImageClient):
    source = 'DuckduckgoImageClient'
    def __init__(self, **kwargs):
        if 'maintain_session' not in kwargs: kwargs['maintain_session'] = True
        super(DuckduckgoImageClient, self).__init__(**kwargs)
        self.default_headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://duckduckgo.com/",
            "Sec-CH-UA": '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
            "Priority": "u=1, i",
        }
        self.session.headers.update(self.default_headers)
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str):
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos = []
        for item in search_result.get('results', []):
            candidate_urls = []
            if ('image' in item) and isinstance(item['image'], str) and item['image'].strip():
                candidate_urls.append(item['img'])
            if ('thumbnail' in item) and isinstance(item['thumbnail'], str) and item['thumbnail'].strip():
                candidate_urls.append(item['thumbnail'])
            image_info = {
                'candidate_urls': candidate_urls, 'raw_data': item, 'identifier': item['image_token'],
            }
            image_infos.append(image_info)
        # return
        return image_infos
    '''_getvqd'''
    def _getvqd(self, keyword: str, base_url: str):
        q = urlencode({"q": keyword}, quote_via=quote, safe="")
        resp = self.get(f'{base_url}?{q}')
        if resp is None or resp.status_code != 200:
            raise requests.HTTPError('fail to get "vqd" as the session parameters')
        m = re.search(r"vqd=([\d-]+)&", resp.text)
        if not m: m = re.search(r"[\"']vqd[\"']\s*:\s*[\"']([\d-]+)[\"']", resp.text)
        if not m: raise requests.HTTPError('fail to get "vqd" as the session parameters')
        vqd = m.group(1)
        return vqd
    '''search'''
    def search(self, keyword, search_limits=1000, num_threadings=1, filters: dict = None, request_overrides: dict = {}):
        # asserts
        assert num_threadings == 1, f'".search" for {self.source} only supports "num_threadings = 1"'
        # logging
        self.logger_handle.info(f'Start to search images using {self.source}.')
        # obtain image infos
        image_infos, base_url, page_size = [], 'https://duckduckgo.com/', 100
        params = {
            "o": "json", "q": "dogs", "l": "wt-wt", "vqd": "4-39911919969715559825435217871297706556",
            "p": "1", "ct": "US", "bpia": "1", "a": "h_",
        }
        if filters is not None: params.update(filters)
        params["q"] = keyword
        params["vqd"] = self._getvqd(keyword=keyword, base_url=base_url)
        with alive_bar(math.ceil(search_limits * 1.2 / page_size)) as bar:
            for pn in range(math.ceil(search_limits * 1.2 / page_size)):
                if pn == 0:
                    search_url = base_url + 'i.js?' + urlencode(params, quote_via=quote)
                    self._search(search_urls=[search_url], bar=alive_bar, image_infos=image_infos, request_overrides=request_overrides)
                else:
                    search_url = base_url + image_infos[-1]['next']
                    self._search(search_urls=[search_url], bar=alive_bar, image_infos=image_infos, request_overrides=request_overrides)
        # logging
        image_infos = self._removeduplicates(image_infos)
        self._appenduniquefilepathforimages(image_infos=image_infos, keyword=keyword)
        if len(image_infos) > 0:
            work_dir = image_infos[0]['work_dir']
            self._savetopkl(image_infos, os.path.join(work_dir, 'search_results.pkl'))
        self.logger_handle.info(f'Finished searching images using {self.source}. Search results have been saved to {work_dir}, valid items: {len(image_infos)}.')
        # return
        return image_infos