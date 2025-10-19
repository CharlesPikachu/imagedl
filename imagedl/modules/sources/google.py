'''
Function:
    Implementation of GoogleImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import math
from bs4 import BeautifulSoup
from .base import BaseImageClient
from six.moves.urllib.parse import urlencode


'''GoogleImageClient'''
class GoogleImageClient(BaseImageClient):
    source = 'GoogleImageClient'
    def __init__(self, **kwargs):
        if 'auto_set_proxies' not in kwargs: kwargs['auto_set_proxies'] = False
        if 'auto_set_headers' not in kwargs: kwargs['auto_set_headers'] = False
        super(GoogleImageClient, self).__init__(**kwargs)
    '''officialsearchanddownload'''
    def officialsearchanddownload(self, google_image_search_overrides: dict = {}, search_overrides: dict = {}):
        # import official api
        try:
            from google_images_search import GoogleImagesSearch
        except:
            print('You must install the official API before using this function via `pip install google_images_search`')
            return
        # asserts
        assert 'q' in search_overrides, 'please set `q` in `search_overrides` as the search keywords'
        # instance GoogleImagesSearch
        google_image_search_params = {
            'validate_images': True, 'developer_key': 'AIzaSyCGyqf36D5k3QghaZLhAqb1R2OUtRFraF8', 'custom_search_cx': '0d386b282da5209ea',
        }
        google_image_search_params.update(google_image_search_overrides)
        gis = GoogleImagesSearch(**google_image_search_params)
        # search and download
        search_params = {'q': 'girls', 'num': 1000}
        search_params.update(search_overrides)
        gis.search(search_params=search_params, path_to_dir=self.work_dir)
    '''serpapisearch'''
    def serpapisearch(self, search_overrides: dict = {}):
        # import api
        try:
            from serpapi import GoogleSearch
        except:
            print('You must install the official API before using this function via `pip install google google-search-results serpapi`')
            return
        # asserts
        assert 'q' in search_overrides, 'please set `q` in `search_overrides` as the search keywords'
        # search
        search_params = {'q': 'girls', 'google_domain': 'google.com', 'tbm': 'isch', 'api_key': 'cb37586e2a8d129c4142b06c3d46a19aa8bb11187c776a85977298893a5a3266'}
        search_engine = GoogleSearch(search_params)
        search_results = search_engine.get_results()
        # return
        return search_results
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str):
        print(search_result)
        image_infos = []
        soup = BeautifulSoup(search_result)
        for div in soup.find_all(name='script'):
            txt = str(div)
            if 'AF_initDataCallback' not in txt: continue
            if 'ds:0' in txt or 'ds:1' not in txt: continue
            print(div)
            # for image_url in re.findall(r'http[^\[]*?\.(?:jpg|png|bmp|gif)', txt): image_urls.add(image_url)
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword, search_limits=1000):
        base_url = 'https://www.google.com/search?'
        search_urls, page_size = [], 20
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            params = {
                'q': keyword, 'ijn': pn, 'start': pn * page_size, 'tbs': '', 'tbm': 'isch',
            }
            search_urls.append(base_url + urlencode(params))
        return search_urls