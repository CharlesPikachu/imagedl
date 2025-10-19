'''
Function:
    Implementation of BaiduImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import math
import json_repair
from urllib.parse import quote
from .base import BaseImageClient
from ..utils import lowerdictkeys


'''BaiduImageClient'''
class BaiduImageClient(BaseImageClient):
    source = 'BaiduImageClient'
    def __init__(self, **kwargs):
        super(BaiduImageClient, self).__init__(**kwargs)
        self.headers = {
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.session.headers.update(self.headers)
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str):
        # parse json text in safety
        search_result: dict = json_repair.loads(search_result)
        # pick best image url
        def pickbesturl(item: dict):
            # --all lower letters for keys with str type
            item = lowerdictkeys(item)
            # --parse try1
            if ('objurl' in item) and isinstance(item['objurl'], str) and item['objurl'].strip():
                return self._parseurl(item['objurl'].strip())
            # --parse try2
            for r in item.get("replaceurl", []):
                r = lowerdictkeys(r)
                if ('objurl' in r) and isinstance(r['objurl'], str) and r['objurl'].strip():
                    return r['objurl'].strip()
            # --parse try3
            if ('middleurl' in item) and isinstance(item['middleurl'], str) and item['middleurl'].strip():
                return item['middleurl'].strip()
            # --parse try4
            if ('thumburl' in item) and isinstance(item['thumburl'], str) and item['thumburl'].strip():
                return item['thumburl'].strip()
            # --failure
            return None
        # parse search result
        image_infos = []
        for item in search_result.get('data', []):
            if not isinstance(item, dict): continue
            url = pickbesturl(item=item)
            if not url: continue
            image_info = {
                'url': url, 'raw_data': item
            }
            image_infos.append(image_info)
        # return
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword, search_limits=1000):
        base_url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&lm=7&fp=result&ie=utf-8&oe=utf-8&st=-1&word={}&queryWord={}&face=0&pn={}&rn={}'
        search_urls, page_size = [], 30
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            search_url = base_url.format(quote(keyword), quote(keyword), pn * page_size, page_size)
            search_urls.append(search_url)
        return search_urls
    '''_parseurl'''
    def _parseurl(self, url: str):
        in_table, out_table = '0123456789abcdefghijklmnopqrstuvw', '7dgjmoru140852vsnkheb963wtqplifca'
        translate_table = str.maketrans(in_table, out_table)
        mapping = {'_z2C$q': ':', '_z&e3B': '.', 'AzdH3F': '/'}
        for k, v in mapping.items():
            url = url.replace(k, v)
        return url.translate(translate_table)


'''tests'''
if __name__ == '__main__':
    BaiduImageClient().search('美女')