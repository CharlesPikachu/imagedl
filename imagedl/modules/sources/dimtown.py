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
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "cookie": "__51vcke__JZppyXW5DeKCSZk8=5c1bbd1a-d73a-5d13-9aa2-5dd9721b8ce0; __51vuft__JZppyXW5DeKCSZk8=1769143410944; __51huid__JieOvjzcuEiglXrs=1a98ddd3-6282-5d21-b962-7cd4bbc48981; Hm_lvt_48244fdab9dbbc97b6ce8beb51cc13a0=1769143411; HMACCOUNT=E9868533209C5410; b2176320bb0b751ada5073d38a32a653=725d89369d1ba7b8f15c340a1eaf8a98; __vtins__JZppyXW5DeKCSZk8=%7B%22sid%22%3A%20%2254d0e761-8600-5a08-ad42-bfc4bdb82a36%22%2C%20%22vd%22%3A%201%2C%20%22stt%22%3A%200%2C%20%22dr%22%3A%200%2C%20%22expires%22%3A%201769150967810%2C%20%22ct%22%3A%201769149167810%7D; __51uvsct__JZppyXW5DeKCSZk8=2; Hm_lpvt_48244fdab9dbbc97b6ce8beb51cc13a0=1769149168",
            "priority": "u=0, i",
            "referer": "https://dimtown.com",
            "sec-ch-ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Google Chrome\";v=\"144\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
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
            except: continue
            soup, post_urls, seen = BeautifulSoup(resp.text, "html.parser"), [], set()
            for a in soup.select('ul#index_ajax_list a[target="_blank"][href]'):
                url = a["href"].strip()
                if DimTownImageClient.POST_URL_RE.fullmatch(url) and url not in seen: seen.add(url); post_urls.append(url)
            search_urls.extend(post_urls)
        return search_urls