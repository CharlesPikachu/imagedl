'''
Function:
    图片下载器
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import sys
import time
import click
if __name__ == '__main__':
    from modules import *
    from __init__ import __version__
else:
    from .modules import *
    from .__init__ import __version__


'''basic info'''
BASICINFO = '''************************************************************
Function: 图片下载器 V%s
Author: Charles
微信公众号: Charles的皮卡丘
操作帮助:
    输入r: 重新初始化程序(即返回主菜单)
    输入q: 退出程序
图片保存路径:
    当前路径下的%s文件夹内
************************************************************'''


'''图片下载器'''
class imagedl():
    def __init__(self, configpath=None, config=None, **kwargs):
        assert configpath or config, 'configpath or config should be given'
        self.config = loadconfig(configpath) if config is None else config
        self.supported_sources = {
            'bing': BingImageDownloader,
            'baidu': BaiduImageDownloader,
            'google': GoogleImageDownloader,
        }
    '''运行'''
    def run(self, target_src=None):
        while True:
            print(BASICINFO % (__version__, self.config.get('savedir')))
            # 输入关键字
            user_input = self.dealInput('请输入图片搜索的关键词: ')
            target_src = 'baidu' if target_src is None else target_src
            # 初始化
            selected_api = self.supported_sources[target_src](
                auto_set_proxies=self.config.get('auto_set_proxies', True), 
                auto_set_headers=self.config.get('auto_set_headers', True),
            )
            # 开始下载
            selected_api.download(
                keyword=user_input, 
                search_limits=self.config.get('search_limits', 1000), 
                num_threadings=self.config.get('num_threadings', 5), 
                savedir=self.config.get('savedir'),
            )
    '''处理用户输入'''
    def dealInput(self, tip=''):
        user_input = input(tip)
        if user_input.lower() == 'q':
            self.logging('ByeBye')
            sys.exit()
        elif user_input.lower() == 'r':
            self.run()
        else:
            return user_input
    '''logging'''
    def logging(self, msg, tip='INFO'):
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} {tip}]: {msg}')
    '''str'''
    def __str__(self):
        return 'Welcome to use imagedl!\nYou can visit https://github.com/CharlesPikachu/imagedl for more details.'


'''cmd直接运行'''
@click.command()
@click.version_option()
@click.option('-k', '--keyword', default=None, help='想要搜索下载的图片关键字, 若不指定, 则进入imagedl终端版')
@click.option('-s', '--savedir', default='images', help='下载的图片的保存路径')
@click.option('-t', '--target', default='baidu', help='指定图片搜索下载的平台, 例如"baidu"')
@click.option('-l', '--limits', default=1000, help='下载的图片数量')
@click.option('-n', '--nthreadings', default=5, help='使用的线程数量')
def imagedlcmd(keyword, savedir, target, limits, nthreadings):
    config = {
        'savedir': savedir,
        'auto_set_proxies': True,
        'auto_set_headers': True,
        'search_limits': limits,
        'num_threadings': nthreadings,
    }
    dl_client = imagedl(config=config)
    if keyword is None:
        dl_client.run(target_src=target)
    else:
        print(dl_client)
        supported_sources = {
            'bing': BingImageDownloader,
            'baidu': BaiduImageDownloader,
            'google': GoogleImageDownloader,
        }
        selected_api = supported_sources[target](
            auto_set_proxies=config.get('auto_set_proxies', True), 
            auto_set_headers=config.get('auto_set_headers', True),
        )
        selected_api.download(
            keyword=keyword, 
            search_limits=config.get('search_limits', 1000), 
            num_threadings=config.get('num_threadings', 5), 
            savedir=config.get('savedir'),
        )


'''run'''
if __name__ == '__main__':
    dl_client = imagedl('config.json')
    dl_client.run()