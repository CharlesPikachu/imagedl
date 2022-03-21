'''
Function:
    谷歌图片搜索和下载类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
import math
import threading
from bs4 import BeautifulSoup
from alive_progress import alive_bar
from .base import BaseImageDownloader
from six.moves.urllib.parse import urlencode


'''谷歌图片搜索和下载类'''
class GoogleImageDownloader(BaseImageDownloader):
    def __init__(self, auto_set_proxies=False, auto_set_headers=False, **kwargs):
        super(GoogleImageDownloader, self).__init__(auto_set_proxies=False, auto_set_headers=False, **kwargs)
        self.source_name = 'google'
    '''搜索'''
    def search(self, keyword, search_limits=1000, num_threadings=5):
        # 构建所有urls
        base_url = 'https://www.google.com/search?'
        search_urls, pagesize = [], 20
        for pn in range(math.ceil(search_limits * 1.2 / pagesize)):
            params = {
                'q': keyword,
                'ijn': pn,
                'start': pn * pagesize,
                'tbs': '',
                'tbm': 'isch',
            }
            search_urls.append(base_url + urlencode(params))
        # 多线程请求获取所有图片链接
        def searchapi(self, search_urls, image_urls, bar):
            while len(search_urls) > 0:
                search_url = search_urls.pop(0)
                response = self.get(search_url)
                if response is None: 
                    bar()
                    continue
                soup = BeautifulSoup(response.text)
                for div in soup.find_all(name='script'):
                    txt = str(div)
                    if 'AF_initDataCallback' not in txt: continue
                    if 'ds:0' in txt or 'ds:1' not in txt: continue
                    for image_url in re.findall(r'http[^\[]*?\.(?:jpg|png|bmp|gif)', txt): image_urls.add(image_url)
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