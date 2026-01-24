'''
Function:
    Implementation of DimTownImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import math
from bs4 import BeautifulSoup
from .base import BaseImageClient


'''DimTownImageClient'''
class DimTownImageClient(BaseImageClient):
    source = 'DimTownImageClient'
    POST_URL_RE = re.compile(r"^https?://dimtown\.com/\d+\.html$")
    def __init__(self, **kwargs):
        super(DimTownImageClient, self).__init__(**kwargs)
        self.default_search_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str):
        # format search result
        soup = BeautifulSoup(search_result, "html.parser")
        # parse search result
        box, image_infos = soup.select_one("#content .content_left"), []
        real_urls = list(dict.fromkeys(u for tag, attr in (("a", "href"), ("img", "src")) for x in (box.select(f"{tag}[{attr}]") if box else []) for u in (x.get(attr),) if u and u.split("?", 1)[0].lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"))))
        for real_url in real_urls:
            image_info = {'candidate_urls': [real_url], 'raw_data': search_result, 'identifier': real_url}
            image_infos.append(image_info)
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits=1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, search_urls, page_size = request_overrides or {}, [], 25
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            try: resp = self.get(f'https://dimtown.com/page/{pn+1}?s={keyword}', **request_overrides); resp.raise_for_status()
            except: break
            soup, post_urls, seen = BeautifulSoup(resp.text, "html.parser"), [], set()
            for a in soup.select('ul#index_ajax_list a[target="_blank"][href]'):
                url = a["href"].strip()
                if DimTownImageClient.POST_URL_RE.fullmatch(url) and url not in seen: seen.add(url); post_urls.append(url)
            search_urls.extend(post_urls)
        return search_urls