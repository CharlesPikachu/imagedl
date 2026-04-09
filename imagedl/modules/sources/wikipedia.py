'''
Function:
    Implementation of WikipediaImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import math
import primp
import random
import json_repair
from ..utils import ImageInfo
from .base import BaseImageClient
from fake_useragent import UserAgent
from urllib.parse import quote, urlencode


'''WikipediaImageClient'''
class WikipediaImageClient(BaseImageClient):
    source = 'WikipediaImageClient'
    def __init__(self, **kwargs):
        super(WikipediaImageClient, self).__init__(**kwargs)
        self.default_search_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"}
        self.default_download_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_initsession'''
    def _initsession(self):
        self.session = primp.Client(proxy=None, timeout=30, impersonate="random", impersonate_os="random", verify=True)
        self.session.headers_update(self.default_headers)
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos: list[ImageInfo] = []
        for item in dict(search_result['query']['pages']).values():
            if not isinstance(item, dict): continue
            candidate_urls = [i['url'] for i in (item.get('imageinfo') or []) if isinstance(i, dict) and i.get('url')]
            if not (candidate_urls := [c for c in candidate_urls if c and str(c).startswith('http')]): continue
            image_infos.extend([ImageInfo(source=self.source, raw_data=item, candidate_download_urls=[c], identifier=c) for c in candidate_urls])
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, filters, base_url = request_overrides or {}, filters or {}, "https://commons.wikimedia.org/w/api.php?"
        (params := {"action": "query", "generator": "search", "gsrsearch": keyword, "gsrlimit": 50, "gsroffset": 0, "prop": "imageinfo", "iiprop": "url", "format": "json", "gsrnamespace": 6}).update(filters)
        search_urls, page_size = [], int(params['gsrlimit'])
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params['gsroffset'] = pn * page_size
            search_urls.append(base_url + urlencode(params, quote_via=quote))
        return search_urls
    '''request'''
    def request(self, url: str, method: str, **kwargs):
        if 'cookies' not in kwargs: kwargs['cookies'] = self.default_cookies
        for _ in range(self.max_retries):
            if not self.maintain_session: self._initsession(); self.random_update_ua and self.session.headers.update({'User-Agent': UserAgent().random})
            proxies, resp = kwargs.pop('proxies', None) or self._autosetproxies(), None
            if proxies: self.session.proxy = random.choice(list(proxies.values())) if isinstance(proxies, dict) else proxies
            try: (resp := self.session.request(method, url, **kwargs)).raise_for_status()
            except Exception as err: self.logger_handle.error(f'{self.source}.request >>> {url} (Error: {err}; status={getattr(locals().get("resp"), "status_code", None)})', disable_print=self.disable_print); continue
            return resp
        return resp
    '''get'''
    def get(self, url, **kwargs): return self.request(url, method='GET', **kwargs)
    '''post'''
    def post(self, url, **kwargs): return self.request(url, method='POST', **kwargs)