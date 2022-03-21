'''
Function:
    图片搜索和下载基类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import time
import imghdr
import shutil
import requests
import threading
from tqdm import tqdm
from freeproxy import freeproxy
from ..utils import randomua, touchdir


'''图片搜索和下载基类'''
class BaseImageDownloader():
    def __init__(self, auto_set_proxies=True, auto_set_headers=True, **kwargs):
        self.session = requests.Session()
        self.auto_set_proxies = auto_set_proxies
        self.auto_set_headers = auto_set_headers
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
        }
        self.session.headers.update(self.headers)
        if auto_set_proxies:
            self.proxy_client = freeproxy.FreeProxy(logfilepath=None)
    '''搜索'''
    def search(self, keyword):
        raise NotImplementedError('not to be implemented')
    '''下载'''
    def download(self, keyword, search_limits=1000, num_threadings=5, savedir='outputs'):
        touchdir(savedir)
        # 获得image_urls
        self.logging(f'Start to search images from {self.source_name}')
        image_urls = self.search(keyword, search_limits, num_threadings)
        # 多线程下载图片
        self.logging(f'Start to download images from {self.source_name}')
        def downloadapi(self, savepaths, image_urls):
            assert len(savepaths) == len(image_urls)
            for savepath, image_url in tqdm(zip(savepaths, image_urls)):
                response = self.get(image_url)
                with open(savepath, 'wb') as fp: fp.write(response.content)
                filetype = imghdr.what(savepath)
                if filetype in ['jpg', 'jpeg', 'png', 'bmp']:
                    savepath_correct = f'{savepath}.{filetype}'
                    shutil.move(savepath, savepath_correct)
                else:
                    os.remove(savepath)
        task_pool, savepaths, num_downloads_per_threading = [], [], round(len(image_urls) / num_threadings)
        for idx in range(len(image_urls)):
            savename = f'image_{str(idx).zfill(8)}'
            savepaths.append(os.path.join(savedir, savename))
        for idx in range(num_threadings):
            start, end = idx * num_downloads_per_threading, (idx + 1) * num_downloads_per_threading
            task = threading.Thread(
                target=downloadapi,
                args=(self, savepaths[start: end], image_urls[start: end])
            )
            task_pool.append(task)
            task.start()
        for task in task_pool: task.join()
    '''get请求'''
    def get(self, url, **kwargs):
        if self.auto_set_headers: self.session.headers.update({'user-agent': randomua()})
        while True:
            response = self.session.get(url, **kwargs)
            if response.status_code != 200:
                if self.auto_set_proxies:
                    headers = self.session.headers.copy()
                    self.session = requests.Session()
                    self.session.proxies.update(self.proxy_client.getrandomproxy())
                    self.session.headers.update(headers)
                    continue
                else:
                    return None
            return response
    '''post请求'''
    def post(self, url, **kwargs):
        if self.auto_set_headers: self.session.headers.update({'user-agent': randomua()})
        while True:
            response = self.session.post(url, **kwargs)
            if response.status_code != 200:
                if self.auto_set_proxies:
                    headers = self.session.headers.copy()
                    self.session = requests.Session()
                    self.session.proxies.update(self.proxy_client.getrandomproxy())
                    self.session.headers.update(headers)
                    continue
                else:
                    return None
            return response
    '''logging'''
    def logging(self, msg, tip='INFO'):
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} {tip}]: {msg}')