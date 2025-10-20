'''initialize'''
from .base import BaseImageClient
from .bing import BingImageClient
from .i360 import I360ImageClient
from .baidu import BaiduImageClient
from .google import GoogleImageClient
from ..utils import BaseModuleBuilder


'''ImageClientBuilder'''
class ImageClientBuilder(BaseModuleBuilder):
    REGISTERED_MODULES = {
        'BingImageClient': BingImageClient, 'BaiduImageClient': BaiduImageClient, 'GoogleImageClient': GoogleImageClient, 
        'I360ImageClient': I360ImageClient,
    }


'''BuildImageClient'''
BuildImageClient = ImageClientBuilder().build