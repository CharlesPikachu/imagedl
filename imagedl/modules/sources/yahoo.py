'''
Function:
    Implementation of YahooImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import math
from html import unescape
from ..utils import Filter
from urllib.parse import quote
from .base import BaseImageClient


'''YahooImageClient'''
class YahooImageClient(BaseImageClient):
    source = 'YahooImageClient'
    def __init__(self, **kwargs):
        super(YahooImageClient, self).__init__(**kwargs)
        self.default_search_headers = {
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        }
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str):
        image_infos, seen = [], set()
        # extract from json
        for m in re.finditer(r'"imgurl":"(https?://[^"]+)"', search_result):
            url = m.group(1)
            url = unescape(url)
            url = url.replace("\\/", "/")
            if url in seen: continue
            seen.add(url)
            image_infos.append({"candidate_urls": [url], "raw_data": {"imgurl": url}, "identifier": url})
        # extract from <img src="...">
        for m in re.finditer(r"<img[^>]+src=\"(https?://[^\" ]+)\"", search_result):
            url = m.group(1)
            url = unescape(url)
            if url in seen: continue
            seen.add(url)
            image_infos.append({"candidate_urls": [url], "raw_data": {"src": url}, "identifier": url})
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides = request_overrides or {}
        base_url = "https://images.search.yahoo.com/search/images?p={keyword}&b={offset}"
        filter_str = self._getfilter().apply(filters, sep="&")
        search_urls, page_size = [], 20
        for page in range(math.ceil(search_limits * 1.2 / page_size)):
            offset = page * page_size + 1
            search_url = base_url.format(keyword=quote(keyword), offset=offset)
            if filter_str: search_url += f"&{filter_str}"
            search_urls.append(search_url)
        return search_urls
    '''_getfilter'''
    def _getfilter(self):
        search_filter = Filter()
        # size
        image_size_map = {"small": "small", "medium": "medium", "large": "large", "extralarge": "wallpaper", "wallpaper": "wallpaper"}
        def formatsize(size: str):
            return f"imgsz={image_size_map[size]}"
        search_filter.addrule("size", formatsize, list(image_size_map.keys()))
        # color
        image_color_map = {
            "color": "color", "bw": "bw", "red": "red", "orange": "orange", "yellow": "yellow", "green": "green", "teal": "teal",
            "blue": "blue", "purple": "purple", "pink": "pink", "brown": "brown", "black": "black", "gray": "gray", "white": "white",
        }
        def formatcolor(color: str):
            return f"imgc={image_color_map[color]}"
        search_filter.addrule("color", formatcolor, list(image_color_map.keys()))
        # type
        image_type_map = {"photo": "photo", "clipart": "clipart", "linedrawing": "linedrawing", "gif": "gif", "transparent": "transparent"}
        def formattype(img_type: str):
            return f"imgty={image_type_map[img_type]}"
        search_filter.addrule("type", formattype, list(image_type_map.keys()))
        # layout
        image_layout_map = {"square": "square", "wide": "wide", "tall": "tall"}
        def formatlayout(layout: str):
            return f"imga={image_layout_map[layout]}"
        search_filter.addrule("layout", formatlayout, list(image_layout_map.keys()))
        # people
        image_people_map = {"face": "face", "portrait": "portrait", "nonportrait": "nonportrait"}
        def formatpeople(people: str):
            return f"imgf={image_people_map[people]}"
        search_filter.addrule("people", formatpeople, list(image_people_map.keys()))
        # time
        image_time_map = {"day": "day", "week": "week", "month": "month", "year": "year"}
        def formattime(t: str):
            return f"imgt={image_time_map[t]}"
        search_filter.addrule("time", formattime, list(image_time_map.keys()))
        # license
        image_license_map = {"cc": "cc", "pd": "pd", "fsu": "fsu", "fsuc": "fsuc", "fmsu": "fmsu", "fmsuc": "fmsuc"}
        def formatlicense(lic: str):
            return f"imgl={image_license_map[lic]}"
        search_filter.addrule("license", formatlicense, list(image_license_map.keys()))
        # return
        return search_filter