'''
Function:
    Implementation of YahooImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import math
from ..utils import Filter
from bs4 import BeautifulSoup
from urllib.parse import quote
from .base import BaseImageClient


'''YahooImageClient'''
class YahooImageClient(BaseImageClient):
    source = 'YahooImageClient'
    def __init__(self, **kwargs):
        super(YahooImageClient, self).__init__(**kwargs)
        self.default_search_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "cookie": "GUC=AQEBCAFpK8ZpV0Ie7wSF&s=AQAAAAfiqwF_&g=aSp9bA; A1=d=AQABBDJQFWcCEMJwcR6f1oZWsTrFgsJ3yAkFEgEBCAHGK2lXadwr0iMA_eMDAAcIMlAVZ8J3yAk&S=AQAAAtxogq22gSrqBlASwUXzjM4; A3=d=AQABBDJQFWcCEMJwcR6f1oZWsTrFgsJ3yAkFEgEBCAHGK2lXadwr0iMA_eMDAAcIMlAVZ8J3yAk&S=AQAAAtxogq22gSrqBlASwUXzjM4; _ga=GA1.1.376091485.1764392311; axids=gam=y-gi4XaFlE2uIWDoRuMGBc84_CgmhvPV1W~A&dv360=eS1tMUJXZzI5RTJ1RW1hUXJrd3U4UWs0aC5MLmJsN2dQZX5B&ydsp=y-dzApDz5E2uLqPwEYzZSwx87F3DHhX2JO~A&tbla=y-YzJ9rXBE2uLHZ_QZLcZnJYpyLcPwzG3S~A; tbla_id=f7e07dff-176b-46ef-932e-9b1441f60525-tuct8b1b787; A1S=d=AQABBDJQFWcCEMJwcR6f1oZWsTrFgsJ3yAkFEgEBCAHGK2lXadwr0iMA_eMDAAcIMlAVZ8J3yAk&S=AQAAAtxogq22gSrqBlASwUXzjM4; cmp=t=1765034846&j=0&u=1---; gpp=DBAA; gpp_sid=-1; lkl=v=2&w=sFLKrWIPBmyF6MJjiEqG5ck2f.RU_PA6xW7o; ymuid=v=13B3697304196A5800087C6F05186BDB&ts=1765034898; _ga_B40QGCQW3G=GS2.1.s1765034845$o2$g1$t1765034909$j60$l0$h0; _ga_40HG6NTJFD=GS2.1.s1765043333$o3$g1$t1765045062$j47$l0$h0; yisn=lrs=1&=undefined&h=48&d=1521x346&dwh=1521x268",
            "priority": "u=0, i",
            "sec-ch-ua": "\"Chromium\";v=\"142\", \"Google Chrome\";v=\"142\", \"Not_A Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        }
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str):
        soup = BeautifulSoup(search_result, "lxml")
        image_infos = []
        results_root = (soup.find("div", id="sres") or soup.find("div", id="results") or soup.find("div", {"class": "results"}) or soup)
        def addimagefromnode(node, url_list):
            urls = []
            for u in url_list:
                if not isinstance(u, str): continue
                u = u.strip()
                if not u: continue
                if u.startswith("data:"): continue
                urls.append(u)
            if not urls: return
            main_url = urls[0]
            raw_data = {str(k).lower(): v for k, v in (node.attrs or {}).items()}
            image_infos.append({"candidate_urls": urls, "raw_data": raw_data, "identifier": main_url})
        for img in results_root.find_all("img"):
            data_src = img.get("data-src")
            src = img.get("src")
            candidate_urls = []
            if data_src: candidate_urls.append(data_src)
            if src and src != data_src: candidate_urls.append(src)
            if not candidate_urls: continue
            flag_real = (
                img.get("data-pos") is not None or any(key in (data_src or "") or key in (src or "") for key in ("sp.yimg.com/ib/th", "mm.bing.net", "yimg.com", "bing.net"))
            )
            if not flag_real: continue
            addimagefromnode(img, candidate_urls)
        for a in results_root.find_all("a", attrs={"data-src": True}):
            data_src = a.get("data-src")
            if not data_src: continue
            addimagefromnode(a, [data_src])
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides = request_overrides or {}
        base_url = "https://images.search.yahoo.com/search/images?p={keyword}&b={offset}"
        filter_str = self._getfilter().apply(filters, sep="&")
        search_urls, page_size = [], 60
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