'''
Function:
    Implementation of DuckduckgoImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import math
import primp
import random
import requests
import json_repair
from ..utils import Filter
from contextlib import suppress
from .base import BaseImageClient
from urllib.parse import urlencode
from fake_useragent import UserAgent


'''DuckduckgoImageClient'''
class DuckduckgoImageClient(BaseImageClient):
    source = 'DuckduckgoImageClient'
    def __init__(self, **kwargs):
        super(DuckduckgoImageClient, self).__init__(**kwargs)
        self.default_search_headers = {"Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Referer": "https://duckduckgo.com/", "Sec-GPC": "1", "Connection": "keep-alive", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Priority": "u=4"}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''ddgssearch'''
    def ddgssearch(self, search_overrides: dict = None):
        # init
        search_overrides = search_overrides or {}
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
    '''_initsession'''
    def _initsession(self):
        self.session = primp.Client(proxy=None, timeout=30, impersonate="random", impersonate_os="random", verify=True)
        self.session.headers_update(self.default_headers)
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str):
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos = []
        for item in search_result.get('results', []):
            candidate_urls = []
            if ('image' in item) and isinstance(item['image'], str) and item['image'].strip(): candidate_urls.append(item['image'])
            if ('thumbnail' in item) and isinstance(item['thumbnail'], str) and item['thumbnail'].strip(): candidate_urls.append(item['thumbnail'])
            image_info = {
                'candidate_urls': candidate_urls, 'raw_data': item, 'identifier': item['image_token'], 
            }
            image_infos.append(image_info)
        # return
        return image_infos
    '''_getvqd'''
    def _getvqd(self, keyword: str, base_url: str = "https://duckduckgo.com", request_overrides: dict = None):
        request_overrides = request_overrides or {}
        resp = self.request(base_url, 'GET', params={"q": keyword}, **request_overrides)
        resp.raise_for_status()
        html_bytes = resp.content
        for c1, c1_len, c2 in ((b'vqd="', 5, b'"'), (b"vqd=", 4, b"&"), (b"vqd='", 5, b"'")):
            with suppress(ValueError):
                start = html_bytes.index(c1) + c1_len
                end = html_bytes.index(c2, start)
                return html_bytes[start: end].decode()
        raise requests.HTTPError('fail to get "vqd" as the session parameters')
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        # init
        request_overrides, base_url = request_overrides or {}, 'https://duckduckgo.com/i.js?'
        # apply filter
        # --regions
        valid_regions = {
            "lt-lt": "Lithuania", "xl-es": "Latin America", "my-ms": "Malaysia", "my-en": "Malaysia (en)", "mx-es": "Mexico", "nl-nl": "Netherlands", "nz-en": "New Zealand",
            "no-no": "Norway", "pe-es": "Peru", "ph-en": "Philippines", "ph-tl": "Philippines (tl)", "pl-pl": "Poland", "pt-pt": "Portugal", "ro-ro": "Romania", "ru-ru": "Russia",
            "sg-en": "Singapore", "sk-sk": "Slovak Republic", "sl-sl": "Slovenia", "za-en": "South Africa", "es-es": "Spain", "se-sv": "Sweden", "ch-de": "Switzerland (de)",
            "ch-fr": "Switzerland (fr)", "ch-it": "Switzerland (it)", "tw-tzh": "Taiwan", "th-th": "Thailand", "tr-tr": "Turkey", "ua-uk": "Ukraine", "uk-en": "United Kingdom",
            "us-en": "United States", "ue-es": "United States (es)", "ve-es": "Venezuela", "vn-vi": "Vietnam", "wt-wt": "No region",
        }
        if filters is not None and 'region' in filters: region = filters.pop('region')
        else: region = "us-en"
        assert region in valid_regions, 'invalid region argument'
        # --safesearch
        valid_safesearchs = {"on": "1", "moderate": "1", "off": "-1"}
        if filters is not None and 'safesearch' in filters: safesearch = filters.pop('safesearch')
        else: safesearch = "off"
        assert safesearch in valid_safesearchs, 'invalid safesearch argument'
        # --others
        filter_str = self._getfilter().apply(filters, sep=',')
        # construct params
        params = {"o": "json", "q": keyword, "l": region, "vqd": self._getvqd(keyword=keyword, base_url='https://duckduckgo.com/', request_overrides=request_overrides), "p": valid_safesearchs[safesearch], "ct": "AT", "s": 0}
        if filter_str: params['f'] = filter_str
        # construct search_urls
        search_urls, page_size = [], 100
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params["s"] = str(pn * page_size)
            search_url = base_url + urlencode(params)
            search_urls.append({'inputs': {'method': 'GET'}, 'url': search_url, 'method': 'request'})
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
    '''request'''
    def request(self, url: str, method: str, **kwargs):
        if 'cookies' not in kwargs: kwargs['cookies'] = self.default_cookies
        resp = None
        for _ in range(self.max_retries):
            if not self.maintain_session:
                self._initsession()
                if self.random_update_ua: self.session.headers_update({'User-Agent': UserAgent().random})
            self._autosetproxies()
            proxies = kwargs.pop('proxies', None) or getattr(self.session, "proxies")
            if proxies: self.session.proxy = random.choice(list(proxies.values())) if isinstance(proxies, dict) else proxies
            try: (resp := self.session.request(method, url, **kwargs)).raise_for_status()
            except Exception as err: self.logger_handle.error(f'{self.source}.request >>> {url} (Error: {err}; status={getattr(locals().get("resp"), "status_code", None)})', disable_print=self.disable_print); continue
            return resp
        return resp
    '''get'''
    def get(self, url, **kwargs): return self.request(url, method='GET', **kwargs)
    '''post'''
    def post(self, url, **kwargs): return self.request(url, method='POST', **kwargs)