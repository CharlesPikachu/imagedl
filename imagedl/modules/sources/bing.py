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
from ..utils import Filter
from bs4 import BeautifulSoup
from urllib.parse import quote
from .base import BaseImageClient


'''BingImageClient'''
class BingImageClient(BaseImageClient):
    source = 'BingImageClient'
    def __init__(self, **kwargs):
        super(BingImageClient, self).__init__(**kwargs)
        self.default_search_headers = {
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str):
        image_infos = []
        soup = BeautifulSoup(search_result, 'lxml')
        pattern = re.compile(r'"murl\":\"(.*?)\"')
        for item in soup.find_all('div', class_='imgpt'):
            try:
                href_str = html.unescape(item.a["m"])
            except:
                continue
            match = pattern.search(href_str)
            if not match: continue
            if not match.group(1).strip(): continue
            image_info = {
                'candidate_urls': [match.group(1).strip()], 'raw_data': str(item), 'identifier': match.group(1).strip(),
            }
            image_infos.append(image_info)
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword, search_limits=1000, filters: dict = None):
        base_url = 'https://www.bing.com/images/async?q={keyword}&first={page}'
        filter_str = self._getfilter().apply(filters)
        filter_str = "&qft=" + filter_str if filter_str else ""
        search_urls, page_size = [], 20
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            search_url = base_url.format(keyword=quote(keyword), page=pn*page_size) + filter_str
            search_urls.append(search_url)
        return search_urls
    '''_getfilter: refer to https://github.com/hellock/icrawler/blob/master/icrawler/builtin/bing.py'''
    def _getfilter(self):
        search_filter = Filter()
        # type filter
        def formattype(img_type):
            prefix = "+filterui:photo-"
            return prefix + "animatedgif" if img_type == "animated" else prefix + img_type
        type_choices = ["photo", "clipart", "linedrawing", "transparent", "animated"]
        search_filter.addrule("type", formattype, type_choices)
        # color filter
        def formatcolor(color: str):
            prefix = "+filterui:color2-"
            if color == "color": return prefix + "color"
            elif color == "blackandwhite": return prefix + "bw"
            else: return prefix + "FGcls_" + color.upper()
        color_choices = [
            "color", "blackandwhite", "red", "orange", "yellow", "green", "teal", "blue", "purple",
            "pink", "white", "gray", "black", "brown",
        ]
        search_filter.addrule("color", formatcolor, color_choices)
        # size filter
        def formatsize(size: str):
            if size in ["large", "medium", "small"]:
                return "+filterui:imagesize-" + size
            elif size == "extralarge":
                return "+filterui:imagesize-wallpaper"
            elif size.startswith("="):
                wh = size[1:].split("x")
                assert len(wh) == 2
                return "+filterui:imagesize-custom_{}_{}".format(*wh)
            else:
                raise ValueError('filter option "size" must be one of the following: "extralarge, large, medium, small, =[]x[]" where [] is an integer')
        search_filter.addrule("size", formatsize)
        # licence filter
        license_code = {
            "creativecommons": "licenseType-Any", "publicdomain": "license-L1", "noncommercial": "license-L2_L3_L4_L5_L6_L7", "commercial": "license-L2_L3_L4",
            "noncommercial,modify": "license-L2_L3_L5_L6", "commercial,modify": "license-L2_L3",
        }
        def formatlicense(license):
            return "+filterui:" + license_code[license]
        license_choices = list(license_code.keys())
        search_filter.addrule("license", formatlicense, license_choices)
        # layout filter
        layout_choices = ["square", "wide", "tall"]
        search_filter.addrule("layout", lambda x: "+filterui:aspect-" + x, layout_choices)
        # people filter
        people_choices = ["face", "portrait"]
        search_filter.addrule("people", lambda x: "+filterui:face-" + x, people_choices)
        # date filter
        date_minutes = {"pastday": 1440, "pastweek": 10080, "pastmonth": 43200, "pastyear": 525600}
        def formatdate(date):
            return "+filterui:age-lt" + str(date_minutes[date])
        date_choices = list(date_minutes.keys())
        search_filter.addrule("date", formatdate, date_choices)
        # return
        return search_filter