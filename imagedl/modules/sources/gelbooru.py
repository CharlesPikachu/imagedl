'''
Function:
    Implementation of GelbooruImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import math
import html as ihtml
from bs4 import BeautifulSoup
from .base import BaseImageClient
from urllib.parse import quote, urlencode, urljoin


'''GelbooruImageClient'''
class GelbooruImageClient(BaseImageClient):
    source = 'GelbooruImageClient'
    def __init__(self, **kwargs):
        super(GelbooruImageClient, self).__init__(**kwargs)
        self.default_search_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "cookie": "PHPSESSID=ngt7lipci8vs7k5ualdrufj3id",
            "priority": "u=0, i",
            "referer": "https://gelbooru.com/index.php",
            "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        }
        self.default_download_headers = {}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str):
        # format search result
        soup = BeautifulSoup(search_result, "html.parser")
        # parse search result
        image_infos, base_url = [], 'https://gelbooru.com/'
        for item in soup.select("div.thumbnail-container article.thumbnail-preview"):
            a = item.find("a", href=True, id=True)
            img = item.find("img")
            if not a or not img: continue
            candidate_urls = []
            href = ihtml.unescape(a["href"])
            post_url = urljoin(base_url, href)
            try:
                image_url = BeautifulSoup(self.get(post_url).text, "lxml").select_one("img#image")["src"]
                if image_url: candidate_urls.append(image_url)
            except:
                pass
            thumb_src = (img.get("data-src") or img.get("data-original") or img.get("src"))
            thumbnail_url = urljoin(base_url, ihtml.unescape(thumb_src)) if thumb_src else None
            if thumbnail_url: candidate_urls.append(thumbnail_url)
            if not candidate_urls: continue
            image_info = {
                'candidate_urls': candidate_urls, 'raw_data': str(item), 'identifier': a.get('id') or candidate_urls[0],
            }
            image_infos.append(image_info)
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword, search_limits=1000, filters: dict = None, request_overrides: dict = None):
        request_overrides = request_overrides or {}
        base_url = 'https://gelbooru.com/index.php?'
        params = {'page': 'post', 's': 'list', 'tags': keyword, 'pid': 0}
        if filters is not None: params.update(filters)
        search_urls, page_size = [], 42
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params['pid'] = pn * page_size
            search_url = base_url + urlencode(params, quote_via=quote)
            search_urls.append(search_url)
        return search_urls