'''
Function:
    Implementation of ImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import sys
import click
import random
import json_repair
if __name__ == '__main__':
    from __init__ import __version__
    from modules import BuildImageClient, LoggerHandle, ImageClientBuilder, BaseImageClient
else:
    from .__init__ import __version__
    from .modules import BuildImageClient, LoggerHandle, ImageClientBuilder, BaseImageClient


'''BASIC_INFO'''
BASIC_INFO = '''************************************************************
Function: Image Downloader --- v%s
Author: Zhenchao Jin
WeChat Official Account (微信公众号): Charles的皮卡丘
Operation Help:
    Enter `r`: Reinitialize the program (i.e., return to the main menu).
    Enter `q`: Exit the program.
Image Save Path:
    Inside the %s folder (root dir is the current directory if using relative path).
************************************************************'''


'''ImageClient'''
class ImageClient():
    def __init__(self, image_source: str = 'BaiduImageClient', init_image_client_cfg: dict = {}, search_limits: int = 1000, num_threadings: int = 5, request_overrides: dict = {}):
        # init
        self.logger_handle = LoggerHandle()
        if image_source is None: random.choice(ImageClientBuilder.REGISTERED_MODULES.keys())
        # instance image_client
        default_image_client_cfg = {
            'work_dir': 'imagedl_outputs', 'logger_handle': self.logger_handle, 'type': image_source,
        }
        default_image_client_cfg.update(init_image_client_cfg)
        self.image_client: BaseImageClient = BuildImageClient(module_cfg=default_image_client_cfg)
        # set attributes
        self.work_dir = default_image_client_cfg['work_dir']
        self.search_limits = search_limits
        self.num_threadings = num_threadings
        self.request_overrides = request_overrides
    '''startcmdui'''
    def startcmdui(self):
        while True:
            print(BASIC_INFO % (__version__, self.work_dir))
            # process user inputs
            user_input = self.processinputs('Please enter keywords for the image search: ')
            # search
            image_infos = self.image_client.search(
                keyword=user_input, search_limits=self.search_limits, num_threadings=self.num_threadings, request_overrides=self.request_overrides
            )
            # download
            self.image_client.download(image_infos=image_infos, num_threadings=self.num_threadings, request_overrides=self.request_overrides)
    '''search'''
    def search(self, keyword, search_limits_overrides: int = None, num_threadings_overrides: int = None, filters: dict = None):
        return self.image_client.search(
            keyword=keyword, search_limits=search_limits_overrides or self.search_limits, 
            num_threadings=num_threadings_overrides or self.num_threadings, filters=filters,
            request_overrides=self.request_overrides
        )
    '''download'''
    def download(self, image_infos: list, num_threadings_overrides: int = None):
        return self.image_client.download(
            image_infos=image_infos, num_threadings=num_threadings_overrides or self.num_threadings, request_overrides=self.request_overrides
        )
    '''processinputs'''
    def processinputs(self, input_tip='', prefix: str = '\n'):
        # accept user inputs
        user_input = input(prefix + input_tip)
        # quit
        if user_input.lower() == 'q':
            self.logger_handle.info('Goodbye — thanks for using imagedl; come back anytime!')
            sys.exit()
        # restart
        elif user_input.lower() == 'r':
            self.startcmdui()
        # common inputs
        else:
            return user_input
    '''str'''
    def __str__(self):
        return 'Welcome to use imagedl!\nYou can visit https://github.com/CharlesPikachu/imagedl for more details.'


'''ImageClientCMD'''
@click.command()
@click.version_option(version=__version__)
@click.option(
    '-k', '--keyword', default=None, help='The keywords for the image search. If left empty, an interactive terminal will open automatically.', type=str, show_default=True,
)
@click.option(
    '-i', '--image-source', '--image_source', default='BaiduImageClient', help='The image search and download source.', type=click.Choice(ImageClientBuilder.REGISTERED_MODULES.keys(), case_sensitive=False), show_default=True, 
)
@click.option(
    '-s', '--search-limits', '--search_limits', default=1000, help='Scale of image downloads.', type=click.IntRange(min=1, max=1e8), show_default=True,
)
@click.option(
    '-n', '--num-threadings', '--num_threadings', default=5, help='Number of threads used.', type=click.IntRange(min=1, max=256), show_default=True,
)
@click.option(
    '-c', '--init-image-client-cfg', '--init_image_client_cfg', default=None, help='Client config such as `work_dir` as a JSON string.', type=str, show_default=True,
)
@click.option(
    '-r', '--request-overrides', '--request_overrides', default=None, help='Requests.get kwargs such as `headers` and `proxies` as a JSON string.', type=str, show_default=True,
)
def ImageClientCMD(keyword, image_source, search_limits, num_threadings, init_image_client_cfg, request_overrides):
    # load json string
    def _safe_load(string):
        if string is not None:
            result = json_repair.loads(string) or {}
        else:
            result = {}
        return result
    init_image_client_cfg = _safe_load(init_image_client_cfg)
    request_overrides = _safe_load(request_overrides)
    # instance image client
    image_client = ImageClient(
        image_source=image_source, init_image_client_cfg=init_image_client_cfg, request_overrides=request_overrides, search_limits=search_limits, num_threadings=num_threadings,
    )
    # switch according to keyword
    if keyword is None:
        image_client.startcmdui()
    else:
        print(image_client)
        # --search
        image_infos = image_client.image_client.search(
            keyword=keyword, search_limits=image_client.search_limits, num_threadings=image_client.num_threadings, request_overrides=image_client.request_overrides
        )
        # --download
        image_client.image_client.download(image_infos=image_infos, num_threadings=image_client.num_threadings, request_overrides=image_client.request_overrides)


'''tests'''
if __name__ == '__main__':
    image_client = ImageClient()
    image_client.startcmdui()