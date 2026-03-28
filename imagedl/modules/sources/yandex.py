'''
Function:
    Implementation of YandexImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import math
import html
import json_repair
from urllib.parse import quote
from .base import BaseImageClient
from ..utils import Filter, ImageInfo


'''YandexImageClient'''
class YandexImageClient(BaseImageClient):
    source = 'YandexImageClient'
    CANDIDATE_DOMAINS = ['https://yandex.com', 'https://yandex.ru', 'https://yandex.kz', 'https://yandex.by', 'https://yandex.com.tr']
    def __init__(self, **kwargs):
        if 'maintain_session' not in kwargs: kwargs['maintain_session'] = True
        super(YandexImageClient, self).__init__(**kwargs)
        self.default_search_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Accept-Encoding': 'gzip, deflate, br, zstd', 'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        # parse
        search_result, image_infos = html.unescape(search_result).replace("\n", "").replace("\r", ""), []
        m = re.search(r'id="ImagesApp-[^"]*"\s*data-state="({.*?})"\s*data-hydrate-priority=', search_result, re.S)
        data_state = json_repair.loads(html.unescape(m.group(1)))
        try: entities = data_state["initialState"]["serpList"]["items"]["entities"]
        except Exception: return image_infos
        if not entities or not isinstance(entities, dict): return image_infos
        # construct valid image infos
        for item in entities.values():
            if not isinstance(item, dict): continue
            candidate_urls = [item.get('origUrl'), f"https:{item.get('image')}" if item.get('image') and not str(item.get('image')).startswith('http') else item.get('image'), (item.get("viewerData", {}) or {}).get("img_href")]
            image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=candidate_urls, identifier=item.get('id') or candidate_urls[0]))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword, search_limits=1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, base_url = request_overrides or {}, '{domain}/images/search?text={keyword}&p={page}'
        for domain in YandexImageClient.CANDIDATE_DOMAINS:
            try: self.session.get(domain, timeout=10).raise_for_status(); break
            except Exception: continue
        filter_str, search_urls, page_size = self._getfilter().apply(filters, sep='&'), [], 30
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            search_url = base_url.format(domain=domain, keyword=quote(keyword), page=pn+1)
            search_urls.append((search_url if not filter_str else (search_url + f'&{filter_str}')))
        return search_urls
    '''_getfilter'''
    def _getfilter(self):
        search_filter = Filter()
        raise_err_func = lambda e: (_ for _ in ()).throw(e)
        # isize filter
        format_size_func = lambda size: (f"isize={size}" if size in ["large", "medium", "small", "wallpaper"] else ((lambda wh: (f"isize=eq&iw={wh[0]}&ih={wh[1]}" if len(wh) == 2 and wh[0].isdigit() and wh[1].isdigit() else raise_err_func(AssertionError('custom size must be in format "=WIDTHxHEIGHT"'))))(str(size)[1:].split("x")) if str(size).startswith("=") else raise_err_func(ValueError('filter option "isize" must be one of: "large", "medium", "small", "wallpaper", "=<int>x<int>"'))))
        search_filter.addrule("isize", format_size_func)
        # iorient filter
        iorient_choices = ["horizontal", "vertical", "square"]
        search_filter.addrule("iorient", lambda x: f"iorient={x}", iorient_choices)
        # itype filter
        itype_choices = ["photo", "clipart", "lineart", "face"]
        search_filter.addrule("itype", lambda x: f"itype={x}", itype_choices)
        # icolor filter
        icolor_choices = ["color", "gray", "red", "orange", "yellow", "green", "cyan", "blue", "violet", "white", "black"]
        search_filter.addrule("icolor", lambda x: f"icolor={x}", icolor_choices)
        # file_type filter
        file_type_choices = ["jpg", "png", "gifan"]
        search_filter.addrule("file_type", lambda x: f"file_type={x}", file_type_choices)
        # return
        return search_filter