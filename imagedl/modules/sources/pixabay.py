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
from ..utils import Filter
from urllib.parse import quote
from .base import BaseImageClient


'''PixabayImageClient'''
class PixabayImageClient(BaseImageClient):
    source = 'PixabayImageClient'
    def __init__(self, api_key=None, **kwargs):
        super(PixabayImageClient, self).__init__(**kwargs)
        self.default_search_headers = {
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'Referer': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.default_headers = self.default_search_headers
        self._initsession()
        self.api_key = random.choice([
            '52293499-20edab5a9aeb2872ddc6cf68d', '51464414-1d83eb06bfdf3164b71156c0d', '50096047-8bb459140d4c19e045f4f2381', '35428194-f806941a429b19ee5838722ec',
            '43843784-ca8a7d4eb022dffa63faad957', '34748321-56ec586673804760cca13f7f6', '22850428-9964a4ca16315545d67c15abc', '20524560-a948ec896d1e8c0b8ba1135a6',
            '20583871-24538aa0638807f136238470d', '34787804-1aefa27f7d66275b11fe28ff3', '15089766-5bf9896a3416c7dcc335047dc', '47820586-1bbcb8dfd700ccd5c12e5d9e1',
        ]) if api_key is None else api_key
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str):
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos = []
        for item in search_result.get('hits', []):
            candidate_urls = []
            if ('fullHDURL' in item) and isinstance(item['fullHDURL'], str) and item['fullHDURL'].strip():
                candidate_urls.append(item['fullHDURL'])
            if ('imageURL' in item) and isinstance(item['imageURL'], str) and item['imageURL'].strip():
                candidate_urls.append(item['imageURL'])
            if ('largeImageURL' in item) and isinstance(item['largeImageURL'], str) and item['largeImageURL'].strip():
                candidate_urls.append(item['largeImageURL'])
            if ('webformatURL' in item) and isinstance(item['webformatURL'], str) and item['webformatURL'].strip():
                candidate_urls.append(item['webformatURL'])
            if ('previewURL' in item) and isinstance(item['previewURL'], str) and item['previewURL'].strip():
                candidate_urls.append(item['previewURL'])
            image_info = {
                'candidate_urls': candidate_urls, 'raw_data': item, 'identifier': item['id'],
            }
            image_infos.append(image_info)
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword, search_limits=1000, filters: dict = None):
        base_url = 'https://pixabay.com/api/?key={api_key}&q={keyword}&per_page={page_size}&page={page}'
        filter_str = self._getfilter().apply(filters, sep='&')
        search_urls, page_size = [], 20
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            search_url = base_url.format(api_key=self.api_key, keyword=quote(keyword), page_size=page_size, page=pn+1)
            if filter_str: search_url += f'&{filter_str}'
            search_urls.append(search_url)
        return search_urls
    '''_getfilter'''
    def _getfilter(self):
        search_filter = Filter()
        # lang filter
        lang_choices = ["cs","da","de","en","es","fr","id","it","hu","nl","no","pl","pt","ro","sk","fi","sv","tr","vi","th","bg","ru","el","ja","ko","zh"]
        def formatlang(v: str):
            return f"lang={v}"
        search_filter.addrule("lang", formatlang, lang_choices)
        # id filter
        def formatid(v: str):
            return f"id={v}"
        search_filter.addrule("id", formatid, str)
        # image_type filter
        image_type_choices = ["all", "photo", "illustration", "vector"]
        def formatimagetype(v: str):
            return f"image_type={v}"
        search_filter.addrule("image_type", formatimagetype, image_type_choices)
        # orientation filter
        orientation_choices = ["all", "horizontal", "vertical"]
        def formatorientation(v: str):
            return f"orientation={v}"
        search_filter.addrule("orientation", formatorientation, orientation_choices)
        # category filter
        category_choices = [
            "backgrounds","fashion","nature","science","education","feelings","health","people",
            "religion","places","animals","industry","computer","food","sports","transportation",
            "travel","buildings","business","music"
        ]
        def formatcategory(v: str):
            return f"category={v}"
        search_filter.addrule("category", formatcategory, category_choices)
        # size filter
        def formatminwidth(v: int):
            return f"min_width={int(v)}"
        search_filter.addrule("min_width", formatminwidth, int)
        def formatminheight(v: int):
            return f"min_height={int(v)}"
        search_filter.addrule("min_height", formatminheight, int)
        # colors filter
        color_allowed = {
            "grayscale","transparent","red","orange","yellow","green","turquoise",
            "blue","lilac","pink","white","gray","black","brown"
        }
        def formatcolors(v):
            if isinstance(v, str):
                vals = [s.strip() for s in v.split(",") if s.strip()]
            elif isinstance(v, (list, tuple, set)):
                vals = [str(s).strip() for s in v]
            else:
                raise TypeError('filter option "colors" must be a comma-separated string or list/tuple/set of strings')
            invalid = [c for c in vals if c not in color_allowed]
            if invalid:
                raise ValueError('filter option "colors" has invalid value(s): {}'.format(", ".join(invalid)))
            return "colors=" + ",".join(vals)
        search_filter.addrule("colors", formatcolors)
        # editors_choice filter
        def formateditorschoice(v: bool):
            return f"editors_choice={'true' if v else 'false'}"
        search_filter.addrule("editors_choice", formateditorschoice, bool)
        # safesearch filter
        def formatsafesearch(v: bool):
            return f"safesearch={'true' if v else 'false'}"
        search_filter.addrule("safesearch", formatsafesearch, bool)
        # order filter
        order_choices = ["popular", "latest"]
        def formatorder(v: str):
            return f"order={v}"
        search_filter.addrule("order", formatorder, order_choices)
        # callback filter
        def formatcallback(v: str):
            return f"callback={v}"
        search_filter.addrule("callback", formatcallback, str)
        # pretty filter
        def formatpretty(v: bool):
            return f"pretty={'true' if v else 'false'}"
        search_filter.addrule("pretty", formatpretty, bool)
        # return
        return search_filter