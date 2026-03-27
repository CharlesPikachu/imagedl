'''
Function:
    Implementation of I360ImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import math
import json_repair
from urllib.parse import quote
from .base import BaseImageClient
from ..utils import Filter, ImageInfo


'''I360ImageClient'''
class I360ImageClient(BaseImageClient):
    source = 'I360ImageClient'
    def __init__(self, **kwargs):
        super(I360ImageClient, self).__init__(**kwargs)
        self.default_search_headers = {'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos: list[ImageInfo] = []
        for item in (search_result.get('list', []) or []):
            if not isinstance(item, dict): continue
            candidate_urls = [item.get('img'), item.get('thumb_bak'), item.get('thumb'), item.get('_thumb_bak'), item.get('_thumb')]
            if not (candidate_urls := [c for c in candidate_urls if c and str(c).startswith('http')]): continue
            image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=candidate_urls, identifier=item.get('id') or candidate_urls[0]))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, base_url = request_overrides or {}, 'https://image.so.com/j?pn={page_size}&q={keyword}&sn={page}'
        filter_str, search_urls, page_size = self._getfilter().apply(filters, sep='&'), [], 60
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            search_url = base_url.format(page_size=page_size, keyword=quote(keyword), page=pn*page_size)
            if filter_str: search_url += f'&{filter_str}'
            search_urls.append(search_url)
        return search_urls
    '''_getfilter'''
    def _getfilter(self):
        search_filter = Filter()
        raise_err_func = lambda e: (_ for _ in ()).throw(e)
        # size filter
        size_code = {"all": 0, "small": 1, "medium": 2, "large": 3, "extralarge": 4, "wallpaper": 4}
        format_size_func = lambda size: (f"z={size_code[size]}" if size in size_code else raise_err_func(ValueError('filter option "size" must be one of: "all", "small", "medium", "large", "extralarge", "wallpaper"')))
        search_filter.addrule("size", format_size_func, list(size_code.keys()))
        # color filter
        color_choices = ["red", "blue", "black", "white", "pink", "orange", "yellow", "green", "purple", "brown", "teal"]
        format_color_func = lambda color: (f"imgcolor={color}" if color in color_choices else raise_err_func(ValueError(f'filter option "color" must be one of: {", ".join(color_choices)}')))
        search_filter.addrule("color", format_color_func, color_choices)
        # custom minimum width / height filter
        format_min_size_func = lambda size: (f"imgw={w}&imgh={h}" if (isinstance(size, (tuple, list)) and len(size) == 2 and all(str(x).isdigit() for x in size) and (w := int(size[0])) > 0 and (h := int(size[1])) > 0) else (f"imgw={w}&imgh={h}" if (isinstance(size, str) and size.startswith("=") and len(wh := size[1:].lower().split("x")) == 2 and all(x.isdigit() for x in wh) and (w := int(wh[0])) > 0 and (h := int(wh[1])) > 0) else raise_err_func(ValueError('filter option "min_size" must be "=1920x1080" or (1920, 1080)'))))
        search_filter.addrule("min_size", format_min_size_func)
        # type filter
        type_code = {"animated": 1, "static": 2}
        format_type_func = lambda img_type: (f"stype={type_code[img_type]}" if img_type in type_code else raise_err_func(ValueError('filter option "type" must be one of: "animated", "static"')))
        search_filter.addrule("type", format_type_func, list(type_code.keys()))
        # return
        return search_filter