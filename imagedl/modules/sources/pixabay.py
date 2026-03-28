'''
Function:
    Implementation of PixabayImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import math
import random
import json_repair
from urllib.parse import quote
from .base import BaseImageClient
from ..utils import Filter, ImageInfo


'''PixabayImageClient'''
class PixabayImageClient(BaseImageClient):
    source = 'PixabayImageClient'
    CANDIDATE_API_KEYS = [
        '52293499-20edab5a9aeb2872ddc6cf68d', '51464414-1d83eb06bfdf3164b71156c0d', '50096047-8bb459140d4c19e045f4f2381', '35428194-f806941a429b19ee5838722ec',
        '43843784-ca8a7d4eb022dffa63faad957', '34748321-56ec586673804760cca13f7f6', '22850428-9964a4ca16315545d67c15abc', '20524560-a948ec896d1e8c0b8ba1135a6',
        '20583871-24538aa0638807f136238470d', '34787804-1aefa27f7d66275b11fe28ff3', '15089766-5bf9896a3416c7dcc335047dc', '47820586-1bbcb8dfd700ccd5c12e5d9e1',
    ]
    API_KEY = random.choice(CANDIDATE_API_KEYS)
    def __init__(self, api_key: str = None, **kwargs):
        super(PixabayImageClient, self).__init__(**kwargs)
        PixabayImageClient.API_KEY = api_key if api_key is not None else PixabayImageClient.API_KEY
        self.default_search_headers = {'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Referer': 'keep-alive', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos: list[ImageInfo] = []
        for item in (search_result.get('hits', []) or []):
            if not isinstance(item, dict): continue
            candidate_urls = [item.get('fullHDURL'), item.get('imageURL'), item.get('largeImageURL'), item.get('webformatURL'), item.get('previewURL')]
            if not (candidate_urls := [c for c in candidate_urls if c and str(c).startswith('http')]): continue
            image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=candidate_urls, identifier=item.get('id') or candidate_urls[0]))
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, filter_str, search_urls, page_size = request_overrides or {}, self._getfilter().apply(filters, sep='&'), [], 20
        base_url = 'https://pixabay.com/api/?key={api_key}&q={keyword}&per_page={page_size}&page={page}'
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            search_url = base_url.format(api_key=PixabayImageClient.API_KEY, keyword=quote(keyword), page_size=page_size, page=pn+1)
            search_urls.append((search_url if not filter_str else (search_url + f'&{filter_str}')))
        return search_urls
    '''_getfilter'''
    def _getfilter(self):
        search_filter = Filter()
        raise_err_func = lambda e: (_ for _ in ()).throw(e)
        # lang filter
        lang_choices = ["cs", "da", "de", "en", "es", "fr", "id", "it", "hu", "nl", "no", "pl", "pt", "ro", "sk", "fi", "sv", "tr", "vi", "th", "bg", "ru", "el", "ja", "ko", "zh"]
        search_filter.addrule("lang", lambda v: f"lang={v}", lang_choices)
        # id filter
        search_filter.addrule("id", lambda v: f"id={v}", str)
        # image_type filter
        image_type_choices = ["all", "photo", "illustration", "vector"]
        search_filter.addrule("image_type", lambda v: f"image_type={v}", image_type_choices)
        # orientation filter
        orientation_choices = ["all", "horizontal", "vertical"]
        search_filter.addrule("orientation", lambda v: f"orientation={v}", orientation_choices)
        # category filter
        category_choices = ["backgrounds", "fashion", "nature", "science", "education", "feelings", "health", "people", "religion", "places", "animals", "industry", "computer", "food", "sports", "transportation", "travel", "buildings", "business", "music"]
        search_filter.addrule("category", lambda v: f"category={v}", category_choices)
        # size filter
        search_filter.addrule("min_width", lambda v: f"min_width={int(v)}", int)
        search_filter.addrule("min_height", lambda v: f"min_height={int(v)}", int)
        # colors filter
        color_allowed = {"grayscale", "transparent", "red", "orange", "yellow", "green", "turquoise", "blue", "lilac", "pink", "white", "gray", "black", "brown"}
        format_colors_func = lambda v: ((lambda vals: (raise_err_func(ValueError('filter option "colors" has invalid value(s): {}'.format(", ".join(invalid)))) if (invalid := [c for c in vals if c not in color_allowed]) else "colors=" + ",".join(vals)))([s.strip() for s in v.split(",") if s.strip()] if isinstance(v, str) else [str(s).strip() for s in v] if isinstance(v, (list, tuple, set)) else raise_err_func(TypeError('filter option "colors" must be a comma-separated string or list/tuple/set of strings'))))
        search_filter.addrule("colors", format_colors_func)
        # editors_choice filter
        search_filter.addrule("editors_choice", lambda v: f"editors_choice={'true' if v else 'false'}", bool)
        # safesearch filter
        search_filter.addrule("safesearch", lambda v: f"safesearch={'true' if v else 'false'}", bool)
        # order filter
        order_choices = ["popular", "latest"]
        search_filter.addrule("order", lambda v: f"order={v}", order_choices)
        # callback filter
        search_filter.addrule("callback", lambda v: f"callback={v}", str)
        # pretty filter
        search_filter.addrule("pretty", lambda v: f"pretty={'true' if v else 'false'}", bool)
        # return
        return search_filter