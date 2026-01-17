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
import pickle
import shutil
import imghdr
import requests
import threading
import json_repair
from datetime import datetime
from fake_useragent import UserAgent
from alive_progress import alive_bar
from pathvalidate import sanitize_filepath
from ..utils import usedownloadheaderscookies, usesearchheaderscookies, touchdir, LoggerHandle, Filter


'''BaseImageClient'''
class BaseImageClient():
    source = 'BaseImageClient'
    def __init__(self, auto_set_proxies: bool = False, random_update_ua: bool = False, max_retries: int = 5, maintain_session: bool = False, 
                 logger_handle: LoggerHandle = None, disable_print: bool = False, work_dir: str = 'imagedl_outputs', freeproxy_settings: dict = None):
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
        self.freeproxy_settings = freeproxy_settings or {}
        # init requests.Session
        self.default_search_headers = {'User-Agent': UserAgent().chrome}
        self.default_download_headers = {'User-Agent': UserAgent().chrome}
        self.default_headers = self.default_search_headers
        self._initsession()
        # proxied_session_client
        self.proxied_session_client = None
        if auto_set_proxies:
            from freeproxy import freeproxy
            default_freeproxy_settings = dict(disable_print=True, proxy_sources=['ProxiflyProxiedSession'], max_tries=20, init_proxied_session_cfg={})
            default_freeproxy_settings.update(self.freeproxy_settings)
            self.proxied_session_client = freeproxy.ProxiedSessionClient(**default_freeproxy_settings)
    '''_initsession'''
    def _initsession(self):
        self.session = requests.Session()
        self.session.headers = self.default_headers
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword, search_limits=1000, filters: dict = None, request_overrides: dict = None):
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
        work_dir = sanitize_filepath(os.path.join(self.work_dir, self.source, f'{time_stamp} {keyword.replace(" ", "")}'))
        touchdir(work_dir)
        for idx, image_info in enumerate(image_infos):
            image_info['work_dir'] = work_dir
            image_info['file_path'] = os.path.join(work_dir, f'{str(idx+1).zfill(8)}')
        return image_infos
    '''_search'''
    @usesearchheaderscookies
    def _search(self, search_urls: list, bar: alive_bar, image_infos: list, request_overrides: dict = None):
        request_overrides = request_overrides or {}
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
                self.logger_handle.error(f'{self.source}._search >>> {search_url} (Error: {err})', disable_print=self.disable_print)
                search_result = []
            if isinstance(search_result, dict):
                image_infos.append(search_result)
            else:
                assert isinstance(search_result, list)
                image_infos.extend(search_result)
            bar()
        return image_infos
    '''search'''
    @usesearchheaderscookies
    def search(self, keyword: str, search_limits: int = 1000, num_threadings: int = 5, filters: dict = None, request_overrides: dict = None):
        # init
        request_overrides = request_overrides or {}
        # logging
        self.logger_handle.info(f'Start to search images using {self.source}.', disable_print=self.disable_print)
        # construct search urls
        search_urls = self._constructsearchurls(keyword=keyword, search_limits=search_limits, filters=filters, request_overrides=request_overrides)
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
            touchdir(work_dir)
            self._savetopkl(image_infos, os.path.join(work_dir, 'search_results.pkl'))
        else:
            work_dir = self.work_dir
        self.logger_handle.info(f'Finished searching images using {self.source}. Search results have been saved to {work_dir}, valid items: {len(image_infos)}.', disable_print=self.disable_print)
        # return
        return image_infos
    '''_getfilter'''
    def _getfilter(self):
        search_filter = Filter()
        return search_filter
    '''_download'''
    @usedownloadheaderscookies
    def _download(self, image_infos: list, bar: alive_bar, request_overrides: dict = None, downloaded_image_infos: list = None):
        request_overrides = request_overrides or {}
        checked_work_dirs = set()
        for image_info in image_infos:
            if image_info['work_dir'] not in checked_work_dirs:
                touchdir(image_info['work_dir'])
                checked_work_dirs.add(image_info['work_dir'])
        while len(image_infos) > 0:
            image_info = image_infos.pop(0)
            file_path, image_candidate_urls = image_info['file_path'], image_info['candidate_urls']
            for image_candidate_url in image_candidate_urls:
                resp = self.get(image_candidate_url, **request_overrides)
                if resp is not None and resp.status_code == 200: break
            if resp is None or resp.status_code != 200: bar(); continue
            assert (not os.path.exists(file_path))
            with open(file_path, 'wb') as fp: fp.write(resp.content)
            ext = imghdr.what(file_path)
            if ext in ["rgb", "gif", "pbm", "pgm", "ppm", "tiff", "rast", "xbm", "jpeg", "jpg", "bmp", "png", "webp", "exr"]:
                file_path_with_ext = f'{file_path}.{ext}'
                assert (not os.path.exists(file_path_with_ext))
                shutil.move(file_path, file_path_with_ext)
                downloaded_image_info = copy.deepcopy(image_info)
                downloaded_image_info['file_path'] = file_path_with_ext
                downloaded_image_infos.append(downloaded_image_info)
            else:
                os.remove(file_path)
            bar()
        return downloaded_image_infos
    '''download'''
    @usedownloadheaderscookies
    def download(self, image_infos: list, num_threadings: int = 5, request_overrides: dict = None):
        # init
        request_overrides = request_overrides or {}
        # logging
        self.logger_handle.info(f'Start to download images using {self.source}.', disable_print=self.disable_print)
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
            touchdir(work_dir)
            self._savetopkl(downloaded_image_infos, os.path.join(work_dir, 'download_results.pkl'))
        else:
            work_dir = self.work_dir
        self.logger_handle.info(f'Finished downloading images using {self.source}. Download results have been saved to {work_dir}, valid downloads: {len(downloaded_image_infos)}.', disable_print=self.disable_print)
        # return
        return downloaded_image_infos
    '''get'''
    def get(self, url, **kwargs):
        resp = None
        for _ in range(self.max_retries):
            if not self.maintain_session:
                self._initsession()
                if self.random_update_ua: self.session.headers.update({'User-Agent': UserAgent().random})
            if self.auto_set_proxies:
                try:
                    self.session.proxies = self.proxied_session_client.getrandomproxy()
                except Exception as err:
                    self.logger_handle.error(f'{self.source}.get >>> {url} (Error: {err})', disable_print=self.disable_print)
                    self.session.proxies = {}
            else:
                self.session.proxies = {}
            proxies = kwargs.pop('proxies', None) or self.session.proxies
            try:
                resp = self.session.get(url, proxies=proxies, **kwargs)
                resp.raise_for_status()
            except Exception as err:
                self.logger_handle.error(f'{self.source}.get >>> {url} (Error: {err})', disable_print=self.disable_print)
                continue
            return resp
        return resp
    '''post'''
    def post(self, url, **kwargs):
        resp = None
        for _ in range(self.max_retries):
            if not self.maintain_session:
                self._initsession()
                if self.random_update_ua: self.session.headers.update({'User-Agent': UserAgent().random})
            if self.auto_set_proxies:
                try:
                    self.session.proxies = self.proxied_session_client.getrandomproxy()
                except Exception as err:
                    self.logger_handle.error(f'{self.source}.post >>> {url} (Error: {err})', disable_print=self.disable_print)
                    self.session.proxies = {}
            else:
                self.session.proxies = {}
            proxies = kwargs.pop('proxies', None) or self.session.proxies
            try:
                resp = self.session.post(url, proxies=proxies, **kwargs)
                resp.raise_for_status()
            except Exception as err:
                self.logger_handle.error(f'{self.source}.post >>> {url} (Error: {err})', disable_print=self.disable_print)
                continue
            return resp
        return resp
    '''_savetopkl'''
    def _savetopkl(self, data, file_path, auto_sanitize=True):
        if auto_sanitize: file_path = sanitize_filepath(file_path)
        with open(file_path, 'wb') as fp: pickle.dump(data, fp)