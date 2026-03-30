'''
Function:
    Implementation of LifeOfPixImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import math
import json_repair
from urllib.parse import quote
from .base import BaseImageClient
from ..utils import ImageInfo, cookies2string


'''LifeOfPixImageClient'''
class LifeOfPixImageClient(BaseImageClient):
    source = 'LifeOfPixImageClient'
    def __init__(self, **kwargs):
        kwargs['enable_search_curl_cffi'] = True
        super(LifeOfPixImageClient, self).__init__(**kwargs)
        self.default_search_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36", "Accept": "application/json, text/plain, */*", "Accept-Language": "en-US,en;q=0.9", "Referer": "https://www.lifeofpix.com/", "X-Requested-With": "XMLHttpRequest"}
        self.default_download_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos: list[ImageInfo] = []
        for item in search_result['data']:
            if not isinstance(item, dict): continue
            candidate_urls = [item.get('urlDownload'), item.get('url'), item.get('istockRelatedThumbnailLargeUrl'), item.get('istockRelatedThumbnailSmallUrl'), item.get('istockRelatedThumbnailPreviewUrl'), item.get('thumbnail'), item.get('istockRelatedThumbnailMosaicUrl')]
            if not (candidate_urls := [c for c in candidate_urls if c and str(c).startswith('http')]): continue
            image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=candidate_urls, identifier=item.get('id') or candidate_urls[0]))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, filters, search_urls, page_size = request_overrides or {}, filters or {}, [], 40
        request_overrides['impersonate'] = 'chrome131'; (resp := self.get("https://www.lifeofpix.com/", **request_overrides)).raise_for_status()
        if 'Cookie' not in self.default_headers: self.default_headers['Cookie'] = cookies2string(resp.cookies.get_dict())
        if 'Cookie' not in self.default_search_headers: self.default_search_headers['Cookie'] = cookies2string(resp.cookies.get_dict())
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            keyword = quote(re.sub(r'\s+', '-', keyword.strip()), safe='')
            search_urls.append(f"https://www.lifeofpix.com/api/search/photos/{keyword}/{page_size}.json?page={pn+1}")
        return search_urls