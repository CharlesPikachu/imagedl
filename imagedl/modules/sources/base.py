'''
Function:
    Implementation of BaseImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import copy
import time
import imghdr
import pickle
import shutil
import requests
import threading
import json_repair
from freeproxy import freeproxy
from fake_useragent import UserAgent
from alive_progress import alive_bar
from ..utils import touchdir, LoggerHandle


'''BaseImageClient'''
class BaseImageClient():
    source = 'BaseImageClient'
    def __init__(self, auto_set_proxies: bool = True, auto_set_headers: bool = True, max_retries: int = 5, maintain_session: bool = False, 
                 logger_handle: LoggerHandle = None, disable_print: bool = False, work_dir: str = 'imagedl_downloaded_images', proxy_sources: list = None):
        # set up work dir
        touchdir(work_dir)
        # set attributes
        self.work_dir = work_dir
        self.max_retries = max_retries
        self.disable_print = disable_print
        self.logger_handle = logger_handle if logger_handle else LoggerHandle()
        self.maintain_session = maintain_session
        self.auto_set_proxies = auto_set_proxies
        self.auto_set_headers = auto_set_headers
        # init requests.Session
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': UserAgent().random})
        # proxied_session_client
        self.proxied_session_client = freeproxy.ProxiedSessionClient(
            proxy_sources=['KuaidailiProxiedSession', 'IP3366ProxiedSession', 'QiyunipProxiedSession', 'ProxyhubProxiedSession', 'ProxydbProxiedSession'] if proxy_sources is None else proxy_sources, 
            disable_print=True
        ) if auto_set_proxies else None
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword, search_limits=1000, filters: dict = None):
        raise NotImplementedError('not to be implemented')
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str):
        search_result = json_repair.loads(search_result)
        return search_result
    '''_appenduniquefilepathforimages'''
    def _appenduniquefilepathforimages(self, keyword, image_infos: list):
        time_stamp = int(time.time())
        for idx, image_info in enumerate(image_infos):
            image_info['file_path'] = os.path.join(self.work_dir, f'{self.source}_{keyword}_t{time_stamp}_{str(idx).zfill(8)}')
        return image_infos
    '''_search'''
    def _search(self, search_urls: list, bar: alive_bar, image_infos: list, request_overrides: dict = {}):
        while len(search_urls) > 0:
            search_url = search_urls.pop(0)
            resp = self.get(search_url, **request_overrides)
            if resp is None or resp.status_code != 200:
                bar()
                continue
            resp.encoding = 'utf-8'
            try:
                search_result = self._parsesearchresult(resp.text)
            except:
                search_result = []
            if isinstance(search_result, dict):
                image_infos.append(search_result)
            else:
                assert isinstance(search_result, list)
                image_infos.extend(search_result)
            bar()
    '''search'''
    def search(self, keyword, search_limits=1000, num_threadings=5, filters: dict = None, request_overrides: dict = {}):
        # logging
        self.logger_handle.info(f'Start to search images using {self.source}.')
        # construct search urls
        search_urls = self._constructsearchurls(keyword=keyword, search_limits=search_limits, filters=filters)
        # multi threadings for searching images
        task_pool, image_infos = [], []
        with alive_bar(len(search_urls)) as bar:
            for _ in range(num_threadings):
                task = threading.Thread(target=self._search, args=(search_urls, bar, image_infos, request_overrides))
                task_pool.append(task)
                task.start()
            for task in task_pool: task.join()
        # logging
        self._appenduniquefilepathforimages(image_infos=image_infos, keyword=keyword)
        self.savetopkl(image_infos, os.path.join(self.work_dir, f'{self.source}_image_infos_t{int(time.time())}.pkl'))
        self.logger_handle.info(f'Finished searching images using {self.source}. All results have been saved to {self.work_dir}, valid items: {len(image_infos)}.')
        # return
        return image_infos
    '''_download'''
    def _download(self, image_infos: list, bar: alive_bar, request_overrides: dict = {}, processed_image_infos: list = None):
        while len(image_infos) > 0:
            image_info = image_infos.pop(0)
            file_path, image_candidate_urls = image_info['file_path'], image_info['candidate_urls']
            for image_candidate_url in image_candidate_urls:
                resp = self.get(image_candidate_url, **request_overrides)
                if resp is not None and resp.status_code == 200: break
            if resp is None or resp.status_code != 200:
                bar()
                continue
            assert (not os.path.exists(file_path))
            with open(file_path, 'wb') as fp:
                fp.write(resp.content)
            ext = imghdr.what(file_path)
            if ext in ['jpg', 'jpeg', 'png', 'bmp', 'gif']:
                file_path_with_ext = f'{file_path}.{ext}'
                assert (not os.path.exists(file_path_with_ext))
                shutil.move(file_path, file_path_with_ext)
                processed_image_info = copy.deepcopy(image_info)
                processed_image_info['file_path'] = file_path_with_ext
                processed_image_infos.append(processed_image_info)
            else:
                os.remove(file_path)
            bar()
    '''download'''
    def download(self, image_infos, num_threadings=5, request_overrides: dict = {}):
        # logging
        self.logger_handle.info(f'Start to download images using {self.source}.')
        # multi threadings for downloading images
        task_pool, processed_image_infos = [], []
        with alive_bar(len(image_infos)) as bar:
            for _ in range(num_threadings):
                task = threading.Thread(target=self._download, args=(image_infos, bar, request_overrides, processed_image_infos))
                task_pool.append(task)
                task.start()
            for task in task_pool: task.join()
        # logging
        self.savetopkl(processed_image_infos, os.path.join(self.work_dir, f'{self.source}_processed_image_infos_t{int(time.time())}.pkl'))
        self.logger_handle.info(f'Finished downloading images using {self.source}. All results have been saved to {self.work_dir}, successful downloads: {len(processed_image_infos)}.')
    '''get'''
    def get(self, url, **kwargs):
        resp = None
        for _ in range(self.max_retries):
            headers = self.session.headers
            if not self.maintain_session:
                self.session = requests.Session()
            if self.auto_set_headers:
                self.session.headers = headers
                self.session.headers.update({'User-Agent': UserAgent().random})
            if self.auto_set_proxies:
                try:
                    self.session.proxies = self.proxied_session_client.getrandomproxy()
                except:
                    self.session.proxies = {}
            try:
                resp = self.session.get(url, **kwargs)
            except:
                continue
            if resp.status_code != 200: continue
            return resp
        return resp
    '''post'''
    def post(self, url, **kwargs):
        resp = None
        for _ in range(self.max_retries):
            headers = self.session.headers
            if not self.maintain_session:
                self.session = requests.Session()
            if self.auto_set_headers:
                self.session.headers = headers
                self.session.headers.update({'User-Agent': UserAgent().random})
            if self.auto_set_proxies:
                try:
                    self.session.proxies = self.proxied_session_client.getrandomproxy()
                except:
                    self.session.proxies = {}
            try:
                resp = self.session.post(url, **kwargs)
            except:
                continue
            if resp.status_code != 200: continue
            return resp
        return resp
    '''savetopkl'''
    def savetopkl(self, data, file_path):
        with open(file_path, 'wb') as fp:
            pickle.dump(data, fp)