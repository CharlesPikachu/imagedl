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
import random
import requests
import json_repair
from pathlib import Path
from threading import Lock
from rich.text import Text
from itertools import chain
from datetime import datetime
from collections import defaultdict
from fake_useragent import UserAgent
from pathvalidate import sanitize_filepath
from typing import TYPE_CHECKING, Iterable
from concurrent.futures import ThreadPoolExecutor, as_completed
from ..utils import usedownloadheaderscookies, usesearchheaderscookies, touchdir, cookies2dict, optionalimport, optionalimportfrom, LoggerHandle, Filter, ImageInfo, ImageExtensionUtils
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn, MofNCompleteColumn, ProgressColumn, Task


'''ImageAwareColumn'''
class ImageAwareColumn(ProgressColumn):
    def __init__(self):
        super(ImageAwareColumn, self).__init__()
        self._download_col = DownloadColumn()
    '''render'''
    def render(self, task: Task):
        kind = task.fields.get("kind", "download")
        if kind == "overall": completed = int(task.completed); total = int(task.total) if task.total is not None else 0; return Text(f"{completed}/{total} images")
        else: return self._download_col.render(task)


'''BaseImageClient'''
class BaseImageClient():
    source = 'BaseImageClient'
    def __init__(self, auto_set_proxies: bool = False, random_update_ua: bool = False, enable_search_curl_cffi: bool = False, enable_download_curl_cffi: bool = False, max_retries: int = 5, logger_handle: LoggerHandle = None, 
                 maintain_session: bool = False, disable_print: bool = False, work_dir: str = 'imagedl_outputs', freeproxy_settings: dict = None, default_search_cookies: dict = None, default_download_cookies: dict = None):
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
        freeproxy = optionalimportfrom('freeproxy', 'freeproxy')
        if TYPE_CHECKING: from freeproxy import freeproxy
        (default_freeproxy_settings := dict(disable_print=True, proxy_sources=['ProxiflyProxiedSession'], max_tries=20, init_proxied_session_cfg={})).update(self.freeproxy_settings)
        self.proxied_session_client = freeproxy.ProxiedSessionClient(**default_freeproxy_settings) if auto_set_proxies else None
    '''_listccimpersonates'''
    def _listccimpersonates(self):
        curl_cffi = optionalimport('curl_cffi')
        if TYPE_CHECKING: import curl_cffi
        root = Path(curl_cffi.__file__).resolve().parent
        exts = {".py", ".so", ".pyd", ".dll", ".dylib"}
        pat = re.compile(rb"\b(?:chrome|edge|safari|firefox|tor)(?:\d+[a-z_]*|_android|_ios)?\b")
        return sorted({m.decode("utf-8", "ignore") for p in root.rglob("*") if p.suffix in exts for m in pat.findall(p.read_bytes())})
    '''_initsession'''
    def _initsession(self):
        curl_cffi = optionalimport('curl_cffi')
        if TYPE_CHECKING: import curl_cffi
        self.session = requests.Session() if not self.enable_curl_cffi else curl_cffi.requests.Session()
        self.session.headers = self.default_headers
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword: str, search_limits: int = 1000, filters: dict = None, request_overrides: dict = None):
        raise NotImplementedError('not to be implemented')
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str) -> list[ImageInfo]:
        search_result = json_repair.loads(search_result)
        return search_result
    '''_removeduplicates'''
    def _removeduplicates(self, image_infos: list[ImageInfo] = None) -> list[ImageInfo]:
        unique_image_infos, identifiers = [], set()
        for image_info in image_infos:
            if image_info.identifier in identifiers: continue
            identifiers.add(image_info.identifier); unique_image_infos.append(image_info)
        return unique_image_infos
    '''_appenduniquefilepathforimages'''
    def _appenduniquefilepathforimages(self, keyword: str, image_infos: list[ImageInfo]):
        time_stamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        work_dir = sanitize_filepath(os.path.join(self.work_dir, self.source, f'{time_stamp} {keyword}')); touchdir(work_dir)
        for idx, image_info in enumerate(image_infos):
            image_info.work_dir = work_dir; image_info.save_name = f'{str(idx+1).zfill(8)}'; image_info.save_path = os.path.join(work_dir, image_info.save_name)
        return image_infos
    '''_getfilter'''
    def _getfilter(self):
        search_filter = Filter()
        return search_filter
    '''_search'''
    @usesearchheaderscookies
    def _search(self, keyword: str = '', search_url: str | dict = '', request_overrides: dict = None, image_infos: list = [], progress: Progress = None, progress_id: int = 0) -> list[ImageInfo]:
        # init
        request_overrides = request_overrides or {}
        # successful
        try:
            search_inputs, search_url, request_method = (search_url['inputs'], search_url['url'], search_url['method']) if isinstance(search_url, dict) else ({}, search_url, 'get')
            (resp := {'get': self.get, 'post': self.post}[request_method](search_url, **search_inputs, **request_overrides)).raise_for_status()
            resp.encoding = 'utf-8'; search_result = self._parsesearchresult(resp.text)
            if isinstance(search_result, dict): search_result = ImageInfo.fromdict(search_result)
            if isinstance(search_result, ImageInfo): search_result = [search_result]
            assert isinstance(search_result, Iterable), 'format of search_result should be in "list[ImageInfo]", "dict" or "ImageInfo"'
            image_infos.extend(list(search_result))
            progress.update(progress_id, description=f"{self.source}._search >>> {search_url} (Success)")
        # failure
        except Exception as err:
            progress.update(progress_id, description=f"{self.source}._search >>> {search_url} (Error: {err})")
            self.logger_handle.error(f'{self.source}._search >>> {search_url} (Error: {err})', disable_print=self.disable_print)
        # return
        return image_infos
    '''search'''
    @usesearchheaderscookies
    def search(self, keyword: str, search_limits: int = 1000, num_threadings: int = 5, filters: dict = None, request_overrides: dict = None, main_process_context: Progress = None, main_progress_id: int = None, main_progress_lock: Lock = None) -> list[ImageInfo]:
        # init
        filters, request_overrides = filters or {}, request_overrides or {}
        # logging
        self.logger_handle.info(f'Start to search images using {self.source}.', disable_print=self.disable_print)
        # construct search urls
        search_urls = self._constructsearchurls(keyword=keyword, search_limits=search_limits, filters=filters, request_overrides=request_overrides)
        # multi threadings for searching images
        if main_process_context is None: owns_progress = True; main_process_context = Progress(TextColumn("{task.description}"), BarColumn(bar_width=None), MofNCompleteColumn(), TimeRemainingColumn(), refresh_per_second=10); main_process_context.__enter__()
        else: owns_progress = False
        if main_progress_lock is None: main_progress_lock = Lock()
        with main_progress_lock:
            progress_id = main_process_context.add_task(f"{self.source}.search >>> completed (0/{len(search_urls)})", total=len(search_urls))
            if main_progress_id is not None:
                cur_total = main_process_context.tasks[main_progress_id].total or 0
                main_process_context.update(main_progress_id, total=cur_total + len(search_urls))
                main_process_context.update(main_progress_id, description=f"Search from sources >>> completed ({int(main_process_context.tasks[main_progress_id].completed)}/{cur_total + len(search_urls)})")
        image_infos, submitted_tasks = {}, []
        with ThreadPoolExecutor(max_workers=num_threadings) as pool:
            for search_url_idx, search_url in enumerate(search_urls):
                image_infos[str(search_url_idx)] = []
                submitted_tasks.append(pool.submit(self._search, keyword, search_url, request_overrides, image_infos[str(search_url_idx)], main_process_context, progress_id))
            for future in as_completed(submitted_tasks):
                future.result()
                with main_progress_lock:
                    main_process_context.advance(progress_id, 1)
                    num_searched_urls = int(main_process_context.tasks[progress_id].completed)
                    main_process_context.update(progress_id, description=f"{self.source}.search >>> completed ({num_searched_urls}/{len(search_urls)})")
                    if main_progress_id is None: continue
                    main_process_context.advance(main_progress_id, 1)
                    main_process_context.update(main_progress_id, description=f"Search from sources >>> completed ({int(main_process_context.tasks[main_progress_id].completed)}/{int(main_process_context.tasks[main_progress_id].total or 0)})")
        image_infos = list(chain.from_iterable(image_infos.values())); image_infos = self._removeduplicates(image_infos=image_infos)
        image_infos = self._appenduniquefilepathforimages(image_infos=image_infos, keyword=keyword)
        # logging
        if len(image_infos) > 0:
            work_dir_to_image_info, work_dir = defaultdict(list), ', '.join(list(set([str(img_info.work_dir) for img_info in image_infos])))
            for img_info in image_infos: img_info.work_dir = str(img_info.work_dir); work_dir_to_image_info[img_info.work_dir].append(img_info.todict())
            for w, items in work_dir_to_image_info.items(): touchdir(w); self._savetopkl(items, os.path.join(w, "search_results.pkl"))
        else:
            work_dir = self.work_dir
        self.logger_handle.info(f'Finished searching images using {self.source}. Search results have been saved to {work_dir}, valid items: {len(image_infos)}.', disable_print=self.disable_print)
        if owns_progress: main_process_context.__exit__(None, None, None)
        # return
        return image_infos
    '''_download'''
    @usedownloadheaderscookies
    def _download(self, image_info: ImageInfo, request_overrides: dict = None, downloaded_image_infos: list[ImageInfo] = None) -> list[ImageInfo]:
        # init
        request_overrides = copy.deepcopy(request_overrides or {}); touchdir(image_info.work_dir)
        for candidate_download_url in image_info.candidate_download_urls:
            if image_info.download_headers: request_overrides['headers'] = image_info.download_headers
            if image_info.download_cookies: request_overrides['cookies'] = image_info.download_cookies
            try: (resp := self.get(candidate_download_url, **request_overrides)).raise_for_status()
            except Exception: continue
            if not (ext_detect_result := ImageExtensionUtils.detectimagefile(binary_content=resp.content))['ok']: continue
            image_info.download_url = candidate_download_url
            image_info.ext_detect_result = ext_detect_result; image_info.ext = ext_detect_result['ext']
            image_info.save_name = f"{image_info.save_name}.{image_info.ext}"
            image_info.save_path = os.path.join(image_info.work_dir, image_info.save_name)
            with open(image_info.save_path, 'wb') as fp: fp.write(resp.content)
            downloaded_image_infos.append(image_info); break
        return downloaded_image_infos
    '''download'''
    @usedownloadheaderscookies
    def download(self, image_infos: list[ImageInfo], num_threadings: int = 5, request_overrides: dict = None) -> list[ImageInfo]:
        # init
        request_overrides = request_overrides or {}
        for img_info in image_infos: img_info.work_dir = sanitize_filepath(os.path.dirname(img_info.save_path))
        # logging
        self.logger_handle.info(f'Start to download images using {self.source}.', disable_print=self.disable_print)
        # multi threadings for downloading images
        columns = [SpinnerColumn(), TextColumn("{task.description}"), BarColumn(bar_width=None), TaskProgressColumn(), ImageAwareColumn(), TransferSpeedColumn(), TimeRemainingColumn()]
        with Progress(*columns, refresh_per_second=20, expand=True) as progress:
            images_progress_id, submitted_tasks = progress.add_task(f"{self.source}.download >>> completed (0/{len(image_infos)})", total=len(image_infos), kind='overall'), []; downloaded_image_infos: list[ImageInfo] = []
            with ThreadPoolExecutor(max_workers=num_threadings) as pool:
                for image_info in image_infos: submitted_tasks.append(pool.submit(self._download, image_info, request_overrides, downloaded_image_infos))
                for _ in as_completed(submitted_tasks):
                    progress.advance(images_progress_id, 1)
                    num_downloaded_images = int(progress.tasks[images_progress_id].completed)
                    progress.update(images_progress_id, description=f"{self.source}.download >>> completed ({num_downloaded_images}/{len(image_infos)})")
        # logging
        if len(downloaded_image_infos) > 0:
            work_dir_to_image_info, work_dir = defaultdict(list), ', '.join(list(set([str(img_info.work_dir) for img_info in downloaded_image_infos])))
            for img_info in downloaded_image_infos: img_info.work_dir = str(img_info.work_dir); work_dir_to_image_info[img_info.work_dir].append(img_info.todict())
            for w, items in work_dir_to_image_info.items(): touchdir(w); self._savetopkl(items, os.path.join(w, "download_results.pkl"))
        else:
            work_dir = self.work_dir
        self.logger_handle.info(f'Finished downloading images using {self.source}. Download results have been saved to {work_dir}, valid downloads: {len(downloaded_image_infos)}.', disable_print=self.disable_print)
        # return
        return downloaded_image_infos
    '''_autosetproxies'''
    def _autosetproxies(self):
        if not self.auto_set_proxies: return {}
        try: proxies = self.proxied_session_client.getrandomproxy()
        except Exception as err: self.logger_handle.error(f'{self.source}._autosetproxies >>> freeproxy lib failed to auto fetch proxies (Error: {err})', disable_print=self.disable_print); proxies = {}
        return proxies
    '''get'''
    def get(self, url, **kwargs):
        if 'cookies' not in kwargs: kwargs['cookies'] = self.default_cookies
        if 'impersonate' not in kwargs and self.enable_curl_cffi: kwargs['impersonate'] = random.choice(self.cc_impersonates)
        resp, cloudscraper = None, optionalimport('cloudscraper')
        if TYPE_CHECKING: import cloudscraper
        for _ in range(self.max_retries):
            if not self.maintain_session:
                self._initsession()
                if self.random_update_ua: self.session.headers.update({'User-Agent': UserAgent().random})
            proxies = kwargs.pop('proxies', None) or self._autosetproxies()
            try: (resp := self.session.get(url, proxies=proxies, **kwargs)).raise_for_status(); return resp
            except Exception as err: self.logger_handle.error(f'{self.source}.get >>> {url} (Error: {err}; status={getattr(locals().get("resp"), "status_code", None)})', disable_print=self.disable_print)
            if self.enable_curl_cffi: continue
            try: (resp := cloudscraper.create_scraper(sess=self.session).get(url, proxies=proxies, **kwargs)).raise_for_status()
            except Exception as err: self.logger_handle.error(f'{self.source}.get >>> {url} (Error: {err}; status={getattr(locals().get("resp"), "status_code", None)})', disable_print=self.disable_print); continue
            return resp
        return resp
    '''post'''
    def post(self, url, **kwargs):
        if 'cookies' not in kwargs: kwargs['cookies'] = self.default_cookies
        if 'impersonate' not in kwargs and self.enable_curl_cffi: kwargs['impersonate'] = random.choice(self.cc_impersonates)
        resp, cloudscraper = None, optionalimport('cloudscraper')
        if TYPE_CHECKING: import cloudscraper
        for _ in range(self.max_retries):
            if not self.maintain_session:
                self._initsession()
                if self.random_update_ua: self.session.headers.update({'User-Agent': UserAgent().random})
            proxies = kwargs.pop('proxies', None) or self._autosetproxies()
            try: (resp := self.session.post(url, proxies=proxies, **kwargs)).raise_for_status(); return resp
            except Exception as err: self.logger_handle.error(f'{self.source}.post >>> {url} (Error: {err}; status={getattr(locals().get("resp"), "status_code", None)})', disable_print=self.disable_print)
            if self.enable_curl_cffi: continue
            try: (resp := cloudscraper.create_scraper(sess=self.session).post(url, proxies=proxies, **kwargs)).raise_for_status()
            except Exception as err: self.logger_handle.error(f'{self.source}.post >>> {url} (Error: {err}; status={getattr(locals().get("resp"), "status_code", None)})', disable_print=self.disable_print); continue
            return resp
        return resp
    '''_savetopkl'''
    def _savetopkl(self, data, file_path, auto_sanitize=True):
        if auto_sanitize: file_path = sanitize_filepath(file_path)
        with open(file_path, 'wb') as fp: pickle.dump(data, fp)