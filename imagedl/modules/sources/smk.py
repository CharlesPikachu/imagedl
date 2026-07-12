'''
Function:
    Implementation of SMKImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import math
import json_repair
from ..utils import ImageInfo
from .base import BaseImageClient
from urllib.parse import quote, urlencode


'''SMKImageClient'''
class SMKImageClient(BaseImageClient):
    source = 'SMKImageClient'
    def __init__(self, **kwargs):
        super(SMKImageClient, self).__init__(**kwargs)
        self.default_search_headers = {'Accept': 'application/json, text/plain, */*', 'Referer': 'https://open.smk.dk/', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',}
        self.default_download_headers = {'Referer': 'https://open.smk.dk/', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos: list[ImageInfo] = []
        for item in search_result.get('items', []) or []:
            if not isinstance(item, dict): continue
            candidate_download_urls = [item.get('image_native'), item.get('image_thumbnail'), *[url for alternative_image in (item.get('alternative_images', []) or []) if isinstance(alternative_image, dict) for url in (alternative_image.get('native'), alternative_image.get('thumbnail'),)],]
            candidate_download_urls = [str(url) for url in candidate_download_urls if url and str(url).startswith('http')]
            if not (candidate_download_urls := list(dict.fromkeys(candidate_download_urls))): continue
            image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=candidate_download_urls, identifier=str(item.get('id') or item.get('object_number') or candidate_download_urls[0])))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None) -> list[str]:
        filters, request_overrides, base_url = dict(filters or {}), request_overrides or {}, 'https://api.smk.dk/api/v1/art/search/?'
        page_size = min(max(int(filters.get('rows', 100) or 100), 1), 100)
        (params := {'keys': keyword, 'filters': '[public_domain:true],[has_image:true]', 'offset': 0, 'rows': page_size}).update(filters)
        params['rows'] = page_size; search_urls, num_pages = [], math.ceil(search_limits * 1.2 / page_size)
        for page_idx in range(num_pages):
            params['offset'] = page_idx * page_size
            search_urls.append(base_url + urlencode(params, quote_via=quote))
        return search_urls