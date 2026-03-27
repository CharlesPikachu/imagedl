'''
Function:
    Implementation of ImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import sys
import copy
import click
import json_repair
from threading import Lock
from typing import Iterable
from concurrent.futures import ThreadPoolExecutor
from rich.progress import Progress, TextColumn, BarColumn, TimeRemainingColumn, MofNCompleteColumn
if __name__ == '__main__':
    from __init__ import __version__
    from modules import BuildImageClient, LoggerHandle, ImageClientBuilder, BaseImageClient, ImageInfo, printfullline, colorize
else:
    from .__init__ import __version__
    from .modules import BuildImageClient, LoggerHandle, ImageClientBuilder, BaseImageClient, ImageInfo, printfullline, colorize


'''BASIC_INFO'''
BASIC_INFO = '''Function: Image Downloader --- v%s
Author: Zhenchao Jin
WeChat Official Account (微信公众号): Charles的皮卡丘
Operation Help:
    Enter `r`: Reinitialize the program (i.e., return to the main menu).
    Enter `q`: Exit the program.
Image Save Path:
    Inside the %s folder (root dir is the current directory if using relative path).'''
DEFAULT_IMAGE_SOURCES = ['BaiduImageClient']


'''ImageClient'''
class ImageClient():
    def __init__(self, image_sources: list | str = 'BaiduImageClient', init_image_clients_cfg: dict = None, clients_threadings: dict = {}, requests_overrides: dict = {}, search_filters: dict = {}):
        # prepare and assert
        if isinstance(image_sources, str): image_sources = [image_sources]
        assert isinstance(image_sources, Iterable) and isinstance(init_image_clients_cfg, dict) and isinstance(clients_threadings, dict) and isinstance(requests_overrides, dict) and isinstance(search_filters, dict)
        image_sources, init_image_clients_cfg, clients_threadings, requests_overrides, search_filters = copy.deepcopy(image_sources), copy.deepcopy(init_image_clients_cfg), copy.deepcopy(clients_threadings), copy.deepcopy(requests_overrides), copy.deepcopy(search_filters)
        # set attributes
        self.work_dirs = {}
        self.search_filters = search_filters
        self.clients_threadings = clients_threadings
        self.requests_overrides = requests_overrides
        self.image_sources = list(set(image_sources if image_sources else DEFAULT_IMAGE_SOURCES))
        # init
        self.logger_handle = LoggerHandle(); self.image_clients: dict[str, BaseImageClient] = dict()
        for image_source in self.image_sources:
            if image_source not in ImageClientBuilder.REGISTERED_MODULES.keys(): continue
            init_image_client_cfg = {
                'auto_set_proxies': False, 'random_update_ua': False, 'enable_search_curl_cffi': False, 'enable_download_curl_cffi': False, 'max_retries': 5, 'maintain_session': False, 'logger_handle': self.logger_handle, 
                'disable_print': False, 'work_dir': 'imagedl_outputs', 'freeproxy_settings': None, 'default_search_cookies': None, 'default_download_cookies': None, 'type': image_source,
            }
            init_image_client_cfg.update(init_image_clients_cfg.get(image_source, {}))
            self.image_clients[image_source] = BuildImageClient(module_cfg=init_image_client_cfg)
            self.work_dirs[image_source] = init_image_client_cfg['work_dir']
            if image_source not in self.clients_threadings: self.clients_threadings[image_source] = 5
            if image_source not in self.requests_overrides: self.requests_overrides[image_source] = {}
            if image_source not in self.search_filters: self.search_filters[image_source] = {}
        assert self.image_clients, f'Invalid "image_sources", elements in "image_sources" should be in ({", ".join(ImageClientBuilder.REGISTERED_MODULES.keys())})'
    '''printbasicinfo'''
    def printbasicinfo(self):
        printfullline(ch='-')
        print(BASIC_INFO % (__version__, ', '.join([f'"{v} for {k}"' for k, v in self.work_dirs.items()])))
        printfullline(ch='-')
    '''startcmdui'''
    def startcmdui(self, search_limits_per_source: int | dict = 1000):
        while True:
            self.printbasicinfo()
            # process user inputs
            user_input_keyword = self.processinputs('Please enter keywords for the image search: ')
            # search
            search_results = self.search(keyword=user_input_keyword, search_limits_per_source=search_limits_per_source)
            # download
            self.download(image_infos=search_results)
    '''search'''
    def search(self, keyword, search_limits_per_source: int | dict = 1000):
        self.logger_handle.info(f'Searching {colorize(keyword, "highlight")} From {colorize("|".join(self.image_sources), "highlight")}')
        max_workers, main_progress_lock = min(len(self.image_sources), 10), Lock()
        if isinstance(search_limits_per_source, (int, float)): search_limits_per_source = {key: search_limits_per_source for key in self.image_sources}
        with Progress(TextColumn("{task.description}"), BarColumn(bar_width=None), MofNCompleteColumn(), TimeRemainingColumn(), refresh_per_second=10) as main_process_context:
            main_progress_id = main_process_context.add_task(f"Search from sources >>> completed (0/0)", total=0)
            def search_func(img_s):
                try:
                    return img_s, self.image_clients[img_s].search(keyword=keyword, search_limits=search_limits_per_source[img_s], num_threadings=self.clients_threadings[img_s], filters=self.search_filters[img_s], request_overrides=self.requests_overrides[img_s], main_process_context=main_process_context, main_progress_id=main_progress_id, main_progress_lock=main_progress_lock)
                except Exception as err:
                    self.logger_handle.error(f'ImageClient.{img_s}.search >>> {keyword} (Error: {err})')
                    return img_s, []
            with ThreadPoolExecutor(max_workers=max_workers) as ex:
                return dict(ex.map(search_func, self.image_sources))
    '''download'''
    def download(self, image_infos: list[ImageInfo]):
        classified_image_infos: dict[str, list] = {}
        for image_info in image_infos:
            if image_info.source in classified_image_infos: classified_image_infos[image_info.source].append(image_info)
            else: classified_image_infos[image_info.source] = [image_info]
        for source, source_image_infos in classified_image_infos.items():
            self.image_clients[source].download(image_infos=source_image_infos, num_threadings=self.clients_threadings[source], request_overrides=self.requests_overrides[source])
    '''processinputs'''
    def processinputs(self, input_tip='', prefix: str = '\n'):
        # accept user inputs
        user_input = input(prefix + input_tip)
        # quit
        if user_input.lower() == 'q': self.logger_handle.info('Goodbye — thanks for using imagedl; come back anytime!'); sys.exit()
        # restart
        elif user_input.lower() == 'r': self.startcmdui()
        # common inputs
        else: return user_input
    '''str'''
    def __str__(self):
        return 'Welcome to use imagedl!\nYou can visit https://github.com/CharlesPikachu/imagedl for more details.'


'''ImageClientCMD'''
@click.command()
@click.version_option(version=__version__)
@click.option('-k', '--keyword', default=None, help='The keywords for the image search. If left empty, an interactive terminal will open automatically.', type=str, show_default=True)
@click.option('-s', '--image-sources', '--image_sources', default=','.join(DEFAULT_IMAGE_SOURCES), help='The image search and download sources.', type=str, show_default=True)
@click.option('-c', '--init-image-clients-cfg', '--init_image_clients_cfg', default=None, help='Config such as `work_dir` for each image client as a JSON string.', type=str, show_default=True)
@click.option('-o', '--requests-overrides', '--requests_overrides', default=None, help='Requests.get / Requests.post kwargs such as `headers` and `proxies` for each image client as a JSON string.', type=str, show_default=True)
@click.option('-t', '--clients-threadings', '--clients_threadings', default=None, help='Number of threads used for each image client as a JSON string.', type=str, show_default=True)
@click.option('-f', '--search-filters', '--search_filters', default=None, help='Search filters for each image client as a JSON string.', type=str, show_default=True)
@click.option('-l', '--search-limits-per-source', '--search_limits_per_source', default=1000, help='Scale of image downloads.', type=click.IntRange(min=1, max=1e8), show_default=True)
def ImageClientCMD(keyword, image_sources: str, init_image_clients_cfg: str, requests_overrides: str, clients_threadings: str, search_filters: str, search_limits_per_source: str):
    # load json string
    safe_load_func = lambda string: (json_repair.loads(string) or {}) if string is not None else {}
    init_image_clients_cfg, requests_overrides = safe_load_func(init_image_clients_cfg), safe_load_func(requests_overrides)
    clients_threadings, search_filters = safe_load_func(clients_threadings), safe_load_func(search_filters)
    search_limits_per_source = float(search_limits_per_source) if str(search_limits_per_source).lstrip('-').replace('.', '', 1).isdigit() else safe_load_func(search_limits_per_source)
    # instance image client
    image_client = ImageClient(image_sources=image_sources.replace(' ', '').split(','), init_image_clients_cfg=init_image_clients_cfg, requests_overrides=requests_overrides, clients_threadings=clients_threadings, search_filters=search_filters)
    # switch according to keyword
    if keyword is None:
        image_client.startcmdui(search_limits_per_source=search_limits_per_source)
    else:
        print(image_client)
        # --search
        image_infos = image_client.search(keyword=keyword, search_limits_per_source=search_limits_per_source)
        # --download
        image_client.download(image_infos=image_infos)


'''tests'''
if __name__ == '__main__':
    image_client = ImageClient()
    image_client.startcmdui(search_limits_per_source=10)