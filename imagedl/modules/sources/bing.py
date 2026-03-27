'''
Function:
    Implementation of BingImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import math
import html
from bs4 import BeautifulSoup
from urllib.parse import quote
from .base import BaseImageClient
from ..utils import Filter, ImageInfo


'''BingImageClient'''
class BingImageClient(BaseImageClient):
    source = 'BingImageClient'
    def __init__(self, **kwargs):
        super(BingImageClient, self).__init__(**kwargs)
        self.default_search_headers = {'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        image_infos, soup, pattern = [], BeautifulSoup(search_result, 'lxml'), re.compile(r'"murl\":\"(.*?)\"')
        for item in soup.find_all('div', class_='imgpt'):
            if not (href_str := html.unescape(item.a["m"]) if getattr(item, "a", None) and item.a.has_attr("m") else None): continue
            if (not (match := pattern.search(href_str))) or (not match.group(1).strip()): continue
            image_infos.append(ImageInfo(source=self.source, raw_data=str(item), candidate_download_urls=[match.group(1).strip()], identifier=match.group(1).strip()))
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword, search_limits=1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, search_urls, page_size = request_overrides or {}, [], 20
        base_url = 'https://www.bing.com/images/async?q={keyword}&first={page}'
        filter_str = "&qft=" + filter_str if (filter_str := self._getfilter().apply(filters)) else ""
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            search_url = base_url.format(keyword=quote(keyword), page=pn*page_size) + filter_str
            search_urls.append(search_url)
        return search_urls
    '''_getfilter'''
    def _getfilter(self):
        search_filter = Filter()
        # type filter
        type_choices = ["photo", "clipart", "linedrawing", "transparent", "animated"]
        format_type_func = lambda img_type: "+filterui:photo-" + ("animatedgif" if img_type == "animated" else img_type)
        search_filter.addrule("type", format_type_func, type_choices)
        # color filter
        color_choices = ["color", "blackandwhite", "red", "orange", "yellow", "green", "teal", "blue", "purple", "pink", "white", "gray", "black", "brown"]
        format_color_func = lambda color: ("+filterui:color2-color" if color == "color" else "+filterui:color2-bw" if color == "blackandwhite" else "+filterui:color2-FGcls_" + str(color).upper())
        search_filter.addrule("color", format_color_func, color_choices)
        # size filter
        raise_err_func = lambda e: (_ for _ in ()).throw(e)
        format_size_func = lambda size: ("+filterui:imagesize-" + size if size in ["large", "medium", "small"] else "+filterui:imagesize-wallpaper" if size == "extralarge" else ((lambda wh: "+filterui:imagesize-custom_{}_{}".format(*wh) if len(wh) == 2 else raise_err_func(AssertionError()))(str(size)[1:].split("x")) if str(size).startswith("=") else raise_err_func(ValueError('filter option "size" must be one of the following: "extralarge, large, medium, small, =[]x[]" where [] is an integer'))))
        search_filter.addrule("size", format_size_func)
        # licence filter
        license_code = {"creativecommons": "licenseType-Any", "publicdomain": "license-L1", "noncommercial": "license-L2_L3_L4_L5_L6_L7", "commercial": "license-L2_L3_L4", "noncommercial,modify": "license-L2_L3_L5_L6", "commercial,modify": "license-L2_L3"}
        format_license_func, license_choices = lambda lic: "+filterui:" + license_code[lic], list(license_code.keys())
        search_filter.addrule("license", format_license_func, license_choices)
        # layout filter
        layout_choices = ["square", "wide", "tall"]
        search_filter.addrule("layout", lambda x: "+filterui:aspect-" + x, layout_choices)
        # people filter
        people_choices = ["face", "portrait"]
        search_filter.addrule("people", lambda x: "+filterui:face-" + x, people_choices)
        # date filter
        date_minutes = {"pastday": 1440, "pastweek": 10080, "pastmonth": 43200, "pastyear": 525600}
        format_date_func, date_choices = lambda d: "+filterui:age-lt" + str(date_minutes[d]), list(date_minutes.keys())
        search_filter.addrule("date", format_date_func, date_choices)
        # return
        return search_filter