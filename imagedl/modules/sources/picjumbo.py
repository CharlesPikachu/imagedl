'''
Function:
    Implementation of PicJumboImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import math
from lxml import html
from ..utils import ImageInfo
from urllib.parse import quote
from .base import BaseImageClient


'''PicJumboImageClient'''
class PicJumboImageClient(BaseImageClient):
    source = 'PicJumboImageClient'
    def __init__(self, **kwargs):
        super(PicJumboImageClient, self).__init__(**kwargs)
        self.default_search_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"}
        self.default_download_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        # parse with lxml
        tree = html.fromstring(search_result)
        # parse search result
        image_infos: list[ImageInfo] = []
        for item in tree.xpath('//div[contains(@class,"photo_query")]//div[contains(@class,"photo_item")]'):
            candidate_urls = sorted([{'url': ('https:' + u if u.startswith('//') else u), 'w': int(w[:-1])} for u, w in (x.strip().split() for x in item.xpath('.//img/@srcset')[0].split(','))], key=lambda x: x['w'], reverse=True)
            candidate_urls = [c['url'] for c in candidate_urls if c and isinstance(c, dict) and c.get('url')]
            image_infos.append(ImageInfo(source=self.source, raw_data=str(item), candidate_download_urls=candidate_urls, identifier=candidate_urls[0], description=item.xpath('.//h3/text()')[0].strip()))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, filters, search_urls, page_size = request_overrides or {}, filters or {}, [], 20
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            search_urls.append(f'https://picjumbo.com/search/{quote(keyword, safe="")}/page/{pn+1}/')
        return search_urls