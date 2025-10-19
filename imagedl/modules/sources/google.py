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
import datetime
from ..utils import Filter
from bs4 import BeautifulSoup
from .base import BaseImageClient
from urllib.parse import urlencode


'''GoogleImageClient'''
class GoogleImageClient(BaseImageClient):
    source = 'GoogleImageClient'
    def __init__(self, **kwargs):
        if 'auto_set_proxies' not in kwargs: kwargs['auto_set_proxies'] = False
        if 'auto_set_headers' not in kwargs: kwargs['auto_set_headers'] = False
        super(GoogleImageClient, self).__init__(**kwargs)
        self.headers = {
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.session.headers.update(self.headers)
    '''officialsearchanddownload'''
    def officialsearchanddownload(self, google_image_search_overrides: dict = {}, search_overrides: dict = {}):
        # import official api
        try:
            from google_images_search import GoogleImagesSearch
        except:
            print('You must install the official API before using this function via `pip install google_images_search`')
            return
        # asserts
        assert 'q' in search_overrides, 'please set `q` in `search_overrides` as the search keywords'
        # instance GoogleImagesSearch
        google_image_search_params = {
            'validate_images': True, 'developer_key': 'AIzaSyCGyqf36D5k3QghaZLhAqb1R2OUtRFraF8', 'custom_search_cx': '0d386b282da5209ea',
        }
        google_image_search_params.update(google_image_search_overrides)
        gis = GoogleImagesSearch(**google_image_search_params)
        # search and download
        search_params = {'q': 'girls', 'num': 1000}
        search_params.update(search_overrides)
        gis.search(search_params=search_params, path_to_dir=self.work_dir)
    '''serpapisearch'''
    def serpapisearch(self, search_overrides: dict = {}):
        # import api
        try:
            from serpapi import GoogleSearch
        except:
            print('You must install the official API before using this function via `pip install google google-search-results serpapi`')
            return
        # asserts
        assert 'q' in search_overrides, 'please set `q` in `search_overrides` as the search keywords'
        # search
        search_params = {'q': 'girls', 'google_domain': 'google.com', 'tbm': 'isch', 'api_key': 'cb37586e2a8d129c4142b06c3d46a19aa8bb11187c776a85977298893a5a3266'}
        search_engine = GoogleSearch(search_params)
        search_results = search_engine.get_results()
        # return
        return search_results
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str):
        image_infos = []
        soup = BeautifulSoup(search_result, 'lxml')
        for div in soup.find_all(name='script'):
            txt = str(div)
            urls = re.findall(r"http[^\[]*?.(?:jpg|png|bmp)", txt)
            if not urls: urls = re.findall(r"http[^\[]*?\.(?:jpg|png|bmp)", txt)
            urls = [bytes(url, "utf-8").decode("unicode-escape") for url in urls]
            for url in urls:
                image_info = {
                    'candidate_urls': [url], 'raw_data': txt
                }
                image_infos.append(image_info)
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword, search_limits=1000, filters: dict = None, language: str = None):
        base_url = 'https://www.google.com/search?'
        filter_str = self.getfilter().apply(filters, sep=",")
        search_urls, page_size = [], 100
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params = dict(q=keyword, ijn=pn, start=pn*page_size, tbs=filter_str, tbm="isch")
            if language: params["lr"] = "lang_" + language
            search_urls.append(base_url + urlencode(params))
        return search_urls
    '''getfilter: refer to https://github.com/hellock/icrawler/blob/master/icrawler/builtin/google.py'''
    def getfilter(self):
        search_filter = Filter()
        # type filter
        def formattype(img_type):
            return "itp:lineart" if img_type == "linedrawing" else "itp:" + img_type
        type_choices = ["photo", "face", "clipart", "linedrawing", "animated"]
        search_filter.addrule("type", formattype, type_choices)
        # color filter
        def formatcolor(color):
            if color in ["color", "blackandwhite", "transparent"]:
                code = {"color": "color", "blackandwhite": "gray", "transparent": "trans"}
                return "ic:" + code[color]
            else:
                return f"ic:specific,isc:{color}"
        color_choices = [
            "color", "blackandwhite", "transparent", "red", "orange", "yellow", "green", "teal", "blue",
            "purple", "pink", "white", "gray", "black", "brown",
        ]
        search_filter.addrule("color", formatcolor, color_choices)
        # size filter
        def formatsize(size: str):
            if size in ["large", "medium", "icon"]:
                size_code = {"large": "l", "medium": "m", "icon": "i"}
                return "isz:" + size_code[size]
            elif size.startswith(">"):
                size_code = {
                    "400x300": "qsvga", "640x480": "vga", "800x600": "svga", "1024x768": "xga", "2mp": "2mp", "4mp": "4mp", "6mp": "6mp", 
                    "8mp": "8mp", "10mp": "10mp", "12mp": "12mp", "15mp": "15mp", "20mp": "20mp", "40mp": "40mp", "70mp": "70mp",
                }
                return "isz:lt,islt:" + size_code[size[1:]]
            elif size.startswith("="):
                wh = size[1:].split("x")
                assert len(wh) == 2
                return "isz:ex,iszw:{},iszh:{}".format(*wh)
            else:
                raise ValueError('filter option "size" must be one of the following: `large, medium, icon, >[]x[], =[]x[]` where [] is an integer')
        search_filter.addrule("size", formatsize)
        # licence filter
        license_code = {
            "noncommercial": "f", "commercial": "fc", "noncommercial,modify": "fm", "commercial,modify": "fmc",
        }
        def formatlicense(license):
            return "sur:" + license_code[license]
        license_choices = list(license_code.keys())
        search_filter.addrule("license", formatlicense, license_choices)
        # date filter
        def formatdate(date):
            if date == "anytime":
                return ""
            elif date == "pastday":
                return "qdr:d"
            elif date == "pastweek":
                return "qdr:w"
            elif date == "pastmonth":
                return "qdr:m"
            elif date == "pastyear":
                return "qdr:y"
            elif isinstance(date, tuple):
                assert len(date) == 2
                date_range = []
                for date_ in date:
                    if date_ is None:
                        date_str = ""
                    elif isinstance(date_, (tuple, datetime.date)):
                        date_ = datetime.date(*date_) if isinstance(date_, tuple) else date_
                        date_str = date_.strftime("%m/%d/%Y")
                    else:
                        raise TypeError("date must be a tuple or datetime.date object")
                    date_range.append(date_str)
                return "cdr:1,cd_min:{},cd_max:{}".format(*date_range)
            else:
                raise TypeError('filter option "date" must be "pastday", "pastweek", "anytime", "pastmonth", "pastyear" or "a tuple of dates"')
        search_filter.addrule("date", formatdate)
        # return
        return search_filter