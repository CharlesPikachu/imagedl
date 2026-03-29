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
from contextlib import suppress
from .base import BaseImageClient
from urllib.parse import urlencode
from fake_useragent import UserAgent
from ..utils import Filter, ImageInfo


'''DuckduckgoImageClient'''
class DuckduckgoImageClient(BaseImageClient):
    source = 'DuckduckgoImageClient'
    VALID_SEARCH_SAFE_MODES = {"on": "1", "moderate": "1", "off": "-1"}
    VALID_REGIONS = {
        "lt-lt": "Lithuania", "xl-es": "Latin America", "my-ms": "Malaysia", "my-en": "Malaysia (en)", "mx-es": "Mexico", "nl-nl": "Netherlands", "nz-en": "New Zealand", "no-no": "Norway", "pe-es": "Peru", "ph-en": "Philippines", "ph-tl": "Philippines (tl)", "pl-pl": "Poland", "pt-pt": "Portugal", "ro-ro": "Romania", "ru-ru": "Russia", "us-en": "United States", "ue-es": "United States (es)", "ve-es": "Venezuela", 
        "sg-en": "Singapore", "sk-sk": "Slovak Republic", "sl-sl": "Slovenia", "za-en": "South Africa", "es-es": "Spain", "se-sv": "Sweden", "ch-de": "Switzerland (de)", "ch-fr": "Switzerland (fr)", "ch-it": "Switzerland (it)", "tw-tzh": "Taiwan", "th-th": "Thailand", "tr-tr": "Turkey", "ua-uk": "Ukraine", "uk-en": "United Kingdom", "vn-vi": "Vietnam", "wt-wt": "No region",
    }
    def __init__(self, **kwargs):
        super(DuckduckgoImageClient, self).__init__(**kwargs)
        self.default_search_headers = {"Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Referer": "https://duckduckgo.com/", "Sec-GPC": "1", "Connection": "keep-alive", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Priority": "u=4"}
        self.default_download_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''ddgssearch'''
    def ddgssearch(self, proxy: str = None, timeout: int = 5, verify: bool = True, search_overrides: dict = None) -> list[ImageInfo]:
        # import api
        try: from ddgs import DDGS
        except Exception: print('You must install the official API before using this function via "pip install ddgs"'); return []
        # init
        search_overrides, search_results = search_overrides or {}, []
        assert 'query' in search_overrides, 'please set "query" in "search_overrides" as the search keywords'
        # search
        (search_params := {'query': 'butterfly', 'region': 'us-en', 'safesearch': 'off', 'max_results': 1000, 'backend': 'duckduckgo'}).update(search_overrides)
        for item in DDGS(proxy=proxy, timeout=timeout, verify=verify).images(**search_params):
            if not (candidate_urls := [url for url in [item.get('image'), item.get('thumbnail')] if url and str(url).startswith('http')]): continue
            search_results.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=candidate_urls, identifier=candidate_urls[0]))
        search_results = self._removeduplicates(image_infos=search_results)
        search_results = self._appenduniquefilepathforimages(image_infos=search_results, keyword=search_params['query'])
        # return
        return search_results
    '''_initsession'''
    def _initsession(self):
        self.session = primp.Client(proxy=None, timeout=30, impersonate="random", impersonate_os="random", verify=True)
        self.session.headers_update(self.default_headers)
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos: list[ImageInfo] = []
        for item in search_result.get('results', []):
            candidate_urls = []
            if not isinstance(item, dict): continue
            if ('image' in item) and isinstance(item['image'], str) and str(item['image']).strip(): candidate_urls.append(item['image'])
            if ('thumbnail' in item) and isinstance(item['thumbnail'], str) and str(item['thumbnail']).strip(): candidate_urls.append(item['thumbnail'])
            image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=candidate_urls, identifier=item.get('image_token') or candidate_urls[0]))
        # return
        return image_infos
    '''_getvqd'''
    def _getvqd(self, keyword: str, base_url: str = "https://duckduckgo.com", request_overrides: dict = None):
        request_overrides = request_overrides or {}
        (resp := self.request(base_url, 'GET', params={"q": keyword}, **request_overrides)).raise_for_status()
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
        request_overrides, base_url, filters = request_overrides or {}, 'https://duckduckgo.com/i.js?', filters or {}
        # apply filter
        assert (region := filters.pop('region', 'us-en')) in DuckduckgoImageClient.VALID_REGIONS, 'invalid region argument'
        assert (safesearch := filters.pop('safesearch', 'off')) in DuckduckgoImageClient.VALID_SEARCH_SAFE_MODES, 'invalid safesearch argument'
        params = {"o": "json", "q": keyword, "l": region, "vqd": self._getvqd(keyword=keyword, base_url='https://duckduckgo.com/', request_overrides=request_overrides), "p": DuckduckgoImageClient.VALID_SEARCH_SAFE_MODES[safesearch], "ct": "AT", "s": 0}
        if (filter_str := self._getfilter().apply(filters, sep=',')): params['f'] = filter_str
        # construct search_urls
        search_urls, page_size = [], 100
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params["s"] = str(pn * page_size)
            search_urls.append(base_url + urlencode(params))
        # return
        return search_urls
    '''_getfilter'''
    def _getfilter(self):
        search_filter = Filter()
        # time filter
        time_choices = ["Day", "Week", "Month", "Year"]
        format_time_func = lambda val: f"time:{val}"
        search_filter.addrule("time", format_time_func, time_choices)
        # size filter
        size_choices = ["Small", "Medium", "Large", "Wallpaper"]
        format_size_func = lambda val: f"size:{val}"
        search_filter.addrule("size", format_size_func, size_choices)
        # color filter
        color_choices = ["color", "Monochrome", "Red", "Orange", "Yellow", "Green", "Blue", "Purple", "Pink", "Brown", "Black", "Gray", "Teal", "White"]
        format_color_func = lambda val: f"color:{val}"
        search_filter.addrule("color", format_color_func, color_choices)
        # type filter
        type_choices = ["photo", "clipart", "gif", "transparent", "line"]
        format_type_func = lambda val: f"type:{val}"
        search_filter.addrule("type", format_type_func, type_choices)
        # layout filter
        layout_choices = ["Square", "Tall", "Wide"]
        format_layout_func = lambda val: f"layout:{val}"
        search_filter.addrule("layout", format_layout_func, layout_choices)
        # license filter
        license_choices = ["any", "Public", "Share", "ShareCommercially", "Modify", "ModifyCommercially"]
        format_license_func = lambda val: f"license:{val}"
        search_filter.addrule("license", format_license_func, license_choices)
        # return
        return search_filter
    '''request'''
    def request(self, url: str, method: str, **kwargs):
        if 'cookies' not in kwargs: kwargs['cookies'] = self.default_cookies
        for _ in range(self.max_retries):
            if not self.maintain_session:
                self._initsession()
                if self.random_update_ua: self.session.headers_update({'User-Agent': UserAgent().random})
            proxies, resp = kwargs.pop('proxies', None) or self._autosetproxies(), None
            if proxies: self.session.proxy = random.choice(list(proxies.values())) if isinstance(proxies, dict) else proxies
            try: (resp := self.session.request(method, url, **kwargs)).raise_for_status()
            except Exception as err: self.logger_handle.error(f'{self.source}.request >>> {url} (Error: {err}; status={getattr(locals().get("resp"), "status_code", None)})', disable_print=self.disable_print); continue
            return resp
        return resp
    '''get'''
    def get(self, url, **kwargs): return self.request(url, method='GET', **kwargs)
    '''post'''
    def post(self, url, **kwargs): return self.request(url, method='POST', **kwargs)