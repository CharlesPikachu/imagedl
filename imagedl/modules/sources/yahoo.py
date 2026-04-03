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
import json_repair
from bs4 import BeautifulSoup
from urllib.parse import quote
from .base import BaseImageClient
from fake_useragent import UserAgent
from ..utils import Filter, ImageInfo


'''YahooImageClient'''
class YahooImageClient(BaseImageClient):
    source = 'YahooImageClient'
    CANDIDATE_SEARCH_URL_FORMATS = [
        "https://images.search.yahoo.com/search/images?p={keyword}&b={offset}", "https://tw.images.search.yahoo.com/search/images?p={keyword}&b={offset}", "https://hk.images.search.yahoo.com/search/images?p={keyword}&b={offset}", "https://sg.images.search.yahoo.com/search/images?p={keyword}&b={offset}", "https://in.images.search.yahoo.com/search/images?p={keyword}&b={offset}", "https://au.images.search.yahoo.com/search/images?p={keyword}&b={offset}",
        "https://nz.images.search.yahoo.com/search/images?p={keyword}&b={offset}", "https://id.images.search.yahoo.com/search/images?p={keyword}&b={offset}", "https://ca.images.search.yahoo.com/search/images?p={keyword}&b={offset}", "https://br.images.search.yahoo.com/search/images?p={keyword}&b={offset}", "https://espanol.images.search.yahoo.com/search/images?p={keyword}&b={offset}", "https://uk.images.search.yahoo.com/search/images?p={keyword}&b={offset}",
        "https://de.images.search.yahoo.com/search/images?p={keyword}&b={offset}", "https://fr.images.search.yahoo.com/search/images?p={keyword}&b={offset}", "https://it.images.search.yahoo.com/search/images?p={keyword}&b={offset}", "https://es.images.search.yahoo.com/search/images?p={keyword}&b={offset}", "https://search.yahoo.co.jp/image/search?p={keyword}&b={offset}", "https://kids.yahoo.co.jp/search/image?p={keyword}&b={offset}",
    ]
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
        for li in soup.select("#sres > li.ld[data]"):
            try: data = json_repair.loads(li["data"])
            except Exception: continue
            if (not (orig_url := data.get("ourl") or data.get("iurl"))) or (orig_url in seen): continue
            seen.add(orig_url); image_infos.append(ImageInfo(source=self.source, raw_data={str(k).lower(): v for k, v in data.items()}, candidate_download_urls=[orig_url], identifier=orig_url))
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, base_url = request_overrides or {}, "https://images.search.yahoo.com/search/images?p={keyword}&b={offset}"
        for candidate_base_url in YahooImageClient.CANDIDATE_SEARCH_URL_FORMATS:
            try: (resp := self.get(candidate_base_url.format(keyword=quote(keyword), offset=1), timeout=10, **request_overrides)).raise_for_status()
            except Exception: base_url = "https://images.search.yahoo.com/search/images?p={keyword}&b={offset}"; continue
            if self._parsesearchresult(resp.text): base_url = candidate_base_url; break
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