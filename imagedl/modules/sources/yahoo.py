'''
Function:
    Implementation of YahooImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import math
import primp
import random
from bs4 import BeautifulSoup
from urllib.parse import quote
from .base import BaseImageClient
from fake_useragent import UserAgent
from ..utils import Filter, ImageInfo


'''YahooImageClient'''
class YahooImageClient(BaseImageClient):
    source = 'YahooImageClient'
    def __init__(self, **kwargs):
        super(YahooImageClient, self).__init__(**kwargs)
        self.default_search_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"}
        self.default_download_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_initsession'''
    def _initsession(self):
        self.session = primp.Client(proxy=None, timeout=30, impersonate="random", impersonate_os="random", verify=True)
        self.session.headers_update(self.default_headers)
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        soup, image_infos, seen = BeautifulSoup(search_result, "lxml"), [], set()
        for a in soup.select('a[data-origurl]'):
            if (not (orig_url := a.get("data-origurl"))) or (orig_url in seen): continue
            seen.add(orig_url); image_infos.append(ImageInfo(source=self.source, raw_data={str(k).lower(): v for k, v in a.attrs.items()}, candidate_download_urls=[orig_url], identifier=orig_url))
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, base_url = request_overrides or {}, "https://images.search.yahoo.com/search/images?p={keyword}&b={offset}"
        filter_str, search_urls, page_size = self._getfilter().apply(filters, sep="&"), [], 60
        for page in range(math.ceil(search_limits * 1.2 / page_size)):
            search_url = base_url.format(keyword=quote(keyword), offset=(page * page_size + 1))
            search_urls.append((search_url if not filter_str else (search_url + f"&{filter_str}")))
        return search_urls
    '''_getfilter'''
    def _getfilter(self):
        search_filter = Filter()
        # size
        image_size_map = {"small": "small", "medium": "medium", "large": "large", "extralarge": "wallpaper", "wallpaper": "wallpaper"}
        search_filter.addrule("size", lambda size: f"imgsz={image_size_map[size]}", list(image_size_map.keys()))
        # color
        image_color_map = {"color": "color", "bw": "bw", "red": "red", "orange": "orange", "yellow": "yellow", "green": "green", "teal": "teal", "blue": "blue", "purple": "purple", "pink": "pink", "brown": "brown", "black": "black", "gray": "gray", "white": "white"}
        search_filter.addrule("color", lambda color: f"imgc={image_color_map[color]}", list(image_color_map.keys()))
        # type
        image_type_map = {"photo": "photo", "clipart": "clipart", "linedrawing": "linedrawing", "gif": "gif", "transparent": "transparent"}
        search_filter.addrule("type", lambda img_type: f"imgty={image_type_map[img_type]}", list(image_type_map.keys()))
        # layout
        image_layout_map = {"square": "square", "wide": "wide", "tall": "tall"}
        search_filter.addrule("layout", lambda layout: f"imga={image_layout_map[layout]}", list(image_layout_map.keys()))
        # people
        image_people_map = {"face": "face", "portrait": "portrait", "nonportrait": "nonportrait"}
        search_filter.addrule("people", lambda people: f"imgf={image_people_map[people]}", list(image_people_map.keys()))
        # time
        image_time_map = {"day": "day", "week": "week", "month": "month", "year": "year"}
        search_filter.addrule("time", lambda t: f"imgt={image_time_map[t]}", list(image_time_map.keys()))
        # license
        image_license_map = {"cc": "cc", "pd": "pd", "fsu": "fsu", "fsuc": "fsuc", "fmsu": "fmsu", "fmsuc": "fmsuc"}
        search_filter.addrule("license", lambda lic: f"imgl={image_license_map[lic]}", list(image_license_map.keys()))
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