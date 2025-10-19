'''initialize'''
from .base import BaseImageClient
from .bing import BingImageClient
from .baidu import BaiduImageClient
from .google import GoogleImageClient
from ..utils import BaseModuleBuilder


'''ImageClientBuilder'''
class ImageClientBuilder(BaseModuleBuilder):
    REGISTERED_MODULES = {
        'BingImageClient': BingImageClient, 'BaiduImageClient': BaiduImageClient, 'GoogleImageClient': GoogleImageClient
    }


'''BuildImageClient'''
BuildImageClient = ImageClientBuilder().build