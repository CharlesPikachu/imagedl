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
from urllib.parse import urlencode
from typing_extensions import Unpack
from ..utils import Filter, ImageInfo
from .base import BaseImageClient, BaseImageClientKwargs


'''DuckduckgoImageClient'''
class DuckduckgoImageClient(BaseImageClient):
    source = 'DuckduckgoImageClient'
    VALID_SEARCH_SAFE_MODES = {"on": "1", "moderate": "-1", "off": "-2"}
    VALID_REGIONS = {
        "lt-lt": "Lithuania", "xl-es": "Latin America", "my-ms": "Malaysia", "my-en": "Malaysia (en)", "mx-es": "Mexico", "nl-nl": "Netherlands", "nz-en": "New Zealand", "no-no": "Norway", "pe-es": "Peru", "ph-en": "Philippines", "ph-tl": "Philippines (tl)", "pl-pl": "Poland", "pt-pt": "Portugal", "ro-ro": "Romania", "ru-ru": "Russia", "us-en": "United States", "ue-es": "United States (es)", "ve-es": "Venezuela", 
        "sg-en": "Singapore", "sk-sk": "Slovak Republic", "sl-sl": "Slovenia", "za-en": "South Africa", "es-es": "Spain", "se-sv": "Sweden", "ch-de": "Switzerland (de)", "ch-fr": "Switzerland (fr)", "ch-it": "Switzerland (it)", "tw-tzh": "Taiwan", "th-th": "Thailand", "tr-tr": "Turkey", "ua-uk": "Ukraine", "uk-en": "United Kingdom", "vn-vi": "Vietnam", "wt-wt": "No region",
    }
    def __init__(self, **kwargs: Unpack[BaseImageClientKwargs]):
        kwargs.setdefault('maintain_session', True)
        super(DuckduckgoImageClient, self).__init__(**kwargs)
        self.default_search_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36", "Accept": "application/json, text/javascript, */*; q=0.01", "Accept-Language": "en-US,en;q=0.9", "Referer": "https://duckduckgo.com/", "X-Requested-With": "XMLHttpRequest"}
        self.default_download_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"}
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
            if candidate_urls: image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=candidate_urls, identifier=item.get('image_token') or candidate_urls[0]))
        # return
        return image_infos
    '''_getvqd'''
    def _getvqd(self, keyword: str, base_url: str = "https://duckduckgo.com", request_overrides: dict = None):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.9", "Referer": None, "X-Requested-With": None}
        (resp := self.get(base_url, params={"q": keyword, "iax": "images", "ia": "images"}, headers=headers, **(request_overrides or {}))).raise_for_status()
        if (match := re.search(r'vqd=([\d-]+)', resp.text)): return match.group(1)
        raise requests.HTTPError('fail to get "vqd" as the session parameters')
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        # init
        request_overrides, base_url, filters = request_overrides or {}, 'https://duckduckgo.com/i.js?', (filters or {}).copy()
        # apply filter
        assert (region := filters.pop('region', 'us-en')) in DuckduckgoImageClient.VALID_REGIONS, 'invalid region argument'
        assert (safesearch := filters.pop('safesearch', 'off')) in DuckduckgoImageClient.VALID_SEARCH_SAFE_MODES, 'invalid safesearch argument'
        params = {"l": region, "o": "json", "q": keyword, "vqd": self._getvqd(keyword=keyword, base_url='https://duckduckgo.com/', request_overrides=request_overrides), "f": ",,,,,", "p": DuckduckgoImageClient.VALID_SEARCH_SAFE_MODES[safesearch]}
        if (filter_str := self._getfilter().apply(filters, sep=',')): params['f'] = filter_str
        # construct search_urls
        search_urls, page_size = [], 100
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            if pn: params["s"] = str(pn * page_size)
            search_urls.append({'url': base_url + urlencode(params), 'method': 'get', 'inputs': {'headers': {'Referer': 'https://duckduckgo.com/?' + urlencode({"q": keyword, "iax": "images", "ia": "images"})}}})
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