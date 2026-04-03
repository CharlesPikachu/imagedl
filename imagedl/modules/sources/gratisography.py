'''
Function:
    Implementation of GratisoGraphyImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import math
from bs4 import BeautifulSoup
from ..utils import ImageInfo
from .base import BaseImageClient
from urllib.parse import quote, urljoin


'''GratisoGraphyImageClient'''
class GratisoGraphyImageClient(BaseImageClient):
    source = 'GratisoGraphyImageClient'
    def __init__(self, **kwargs):
        super(GratisoGraphyImageClient, self).__init__(**kwargs)
        self.default_search_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7", "cache-control": "max-age=0", "sec-fetch-user": "?1", "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"', 
            "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": '"Windows"', "sec-fetch-dest": "document", "sec-fetch-mode": "navigate", "sec-fetch-site": "none", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36", "upgrade-insecure-requests": "1", "priority": "u=0, i", 
        }
        self.default_download_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7", "cache-control": "max-age=0", "sec-fetch-user": "?1", "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"', 
            "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": '"Windows"', "sec-fetch-dest": "document", "sec-fetch-mode": "navigate", "sec-fetch-site": "none", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36", "upgrade-insecure-requests": "1", "priority": "u=0, i", 
        }
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        image_infos, soup, urls, base_url = [], BeautifulSoup(search_result, 'lxml'), {}, 'https://gratisography.com'
        score_func = lambda u: int(m.group(1)) * int(m.group(2)) if (m := re.search(r'-(\d+)x(\d+)(?=\.\w+(?:\?|$))', u)) else (int(m.group(1)) if (m := re.search(r'[?&](?:w|width)=(\d+)', u)) else 0)
        for art in soup.select('.search-grid article[id^="single-photo-"]'):
            for img in art.select("img"):
                for k in ("src", "data-src", "data-lazy-src"):
                    if (u := img.get(k)): u = urljoin(base_url, u); urls[u] = max(urls.get(u, 0), score_func(u))
                for k in ("srcset", "data-srcset"):
                    if (ss := img.get(k)):
                        for x in ss.split(","): (p := x.strip().split()) and urls.__setitem__((u := urljoin(base_url, p[0])), max(urls.get(u, 0), int(p[1][:-1]) if len(p) > 1 and p[1].endswith("w") else score_func(u)))
            candidate_urls = list(urls.keys()); urls = {}; image_infos.append(ImageInfo(source=self.source, raw_data=str(art), candidate_download_urls=candidate_urls, identifier=candidate_urls[0]))
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, search_urls, page_size, filters = request_overrides or {}, [], 10, filters or {}
        base_url = 'https://gratisography.com/page/{page}/?s={keyword}'
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            search_url = base_url.format(keyword=quote(keyword), page=pn+1)
            search_urls.append(search_url)
        return search_urls