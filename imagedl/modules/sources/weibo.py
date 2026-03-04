'''
Function:
    Implementation of WeiboImageClient
Author:
    CharlesPikachu
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import math
import json_repair
from urllib.parse import quote
from .base import BaseImageClient


'''WeiboImageClient'''
class WeiboImageClient(BaseImageClient):
    source = 'WeiboImageClient'
    SINAIMG_RE = re.compile(r'(https?://wx\d\.sinaimg\.cn/)' r'(?:thumbnail|thumb150|thumb180|small|square|bmiddle|mw\d+|orj\d+)' r'(/)')
    def __init__(self, **kwargs):
        super(WeiboImageClient, self).__init__(**kwargs)
        self.default_search_headers = {
            'Cookie': 'SUB=_2AkMeQriDf8NxqwFRmv0Rz2LgbI9-zA_EieKoHklYJRM3HRl-yT9yqmE5tRB6NcKWbCbMDwPRXM1ooQJ1pNNWP8ZEg0Ev; WEIBOCN_FROM=1110006030; MLOGIN=0; _T_WM=91941672904; XSRF-TOKEN=72dc30; mweibo_short_token=664a2add81; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D100103type%253D1%2526q%253D%25E7%258C%25AB%25E5%2592%25AA%26fid%3D100103type%253D1%2526q%253D%25E7%258C%25AB%25E5%2592%25AA%26uicode%3D10000011',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1', 'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8', 'Referer': 'https://m.weibo.cn/', 'X-Requested-With': 'XMLHttpRequest',
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36', 'Referer': 'https://weibo.com/',
        }
        self.default_headers = self.default_search_headers
        self._initsession()
    '''_upgradeimageurl'''
    def _upgradeimageurl(self, url: str):
        if not url: return url
        return self.SINAIMG_RE.sub(r'\1large\2', url)
    '''_extractpicsfromblog'''
    def _extractpicsfromblog(self, mblog: dict):
        image_infos = []
        if not isinstance(mblog, dict): return image_infos
        # strategy 1: pics array (most common in mobile API)
        pics = mblog.get('pics') or []
        for pic in pics:
            if not isinstance(pic, dict): continue
            large, candidate_urls = pic.get('large'), []
            if isinstance(large, dict) and str(large.get('url', '')).strip(): candidate_urls.append(str(large['url']).strip())
            (pic_url := str(pic.get('url', '')).strip()) and candidate_urls.extend([u for u in (self._upgradeimageurl(pic_url), pic_url) if u not in candidate_urls])
            if not candidate_urls: continue
            image_infos.append({'candidate_urls': candidate_urls, 'raw_data': pic, 'identifier': candidate_urls[0]})
        # strategy 2: fallback to single pic fields (when pics array is absent)
        if not image_infos:
            for key in ('original_pic', 'bmiddle_pic', 'thumbnail_pic'):
                pic_url = str(mblog.get(key, '')).strip()
                if pic_url: upgraded = self._upgradeimageurl(pic_url); candidate_urls = ([upgraded, pic_url] if upgraded != pic_url else [pic_url]); image_infos.append({'candidate_urls': candidate_urls, 'raw_data': mblog, 'identifier': candidate_urls[0]}); break
        # return
        return image_infos
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str):
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # validate response
        if not isinstance(search_result, dict) or search_result.get('ok') != 1: return []
        data = search_result.get('data', {})
        if not isinstance(data, dict): return []
        cards = data.get('cards', [])
        if not isinstance(cards, list): return []
        # extract image infos from cards
        image_infos = []
        for card in cards:
            if not isinstance(card, dict): continue
            card_type = card.get('card_type')
            card_type == 9 and isinstance((mblog := card.get('mblog')), dict) and image_infos.extend(self._extractpicsfromblog(mblog))
            card_type == 11 and isinstance((card_group := card.get('card_group', [])), list) and image_infos.extend([img for sub_card in card_group if isinstance(sub_card, dict) and sub_card.get('card_type') == 9 and isinstance((sub_mblog := sub_card.get('mblog')), dict) for img in self._extractpicsfromblog(sub_mblog)])
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        request_overrides, base_url = request_overrides or {}, 'https://m.weibo.cn/api/container/getIndex'
        search_type = str(filters.pop('search_type')) if (filters is not None and 'search_type' in filters) else '1'
        containerid = f"100103type%3D{search_type}%26q%3D{quote(keyword, safe='')}"
        search_urls, page_size = [], 20
        num_pages = math.ceil(search_limits * 1.2 / page_size)
        for pn in range(1, num_pages + 1):
            if pn == 1: search_url = f'{base_url}?containerid={containerid}&page_type=searchall'
            else: search_url = f'{base_url}?containerid={containerid}&page_type=searchall&page={pn}'
            search_urls.append(search_url)
        return search_urls