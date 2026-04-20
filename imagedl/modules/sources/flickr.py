'''
Function:
    Implementation of FlickrImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import math
import random
import json_repair
from ..utils import ImageInfo
from .base import BaseImageClient
from urllib.parse import quote, urlencode


'''FlickrImageClient'''
class FlickrImageClient(BaseImageClient):
    source = 'FlickrImageClient'
    CANDIDATE_API_KEYS = [
        '0f15ff623f1198a1f7f52550f8c36057', 'a6365f14201cd3c5f34678e671b9ab8d', 'f7e7fb8cc34e52db3e5af5e1727d0c0b', 'ca4dd89d3dfaeaf075144c3fdec76756',
        '9b4439ce94de7e2ec2c2e6ffadc22bcf', '6c2dba48efdbccaced44ea0b445fecbf', '57bded31ef9c635326e4acfa2c62b7dc', '929033444e3a0d9a3859195d56d36552',
    ]
    def __init__(self, **kwargs):
        super(FlickrImageClient, self).__init__(**kwargs)
        self.default_search_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"}
        self.default_download_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos: list[ImageInfo] = []
        for item in search_result['photos']['photo']:
            if not isinstance(item, dict) or ('url_l' not in item) or not str(item.get('url_l')).startswith('http'): continue
            image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=[item.get('url_l')], identifier=item.get('id') or item.get('url_l')))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, filters, base_url = request_overrides or {}, filters or {}, "https://www.flickr.com/services/rest/?"
        (params := {"method": "flickr.photos.search", "api_key": random.choice(FlickrImageClient.CANDIDATE_API_KEYS), "text": keyword, "format": "json", "nojsoncallback": 1, "extras": "url_l", "per_page": 50, "page": 1, "sort": "relevance", "safe_search": 0}).update(filters)
        search_urls, page_size = [], int(params['per_page'])
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params['page'] = pn + 1
            search_urls.append(base_url + urlencode(params, quote_via=quote))
        return search_urls