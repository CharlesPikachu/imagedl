'''
Function:
    Implementation of GoogleImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import math
import random
import datetime
import json_repair
from bs4 import BeautifulSoup
from .base import BaseImageClient
from urllib.parse import urlencode
from ..utils import Filter, ImageInfo, DrissionPageUtils, FakeRequestsResponse


'''GoogleImageClient'''
class GoogleImageClient(BaseImageClient):
    source = 'GoogleImageClient'
    def __init__(self, **kwargs):
        super(GoogleImageClient, self).__init__(**kwargs)
        self.default_search_headers = {'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''officialsearchanddownload'''
    def officialsearchanddownload(self, google_image_search_overrides: dict = None, search_overrides: dict = None):
        # import api
        try: from google_images_search import GoogleImagesSearch
        except Exception: print('You must install the official API before using this function via "pip install google_images_search"'); return []
        # init
        google_image_search_overrides, search_overrides = google_image_search_overrides or {}, search_overrides or {}
        assert 'q' in search_overrides, 'please set "q" in "search_overrides" as the search keywords'
        # instance GoogleImagesSearch
        (google_image_search_settings := random.choice([
            {'validate_images': True, 'developer_key': 'AIzaSyCGyqf36D5k3QghaZLhAqb1R2OUtRFraF8', 'custom_search_cx': '0d386b282da5209ea'},
            {'validate_images': True, 'developer_key': 'AIzaSyD4dFGSan50nEmXh2Jnm4l6JHCAgEATWJc', 'custom_search_cx': '495179597de2e4ab6'},
            {'validate_images': True, 'developer_key': 'AIzaSyBRlama1N7tiW0yVq45CrqCx9hyFrESmIs', 'custom_search_cx': '144af1a5b59944a2b'},
            {'validate_images': True, 'developer_key': 'AIzaSyB7CcF4xiZqKE3yAmjBDZct4_HHs27gL7Y', 'custom_search_cx': 'd7e74b48d90e7441c'},
        ])).update(google_image_search_overrides)
        gis = GoogleImagesSearch(**google_image_search_settings)
        # search and download
        (search_params := {'q': 'girls', 'num': 1000}).update(search_overrides)
        gis.search(search_params=search_params, path_to_dir=self.work_dir)
    '''serpapisearch'''
    def serpapisearch(self, search_overrides: dict = None) -> list[ImageInfo]:
        # import api
        try: from serpapi import GoogleSearch
        except Exception: print('You must install the official API before using this function via "pip install google google-search-results serpapi"'); return
        # init
        search_overrides, search_results = search_overrides or {}, []
        assert 'q' in search_overrides, 'please set "q" in "search_overrides" as the search keywords'
        CANDIDATE_API_KEYS = ['cb37586e2a8d129c4142b06c3d46a19aa8bb11187c776a85977298893a5a3266']
        # search
        (search_params := {'q': 'girls', 'google_domain': 'google.com', 'tbm': 'isch', 'api_key': random.choice(CANDIDATE_API_KEYS)}).update(search_overrides)
        for item in json_repair.loads(GoogleSearch(search_params).get_results())['images_results']:
            if not isinstance(item, dict): continue
            candidate_urls = [item.get('original'), item.get('thumbnail')]
            if not (candidate_urls := [c for c in candidate_urls if c and str(c).startswith('http')]): continue
            search_results.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=candidate_urls, identifier=candidate_urls[0]))
        search_results = self._removeduplicates(image_infos=search_results)
        search_results = self._appenduniquefilepathforimages(image_infos=search_results, keyword=search_params['q'])
        # return
        return search_results
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        urls, m = set(), re.search(r'google\.ldi\s*=\s*({.*?})\s*;', search_result, re.S)
        try: urls.update(json_repair.loads(m.group(1)).values())
        except Exception: urls = set()
        soup, image_infos = BeautifulSoup(search_result, "lxml"), []
        for img in soup.find_all("img"):
            for k in ("src", "data-src", "data-iurl", "data-img-url", "data-thumb", "data-lzy-src"):
                if (u := img.get(k)) and u.startswith(("http://", "https://")): urls.add(u)
        for url in sorted(urls):
            image_infos.append(ImageInfo(source=self.source, raw_data=search_result, candidate_download_urls=[url], identifier=url))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        # init
        request_overrides, base_url, filters = request_overrides or {}, 'https://www.google.com/search?', filters or {}
        # apply filter
        language = filters.pop('language', None); filter_str = self._getfilter().apply(filters, sep=",")
        # construct search_urls
        search_urls, page_size = [], 100
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params = dict(q=keyword, ijn=pn, start=pn*page_size, tbs=filter_str, tbm="isch")
            if language: params["lr"] = "lang_" + language
            search_urls.append({'url': base_url + urlencode(params), 'method': 'drissionget', 'inputs': {}})
        # return
        return search_urls
    '''_getfilter'''
    def _getfilter(self):
        search_filter = Filter()
        # type filter
        type_choices = ["photo", "face", "clipart", "linedrawing", "animated"]
        search_filter.addrule("type", lambda img_type: "itp:lineart" if img_type == "linedrawing" else "itp:" + img_type, type_choices)
        # color filter
        color_choices = ["color", "blackandwhite", "transparent", "red", "orange", "yellow", "green", "teal", "blue", "purple", "pink", "white", "gray", "black", "brown"]
        format_color_func = lambda color: ("ic:" + {"color": "color", "blackandwhite": "gray", "transparent": "trans"}[color] if color in {"color", "blackandwhite", "transparent"} else f"ic:specific,isc:{color}")
        search_filter.addrule("color", format_color_func, color_choices)
        # size filter
        format_size_func = lambda size: ("isz:" + {"large": "l", "medium": "m", "icon": "i"}[size] if size in {"large", "medium", "icon"} else "isz:lt,islt:" + {"400x300": "qsvga", "640x480": "vga", "800x600": "svga", "1024x768": "xga", "2mp": "2mp", "4mp": "4mp", "6mp": "6mp", "8mp": "8mp", "10mp": "10mp", "12mp": "12mp", "15mp": "15mp", "20mp": "20mp", "40mp": "40mp", "70mp": "70mp",}[size[1:]] if str(size).startswith(">") else ("isz:ex,iszw:{},iszh:{}".format(*wh) if len(wh := str(size)[1:].split("x")) == 2 else (_ for _ in ()).throw(AssertionError())) if str(size).startswith("=") else (_ for _ in ()).throw(ValueError('filter option "size" must be one of the following: "large, medium, icon, >[]x[], =[]x[]" where [] is an integer')))
        search_filter.addrule("size", format_size_func)
        # licence filter
        license_code = {"noncommercial": "f", "commercial": "fc", "noncommercial,modify": "fm", "commercial,modify": "fmc"}
        format_license_func = lambda license: "sur:" + license_code[license]
        license_choices = list(license_code.keys())
        search_filter.addrule("license", format_license_func, license_choices)
        # date filter
        format_date_func = lambda date: ("" if date == "anytime" else "qdr:d" if date == "pastday" else "qdr:w" if date == "pastweek" else "qdr:m" if date == "pastmonth" else "qdr:y" if date == "pastyear" else ("cdr:1,cd_min:{},cd_max:{}".format(*["" if date_ is None else (datetime.date(*date_) if isinstance(date_, tuple) else date_).strftime("%m/%d/%Y") if isinstance(date_, (tuple, datetime.date)) else (_ for _ in ()).throw(TypeError("date must be a tuple or datetime.date object")) for date_ in date]) if len(date) == 2 else (_ for _ in ()).throw(AssertionError())) if isinstance(date, tuple) else (_ for _ in ()).throw(TypeError('filter option "date" must be "pastday", "pastweek", "anytime", "pastmonth", "pastyear" or "a tuple of dates"')))
        search_filter.addrule("date", format_date_func)
        # return
        return search_filter
    '''drissionget'''
    def drissionget(self, url, **request_overrides):
        request_overrides = request_overrides or {}
        page = DrissionPageUtils.initsmartbrowser(headless=False, requests_headers=None, requests_proxies=(request_overrides.get('proxies') or self._autosetproxies()), requests_cookies=(request_overrides.get('cookies') or self.default_cookies))
        page.get(url); page.wait.eles_loaded('tag:img', timeout=10); html_text = page.html; DrissionPageUtils.quitpage(page=page)
        return FakeRequestsResponse(predefined_text=html_text, status_code=200)