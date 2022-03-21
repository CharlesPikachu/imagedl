'''
Function:
    百度图片搜索和下载类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import json
import math
import threading
from urllib.parse import quote
from alive_progress import alive_bar
from .base import BaseImageDownloader


'''百度图片搜索和下载类'''
class BaiduImageDownloader(BaseImageDownloader):
    def __init__(self, auto_set_proxies=True, auto_set_headers=True, **kwargs):
        super(BaiduImageDownloader, self).__init__(auto_set_proxies=auto_set_proxies, auto_set_headers=auto_set_headers, **kwargs)
        self.source_name = 'baidu'
        self.session.headers.update({
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    '''搜索'''
    def search(self, keyword, search_limits=1000, num_threadings=5):
        # 构建所有urls
        base_url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&lm=7&fp=result&ie=utf-8&oe=utf-8&st=-1&word={}&queryWord={}&face=0&pn={}&rn={}'
        search_urls, pagesize = [], 30
        for pn in range(math.ceil(search_limits * 1.2 / pagesize)):
            search_url = base_url.format(quote(keyword), quote(keyword), pn * pagesize, pagesize)
            search_urls.append(search_url)
        # 多线程请求获取所有图片链接
        def searchapi(self, search_urls, image_urls, bar):
            while len(search_urls) > 0:
                search_url = search_urls.pop(0)
                response = self.get(search_url)
                if response is None: 
                    bar()
                    continue
                response.encoding = 'utf-8'
                response_json = json.loads(response.text.replace(r"\'", ""), encoding='utf-8', strict=False)
                for item in response_json['data']:
                    if 'objURL' in item.keys():
                        image_urls.add(self.parseurl(item['objURL']))
                    elif 'replaceUrl' in item.keys() and len(item['replaceUrl']) == 2:
                        image_urls.add(item['replaceUrl'][1]['ObjURL'])
                bar()
        task_pool, image_urls = [], set()
        with alive_bar(min(len(search_urls), search_limits)) as bar:
            for idx in range(num_threadings):
                task = threading.Thread(
                    target=searchapi,
                    args=(self, search_urls, image_urls, bar)
                )
                task_pool.append(task)
                task.start()
            for task in task_pool: task.join()
        # 返回结果
        return list(image_urls)[:search_limits]
    '''解码url'''
    def parseurl(self, url):
        in_table, out_table = '0123456789abcdefghijklmnopqrstuvw', '7dgjmoru140852vsnkheb963wtqplifca'
        translate_table = str.maketrans(in_table, out_table)
        mapping = {'_z2C$q': ':', '_z&e3B': '.', 'AzdH3F': '/'}
        for k, v in mapping.items():
            url = url.replace(k, v)
        return url.translate(translate_table)