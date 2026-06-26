'''
Function:
    Implementation of OpenLibraryImageClient
Author:
    Zhenchao Jin
WeChat Official Account:
    Charles的皮卡丘
'''
import math
import json_repair
from ..utils import ImageInfo
from .base import BaseImageClient
from urllib.parse import quote, urlencode


'''OpenLibraryImageClient'''
class OpenLibraryImageClient(BaseImageClient):
    source = 'OpenLibraryImageClient'
    def __init__(self, **kwargs):
        super(OpenLibraryImageClient, self).__init__(**kwargs)
        self.default_search_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36", "accept": "application/json", "referer": "https://openlibrary.org/"}
        self.default_download_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36", "referer": "https://openlibrary.org/"}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        # init
        cover_urls_func = lambda kind, value: [] if (not value or not (value := str(value).strip())) else [f'https://covers.openlibrary.org/b/{kind}/{value}-L.jpg?default=false', f'https://covers.openlibrary.org/b/{kind}/{value}-M.jpg?default=false']
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos: list[ImageInfo] = []
        for item in search_result.get('docs', []):
            if not isinstance(item, dict): continue
            candidate_urls = []; candidate_urls.extend(cover_urls_func('id', item.get('cover_i')))
            candidate_urls.extend(cover_urls_func('olid', item.get('cover_edition_key')))
            for isbn in item.get('isbn', [])[:3]: candidate_urls.extend(cover_urls_func('isbn', isbn))
            if not (candidate_urls := list(dict.fromkeys(candidate_urls))): continue
            identifier = item.get('key') or item.get('cover_edition_key') or item.get('cover_i') or candidate_urls[0]
            image_infos.append(ImageInfo(source=self.source, raw_data=item, candidate_download_urls=candidate_urls, identifier=identifier))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, filters, base_url = request_overrides or {}, filters or {}, 'https://openlibrary.org/search.json?'
        page_size = int(filters.pop('limit', 100) or 100); page_size = min(max(page_size, 1), 100); search_urls = []
        (params := {'q': keyword, 'limit': page_size, 'offset': 0, 'fields': 'key,title,author_name,first_publish_year,cover_i,cover_edition_key,isbn,edition_key'}).update(filters)
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params['offset'] = pn * page_size
            search_urls.append(base_url + urlencode(params, quote_via=quote))
        return search_urls