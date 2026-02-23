'''
Function:
    Implementation of BaseImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import copy
import pickle
import shutil
import imghdr
import random
import requests
import threading
import json_repair
from pathlib import Path
from datetime import datetime
from fake_useragent import UserAgent
from alive_progress import alive_bar
from pathvalidate import sanitize_filepath
from ..utils import usedownloadheaderscookies, usesearchheaderscookies, touchdir, cookies2dict, optionalimport, LoggerHandle, Filter


'''BaseImageClient'''
class BaseImageClient():
    source = 'BaseImageClient'
    def __init__(self, auto_set_proxies: bool = False, random_update_ua: bool = False, enable_search_curl_cffi: bool = False, enable_download_curl_cffi: bool = False,
                 max_retries: int = 5, maintain_session: bool = False, logger_handle: LoggerHandle = None, disable_print: bool = False, work_dir: str = 'imagedl_outputs', 
                 freeproxy_settings: dict = None, default_search_cookies: dict = None, default_download_cookies: dict = None):
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
        self.default_search_cookies = cookies2dict(default_search_cookies)
        self.default_download_cookies = cookies2dict(default_download_cookies)
        self.default_cookies = self.default_search_cookies
        self.enable_search_curl_cffi = enable_search_curl_cffi
        self.enable_download_curl_cffi = enable_download_curl_cffi
        self.enable_curl_cffi = self.enable_search_curl_cffi
        self.cc_impersonates = self._listccimpersonates() if (enable_search_curl_cffi or enable_download_curl_cffi) else None
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
    '''_listccimpersonates'''
    def _listccimpersonates(self):
        curl_cffi = optionalimport('curl_cffi')
        root = Path(curl_cffi.__file__).resolve().parent
        exts = {".py", ".so", ".pyd", ".dll", ".dylib"}
        pat = re.compile(rb"\b(?:chrome|edge|safari|firefox|tor)(?:\d+[a-z_]*|_android|_ios)?\b")
        return sorted({m.decode("utf-8", "ignore") for p in root.rglob("*") if p.suffix in exts for m in pat.findall(p.read_bytes())})
    '''_initsession'''
    def _initsession(self):
        curl_cffi = optionalimport('curl_cffi')
        self.session = requests.Session() if not self.enable_curl_cffi else curl_cffi.requests.Session()
        self.session.headers = self.default_headers
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        raise NotImplementedError('not to be implemented')
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str):
        search_result = json_repair.loads(search_result)
        return search_result
    '''_removeduplicates'''
    def _removeduplicates(self, image_infos: list = None):
        unique_image_infos, identifiers = [], set()
        for image_info in image_infos:
            if image_info['identifier'] in identifiers: continue
            identifiers.add(image_info['identifier'])
            unique_image_infos.append(image_info)
        return unique_image_infos
    '''_appenduniquefilepathforimages'''
    def _appenduniquefilepathforimages(self, keyword: str, image_infos: list):
        time_stamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        work_dir = sanitize_filepath(os.path.join(self.work_dir, self.source, f'{time_stamp} {keyword.replace(" ", "")}')); touchdir(work_dir)
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
            search_inputs, search_url, request_method = (search_url['inputs'], search_url['url'], search_url['method']) if isinstance(search_url, dict) else ({}, search_url, 'get')
            try: resp: requests.Response = getattr(self, request_method)(search_url, **search_inputs, **request_overrides); resp.raise_for_status()
            except Exception: bar(); continue
            if (resp is None) or (resp.status_code not in {200}): bar(); continue
            resp.encoding = 'utf-8'
            try: search_result = self._parsesearchresult(resp.text)
            except Exception as err: self.logger_handle.error(f'{self.source}._search >>> {search_url} (Error: {err})', disable_print=self.disable_print); search_result = []
            if isinstance(search_result, dict): image_infos.append(search_result)
            else: assert isinstance(search_result, (list, tuple)); image_infos.extend(list(search_result))
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
                task_pool.append(task); task.start()
            for task in task_pool: task.join()
        # logging
        image_infos = self._removeduplicates(image_infos)
        self._appenduniquefilepathforimages(image_infos=image_infos, keyword=keyword)
        if len(image_infos) > 0:
            work_dir = image_infos[0]['work_dir']; touchdir(work_dir)
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
        request_overrides, checked_work_dirs = request_overrides or {}, set()
        for info in image_infos: (wd := info["work_dir"]) in checked_work_dirs or (touchdir(wd), checked_work_dirs.add(wd))
        while len(image_infos) > 0:
            image_info = image_infos.pop(0); file_path, image_candidate_urls, resp = image_info['file_path'], image_info['candidate_urls'], None
            for image_candidate_url in image_candidate_urls:
                try: (resp := self.get(image_candidate_url, **request_overrides)).raise_for_status(); break
                except Exception: continue
            if (resp is None) or (resp.status_code not in {200}) or os.path.exists(file_path): bar(); continue
            with open(file_path, 'wb') as fp: fp.write(resp.content)
            if (ext := imghdr.what(file_path)) in {"rgb", "gif", "pbm", "pgm", "ppm", "tiff", "rast", "xbm", "jpeg", "jpg", "bmp", "png", "webp", "exr"}:
                shutil.move(file_path, f'{file_path}.{ext}')
                downloaded_image_info = copy.deepcopy(image_info); downloaded_image_info['file_path'] = f'{file_path}.{ext}'; downloaded_image_infos.append(downloaded_image_info)
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
                task_pool.append(task); task.start()
            for task in task_pool: task.join()
        # logging
        if len(downloaded_image_infos) > 0:
            work_dir = downloaded_image_infos[0]['work_dir']; touchdir(work_dir)
            self._savetopkl(downloaded_image_infos, os.path.join(work_dir, 'download_results.pkl'))
        else:
            work_dir = self.work_dir
        self.logger_handle.info(f'Finished downloading images using {self.source}. Download results have been saved to {work_dir}, valid downloads: {len(downloaded_image_infos)}.', disable_print=self.disable_print)
        # return
        return downloaded_image_infos
    '''_autosetproxies'''
    def _autosetproxies(self):
        if self.auto_set_proxies:
            try: self.session.proxies = self.proxied_session_client.getrandomproxy()
            except Exception as err: self.logger_handle.error(f'{self.source}._autosetproxies >>> freeproxy lib failed to auto fetch proxies (Error: {err})', disable_print=self.disable_print); self.session.proxies = {}
        else:
            self.session.proxies = {}
    '''get'''
    def get(self, url, **kwargs):
        if 'cookies' not in kwargs: kwargs['cookies'] = self.default_cookies
        if 'impersonate' not in kwargs and self.enable_curl_cffi: kwargs['impersonate'] = random.choice(self.cc_impersonates)
        resp = None
        for _ in range(self.max_retries):
            if not self.maintain_session:
                self._initsession()
                if self.random_update_ua: self.session.headers.update({'User-Agent': UserAgent().random})
            self._autosetproxies()
            proxies = kwargs.pop('proxies', None) or self.session.proxies
            try: (resp := self.session.get(url, proxies=proxies, **kwargs)).raise_for_status()
            except Exception as err: self.logger_handle.error(f'{self.source}.get >>> {url} (Error: {err}; status={getattr(locals().get("resp"), "status_code", None)})', disable_print=self.disable_print); continue
            return resp
        return resp
    '''post'''
    def post(self, url, **kwargs):
        if 'cookies' not in kwargs: kwargs['cookies'] = self.default_cookies
        if 'impersonate' not in kwargs and self.enable_curl_cffi: kwargs['impersonate'] = random.choice(self.cc_impersonates)
        resp = None
        for _ in range(self.max_retries):
            if not self.maintain_session:
                self._initsession()
                if self.random_update_ua: self.session.headers.update({'User-Agent': UserAgent().random})
            self._autosetproxies()
            proxies = kwargs.pop('proxies', None) or self.session.proxies
            try: (resp := self.session.post(url, proxies=proxies, **kwargs)).raise_for_status()
            except Exception as err: self.logger_handle.error(f'{self.source}.post >>> {url} (Error: {err}; status={getattr(locals().get("resp"), "status_code", None)})', disable_print=self.disable_print); continue
            return resp
        return resp
    '''_savetopkl'''
    def _savetopkl(self, data, file_path, auto_sanitize=True):
        if auto_sanitize: file_path = sanitize_filepath(file_path)
        with open(file_path, 'wb') as fp: pickle.dump(data, fp)