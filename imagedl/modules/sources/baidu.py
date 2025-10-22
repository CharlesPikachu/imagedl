'''
Function:
    Implementation of BaiduImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import math
import json_repair
from urllib.parse import quote
from .base import BaseImageClient
from ..utils import lowerdictkeys, Filter


'''BaiduImageClient'''
class BaiduImageClient(BaseImageClient):
    source = 'BaiduImageClient'
    def __init__(self, **kwargs):
        super(BaiduImageClient, self).__init__(**kwargs)
        self.default_search_headers = {
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str):
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # pick all image urls
        def pickallimageurls(item: dict):
            candidate_urls = []
            # --all lower letters for keys with str type
            item = lowerdictkeys(item)
            # --parse try1
            if ('objurl' in item) and isinstance(item['objurl'], str) and item['objurl'].strip():
                candidate_urls.append(self._parseurl(item['objurl'].strip()))
            # --parse try2
            if ('hoverurl' in item) and isinstance(item['hoverurl'], str) and item['hoverurl'].strip():
                candidate_urls.append(item['hoverurl'].strip())
            # --parse try3
            for r in item.get("replaceurl", []):
                r = lowerdictkeys(r)
                if ('objurl' in r) and isinstance(r['objurl'], str) and r['objurl'].strip():
                    candidate_urls.append(r['objurl'].strip())
            # --parse try4
            if ('middleurl' in item) and isinstance(item['middleurl'], str) and item['middleurl'].strip():
                candidate_urls.append(item['middleurl'].strip())
            # --parse try5
            if ('thumburl' in item) and isinstance(item['thumburl'], str) and item['thumburl'].strip():
                candidate_urls.append(item['thumburl'].strip())
            # --return
            return candidate_urls
        # parse search result
        image_infos = []
        for item in search_result.get('data', []):
            if not isinstance(item, dict): continue
            candidate_urls = pickallimageurls(item=item)
            if not candidate_urls: continue
            image_info = {
                'candidate_urls': candidate_urls, 'raw_data': item, 'identifier': candidate_urls[0],
            }
            image_infos.append(image_info)
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword, search_limits=1000, filters: dict = None):
        base_url = 'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&word={}&pn={}&rn={}'
        filter_str = self._getfilter().apply(filters, sep="&")
        search_urls, page_size = [], 30
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            search_url = base_url.format(quote(keyword), pn * page_size, page_size)
            if filter_str: search_url += f'&{filter_str}'
            search_urls.append(search_url)
        return search_urls
    '''_parseurl'''
    def _parseurl(self, url: str):
        in_table, out_table = '0123456789abcdefghijklmnopqrstuvw', '7dgjmoru140852vsnkheb963wtqplifca'
        translate_table = str.maketrans(in_table, out_table)
        mapping = {'_z2C$q': ':', '_z&e3B': '.', 'AzdH3F': '/'}
        for k, v in mapping.items():
            url = url.replace(k, v)
        return url.translate(translate_table)
    '''_getfilter: refer to https://github.com/hellock/icrawler/blob/master/icrawler/builtin/baidu.py'''
    def _getfilter(self):
        search_filter = Filter()
        # type filter
        type_code = {
            "portrait": "s=3&lm=0&st=-1&face=0", "face": "s=0&lm=0&st=-1&face=1", "clipart": "s=0&lm=0&st=1&face=0", "linedrawing": "s=0&lm=0&st=2&face=0",
            "animated": "s=0&lm=6&st=-1&face=0", "static": "s=0&lm=7&st=-1&face=0",
        }
        def formattype(img_type):
            return type_code[img_type]
        type_choices = list(type_code.keys())
        search_filter.addrule("type", formattype, type_choices)
        # color filter
        color_code = {
            "red": 1, "orange": 256, "yellow": 2, "green": 4, "purple": 32, "pink": 64,
            "teal": 8, "blue": 16, "brown": 12, "white": 1024, "black": 512, "blackandwhite": 2048,
        }
        def formatcolor(color):
            return f"ic={color_code[color]}"
        color_choices = list(color_code.keys())
        search_filter.addrule("color", formatcolor, color_choices)
        # size filter
        def formatsize(size: str):
            if size in ["extralarge", "large", "medium", "small"]:
                size_code = {"extralarge": 9, "large": 3, "medium": 2, "small": 1}
                return f"z={size_code[size]}"
            elif size.startswith("="):
                wh = size[1:].split("x")
                assert len(wh) == 2
                return "width={}&height={}".format(*wh)
            else:
                raise ValueError('filter option "size" must be one of the following: `extralarge, large, medium, small, =[]x[]`, where [] is an integer')
        search_filter.addrule("size", formatsize)
        # return
        return search_filter