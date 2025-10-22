'''
Function:
    Implementation of DuckduckgoImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import math
import requests
import json_repair
from ..utils import Filter
from .base import BaseImageClient
from urllib.parse import quote, urlencode


'''DuckduckgoImageClient'''
class DuckduckgoImageClient(BaseImageClient):
    source = 'DuckduckgoImageClient'
    def __init__(self, **kwargs):
        if 'maintain_session' not in kwargs: kwargs['maintain_session'] = True
        super(DuckduckgoImageClient, self).__init__(**kwargs)
        self.default_search_headers = {
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
        self.default_headers = self.default_search_headers
        self._initsession()
    '''ddgssearch'''
    def ddgssearch(self, search_overrides: dict = {}):
        # import api
        try:
            from ddgs import DDGS
        except:
            print('You must install the official API before using this function via "pip install ddgs"')
            return
        # asserts
        assert 'query' in search_overrides, 'please set "query" in "search_overrides" as the search keywords'
        # search
        search_params = {'query': 'butterfly', 'region': 'us-en', 'safesearch': 'off', 'max_results': 1000, 'backend': 'duckduckgo'}
        search_params.update(search_overrides)
        results = DDGS().images(**search_params)
        # return
        return results
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str):
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos = []
        for item in search_result.get('results', []):
            candidate_urls = []
            if ('image' in item) and isinstance(item['image'], str) and item['image'].strip():
                candidate_urls.append(item['image'])
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
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword, search_limits=1000, filters: dict = None):
        # base url
        base_url = 'https://duckduckgo.com/i.js?'
        # apply filter
        # --regions
        valid_regions = {
            "lt-lt": "Lithuania", "xl-es": "Latin America", "my-ms": "Malaysia", "my-en": "Malaysia (en)", "mx-es": "Mexico", "nl-nl": "Netherlands", "nz-en": "New Zealand",
            "no-no": "Norway", "pe-es": "Peru", "ph-en": "Philippines", "ph-tl": "Philippines (tl)", "pl-pl": "Poland", "pt-pt": "Portugal", "ro-ro": "Romania", "ru-ru": "Russia",
            "sg-en": "Singapore", "sk-sk": "Slovak Republic", "sl-sl": "Slovenia", "za-en": "South Africa", "es-es": "Spain", "se-sv": "Sweden", "ch-de": "Switzerland (de)",
            "ch-fr": "Switzerland (fr)", "ch-it": "Switzerland (it)", "tw-tzh": "Taiwan", "th-th": "Thailand", "tr-tr": "Turkey", "ua-uk": "Ukraine", "uk-en": "United Kingdom",
            "us-en": "United States", "ue-es": "United States (es)", "ve-es": "Venezuela", "vn-vi": "Vietnam", "wt-wt": "No region",
        }
        if filters is not None and 'region' in filters:
            region = filters.pop('region')
        else:
            region = "wt-wt"
        assert region in valid_regions
        # --safesearch
        valid_safesearchs = {"on": "1", "moderate": "1", "off": "-1"}
        if filters is not None and 'safesearch' in filters:
            safesearch = filters.pop('safesearch')
        else:
            safesearch = "moderate"
        assert safesearch in valid_safesearchs
        # --others
        filter_str = self._getfilter().apply(filters, sep=',')
        # construct params
        params = {
            "o": "json", "q": keyword, "l": region, "vqd": self._getvqd(keyword=keyword, base_url='https://duckduckgo.com/'),
            "p": valid_safesearchs[safesearch], "f": filter_str, "s": 0,
        }
        # construct search_urls
        search_urls, page_size = [], 100
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params["s"] = pn * page_size
            search_url = base_url + urlencode(params)
            search_urls.append(search_url)
        # return
        return search_urls
    '''_getfilter'''
    def _getfilter(self):
        search_filter = Filter()
        # time filter
        time_choices = ["Day", "Week", "Month", "Year"]
        def formattime(val: str):
            return f"time:{val}"
        search_filter.addrule("time", formattime, time_choices)
        # size filter
        size_choices = ["Small", "Medium", "Large", "Wallpaper"]
        def formatsize(val: str):
            return f"size:{val}"
        search_filter.addrule("size", formatsize, size_choices)
        # color filter
        color_choices = ["color", "Monochrome", "Red", "Orange", "Yellow", "Green", "Blue", "Purple", "Pink", "Brown", "Black", "Gray", "Teal", "White"]
        def formatcolor(val: str):
            return f"color:{val}"
        search_filter.addrule("color", formatcolor, color_choices)
        # type filter
        type_choices = ["photo", "clipart", "gif", "transparent", "line"]
        def formattype(val: str):
            return f"type:{val}"
        search_filter.addrule("type", formattype, type_choices)
        # layout filter
        layout_choices = ["Square", "Tall", "Wide"]
        def formatlayout(val: str):
            return f"layout:{val}"
        search_filter.addrule("layout", formatlayout, layout_choices)
        # license filter
        license_choices = ["any", "Public", "Share", "ShareCommercially", "Modify", "ModifyCommercially"]
        def formatlicense(val: str):
            return f"license:{val}"
        search_filter.addrule("license", formatlicense, license_choices)
        # return
        return search_filter