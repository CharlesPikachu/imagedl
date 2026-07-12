'''
Function:
    Implementation of BlueskyImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import json_repair
from ..utils import ImageInfo
from .base import BaseImageClient
from urllib.parse import quote, urlencode


'''BlueskyImageClient'''
class BlueskyImageClient(BaseImageClient):
    source = 'BlueskyImageClient'
    def __init__(self, **kwargs):
        super(BlueskyImageClient, self).__init__(**kwargs)
        self.default_search_headers = {'Accept': 'application/json, text/plain, */*', 'Referer': 'https://bsky.app/', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',}
        self.default_download_headers = {'Referer': 'https://bsky.app/', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',}
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_extractimagegroups'''
    def _extractimagegroups(self, node) -> list[list[str]]:
        image_groups = []
        if isinstance(node, list): image_groups.extend(group for item in node for group in self._extractimagegroups(item)); return image_groups
        if not isinstance(node, dict): return image_groups
        candidate_download_urls = [str(url) for url in [node.get('fullsize'), node.get('thumb')] if url and str(url).startswith('http')]
        if (candidate_download_urls := list(dict.fromkeys(candidate_download_urls))): image_groups.append(candidate_download_urls); return image_groups
        image_groups.extend(group for key in ('images', 'media') if key in node for group in self._extractimagegroups(node.get(key)))
        return image_groups
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # parse search result
        image_infos: list[ImageInfo] = []
        for post in search_result.get('posts', []) or []:
            if not isinstance(post, dict): continue
            image_groups = self._extractimagegroups(post.get('embed', {}) or {})
            post_identifier = post.get('uri') or post.get('cid') or ''
            for image_idx, candidate_download_urls in enumerate(image_groups):
                identifier = post_identifier or candidate_download_urls[0]
                image_infos.append(ImageInfo(source=self.source, raw_data=post, candidate_download_urls=candidate_download_urls, identifier=f'{identifier}#{image_idx}',))
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None) -> list[str]:
        filters, request_overrides, base_url = dict(filters or {}), request_overrides or {}, 'https://api.bsky.app/xrpc/app.bsky.feed.searchPosts?'
        page_size = min(max(int(filters.pop('limit', min(max(int(search_limits * 1.2), 1), 100)) or 1), 1), 100)
        (params := {'q': keyword, 'limit': page_size, 'sort': 'latest',}).update(filters); params['limit'] = page_size
        return [base_url + urlencode(params, quote_via=quote, doseq=True)]