'''
Function:
    Implementation of EverypixelImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import math
import json_repair
from .base import BaseImageClient
from urllib.parse import quote, urlencode
from ..utils import ImageInfo, DrissionPageUtils


'''EverypixelImageClient'''
class EverypixelImageClient(BaseImageClient):
    source = 'EverypixelImageClient'
    def __init__(self, **kwargs):
        super(EverypixelImageClient, self).__init__(**kwargs)
        self.default_search_headers = {}
        self.default_download_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_updateheaders'''
    def _updateheaders(self, request_overrides: dict = None):
        request_overrides = request_overrides or {}
        page = DrissionPageUtils.initsmartbrowser(headless=False, requests_headers=None, requests_proxies=(request_overrides.get('proxies') or self._autosetproxies()), requests_cookies=(request_overrides.get('cookies') or self.default_cookies))
        page.get('https://www.everypixel.com/'); search_input = page.ele('xpath://input[@name="q"]', timeout=30)
        page.listen.start('everypixel.com/q/'); search_input.input('cute dogs\n')
        if (packet := page.listen.wait(timeout=10)): self.default_search_headers = {k: v for k, v in packet.request.headers.items() if not str(k).startswith(':')}
        self.default_headers = self.default_search_headers; self._initsession(); DrissionPageUtils.quitpage(page=page)
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        # parse json text in safety
        if not (loaded_search_result := json_repair.loads(search_result)['images']): return []
        search_result: list = list(); loaded_search_result = dict(loaded_search_result)
        for v in list(loaded_search_result.values()): search_result.extend(v if isinstance(v, list) else [])
        # parse search result
        image_infos: list[ImageInfo] = []
        for item in search_result:
            if not isinstance(item, dict) or ('url' not in item) or (not str(item.get('url')).startswith('http')): continue
            image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=[item.get('url')], identifier=item.get('basic_img_id') or item.get('id') or item.get('url')))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        self._updateheaders(request_overrides=request_overrides)
        request_overrides, filters, base_url = request_overrides or {}, filters or {}, 'https://www.everypixel.com/search/search?'
        (params := {'q': keyword, 'is_id': 64, 'limit': 50, 'json': '1', 'page': 1}).update(filters)
        search_urls, page_size = [], int(params['limit'])
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params['page'] = pn + 1
            search_urls.append(base_url + urlencode(params, quote_via=quote))
        return search_urls