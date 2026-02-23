'''
Function:
    Implementation of EverypixelImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import math
import json_repair
from .base import BaseImageClient
from ..utils import cookies2string
from urllib.parse import quote, urlencode


'''EverypixelImageClient'''
class EverypixelImageClient(BaseImageClient):
    source = 'EverypixelImageClient'
    def __init__(self, **kwargs):
        super(EverypixelImageClient, self).__init__(**kwargs)
        self.default_search_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "accept-encoding": "gzip, deflate, br, zstd", "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7", "cache-control": "max-age=0", "priority": "u=0, i", "sec-ch-ua": '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"', "sec-ch-ua-arch": '"x86"', "sec-ch-ua-bitness": '"64"', "sec-ch-ua-full-version": '"145.0.7632.76"', "sec-ch-ua-full-version-list": '"Not:A-Brand";v="99.0.0.0", "Google Chrome";v="145.0.7632.76", "Chromium";v="145.0.7632.76"',
            "cookie": "_ga=GA1.1.859071961.1770791608; cookie_popup_shown=1; _ga_7VBKBQ1JV6=GS2.1.s1770792674$o1$g1$t1770794235$j60$l0$h0; cf_clearance=ycaLwAl0aHa9W_GxSkDaGK6ZK7BqgBWf.zyU_kncpAo-1771821234-1.2.1.1-w1xY1nDyWVpgBVtala9.P4FHFZR9xbYsAxa9.d4Xl.qlUiLTrOLr.l8DHt0iwoKs7mYTEiszd7V3YRaGZCeN7k6VKUMozD2YgWE2ueVqkyS6my_lhYkznuoNAcCwuS.UxkBzmwd08nnjjROAZZIzsyN0yMAhUC_SRNvmCsRn5fKkQ0vKiiuKOoDtNVceRKEuGk1IcO3aNsjnaYCpnhrSOoRjJoC4MxLkoRPJYbBEn8k; client_id=10c7890a715394b89e253ea989163e0e; session_id=f0a13985-bb58-431e-b0ad-6b5cf020396d; userStatus=0; _ga_FLYERKMCP5=GS2.1.s1771821236$o2$g1$t1771821245$j51$l0$h0",
            "sec-ch-ua-mobile": "?0", "sec-ch-ua-model": '""', "sec-ch-ua-platform": '"Windows"', "sec-ch-ua-platform-version": '"10.0.0"', "sec-fetch-dest": "document", "sec-fetch-mode": "navigate", "sec-fetch-site": "none", "sec-fetch-user": "?1", "upgrade-insecure-requests": "1", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
        }
        if self.default_cookies: self.default_search_headers['cookie'] = cookies2string(self.default_cookies)
        self.default_download_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
        }
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str):
        # parse json text in safety
        loaded_search_result: dict = json_repair.loads(search_result)['images']; search_result: list = []
        if not loaded_search_result: return []
        for v in list(loaded_search_result.values()): search_result.extend(v if isinstance(v, list) else [])
        # parse search result
        image_infos = []
        for item in search_result:
            if not isinstance(item, dict) or ('url' not in item) or (not str(item.get('url')).startswith('http')): continue
            image_info = {
                'candidate_urls': [item.get('url')], 'raw_data': item, 'identifier': item.get('basic_img_id') or item.get('id') or item.get('url'),
            }
            image_infos.append(image_info)
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides = request_overrides or {}
        base_url = 'https://www.everypixel.com/search/search?'
        params = {'q': keyword, 'is_id': 64, 'limit': 50, 'json': '1', 'page': 1}
        if filters is not None: params.update(filters)
        search_urls, page_size = [], int(params['limit'])
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params['page'] = pn + 1
            search_url = base_url + urlencode(params, quote_via=quote)
            search_urls.append(search_url)
        return search_urls