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
import imghdr
import pickle
import shutil
import requests
import threading
import json_repair
from datetime import datetime
from freeproxy import freeproxy
from fake_useragent import UserAgent
from alive_progress import alive_bar
from pathvalidate import sanitize_filepath
from ..utils import touchdir, LoggerHandle, Filter


'''BaseImageClient'''
class BaseImageClient():
    source = 'BaseImageClient'
    def __init__(self, auto_set_proxies: bool = True, maintain_headers: bool = False, random_update_ua: bool = False, max_retries: int = 5, maintain_session: bool = False, 
                 logger_handle: LoggerHandle = None, disable_print: bool = False, work_dir: str = 'imagedl_outputs', proxy_sources: list = None):
        # set up work dir
        touchdir(work_dir)
        # set attributes
        self.work_dir = work_dir
        self.max_retries = max_retries
        self.disable_print = disable_print
        self.logger_handle = logger_handle if logger_handle else LoggerHandle()
        self.random_update_ua = random_update_ua
        self.maintain_session = maintain_session
        self.auto_set_proxies = auto_set_proxies
        self.maintain_headers = maintain_headers
        # init requests.Session
        self.session = requests.Session()
        self.default_headers = {'User-Agent': UserAgent().random}
        self.session.headers.update(self.default_headers)
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
    '''_removeduplicates'''
    def _removeduplicates(self, image_infos: list = None):
        unique_image_infos, identifiers = [], set()
        for image_info in image_infos:
            if image_info['identifier'] in identifiers:
                continue
            identifiers.add(image_info['identifier'])
            unique_image_infos.append(image_info)
        return unique_image_infos
    '''_appenduniquefilepathforimages'''
    def _appenduniquefilepathforimages(self, keyword: str, image_infos: list):
        time_stamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        work_dir = os.path.join(self.work_dir, self.source, f'{time_stamp} {keyword.replace(" ", "")}')
        touchdir(work_dir)
        for idx, image_info in enumerate(image_infos):
            image_info['work_dir'] = work_dir
            image_info['file_path'] = os.path.join(work_dir, f'{str(idx+1).zfill(8)}')
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
            except Exception as err:
                self.logger_handle.error(err, disable_print=self.disable_print)
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
        image_infos = self._removeduplicates(image_infos)
        self._appenduniquefilepathforimages(image_infos=image_infos, keyword=keyword)
        if len(image_infos) > 0:
            work_dir = image_infos[0]['work_dir']
            self._savetopkl(image_infos, os.path.join(work_dir, 'search_results.pkl'))
        else:
            work_dir = self.work_dir
        self.logger_handle.info(f'Finished searching images using {self.source}. Search results have been saved to {work_dir}, valid items: {len(image_infos)}.')
        # return
        return image_infos
    '''_getfilter'''
    def _getfilter(self):
        search_filter = Filter()
        return search_filter
    '''_download'''
    def _download(self, image_infos: list, bar: alive_bar, request_overrides: dict = {}, downloaded_image_infos: list = None):
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
                downloaded_image_info = copy.deepcopy(image_info)
                downloaded_image_info['file_path'] = file_path_with_ext
                downloaded_image_infos.append(downloaded_image_info)
            else:
                os.remove(file_path)
            bar()
    '''download'''
    def download(self, image_infos, num_threadings=5, request_overrides: dict = {}):
        # logging
        self.logger_handle.info(f'Start to download images using {self.source}.')
        # multi threadings for downloading images
        task_pool, downloaded_image_infos = [], []
        with alive_bar(len(image_infos)) as bar:
            for _ in range(num_threadings):
                task = threading.Thread(target=self._download, args=(image_infos, bar, request_overrides, downloaded_image_infos))
                task_pool.append(task)
                task.start()
            for task in task_pool: task.join()
        # logging
        if len(downloaded_image_infos) > 0:
            work_dir = downloaded_image_infos[0]['work_dir']
            self._savetopkl(downloaded_image_infos, os.path.join(work_dir, 'download_results.pkl'))
        else:
            work_dir = self.work_dir
        self.logger_handle.info(f'Finished downloading images using {self.source}. Download results have been saved to {work_dir}, valid downloads: {len(downloaded_image_infos)}.')
    '''get'''
    def get(self, url, **kwargs):
        resp = None
        for _ in range(self.max_retries):
            headers = self.session.headers
            if not self.maintain_session:
                self.session = requests.Session()
                if self.maintain_headers:
                    self.session.headers = headers
                else:
                    self.session.headers = self.default_headers
                    if self.random_update_ua: self.session.headers.update({'User-Agent': UserAgent().random})
            if self.auto_set_proxies:
                try:
                    self.session.proxies = self.proxied_session_client.getrandomproxy()
                except Exception as err:
                    self.logger_handle.error(err, disable_print=self.disable_print)
                    self.session.proxies = {}
            else:
                self.session.proxies = {}
            try:
                resp = self.session.get(url, **kwargs)
            except Exception as err:
                self.logger_handle.error(err, disable_print=self.disable_print)
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
            if self.maintain_headers:
                self.session.headers = headers
            else:
                self.session.headers = self.default_headers
                if self.random_update_ua: self.session.headers.update({'User-Agent': UserAgent().random})
            if self.auto_set_proxies:
                try:
                    self.session.proxies = self.proxied_session_client.getrandomproxy()
                except Exception as err:
                    self.logger_handle.error(err, disable_print=self.disable_print)
                    self.session.proxies = {}
            else:
                self.session.proxies = {}
            try:
                resp = self.session.post(url, **kwargs)
            except Exception as err:
                self.logger_handle.error(err, disable_print=self.disable_print)
                continue
            if resp.status_code != 200: continue
            return resp
        return resp
    '''_savetopkl'''
    def _savetopkl(self, data, file_path, auto_sanitize=True):
        if auto_sanitize: file_path = sanitize_filepath(file_path)
        with open(file_path, 'wb') as fp:
            pickle.dump(data, fp)