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
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
            "cookie": "client_id=e30f48e30aba6693e1302ac195e2e452; session_id=6ce6d099-06a7-404d-a63c-eb3a31e0acb9; userStatus=0; _ga=GA1.1.859071961.1770791608; cookie_popup_shown=1; cf_clearance=YOLS0wwbZdTaAcyw1gud7W5Dai11jM4zZ.lIiT_UWj8-1770793518-1.2.1.1-52tzVj3lyOFBKOfv2JmOb1.kFqmCwNcdcl0fqRFa0WfoTz4_eUeroPmwt03VgnzGhzsLNphRsl9H5LQ12GaJa61dSJFm6AVpPg3TBNnp60RoUOYYq0t6Ky9eIjLA5QekZ6pIh.ggJhnoSaYvKAz9Aos_V7P2CEVI7.ojxb6WQT0maP8FpY.47uq1mczV6lq.VHQ2N3T4AF8.vsh4p6X9S0YKnNdfzXj5L42zw.xWrBI; _ga_FLYERKMCP5=GS2.1.s1770791608$o1$g1$t1770793888$j56$l0$h0; _ga_7VBKBQ1JV6=GS2.1.s1770792674$o1$g1$t1770794235$j60$l0$h0",
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