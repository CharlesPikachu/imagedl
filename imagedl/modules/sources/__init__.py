'''initialize'''
from .base import BaseImageClient
from .bing import BingImageClient
from .i360 import I360ImageClient
from .baidu import BaiduImageClient
from .sogou import SogouImageClient
from .google import GoogleImageClient
from ..utils import BaseModuleBuilder
from .yandex import YandexImageClient
from .pixabay import PixabayImageClient
from .duckduckgo import DuckduckgoImageClient


'''ImageClientBuilder'''
class ImageClientBuilder(BaseModuleBuilder):
    REGISTERED_MODULES = {
        'BingImageClient': BingImageClient, 'BaiduImageClient': BaiduImageClient, 'GoogleImageClient': GoogleImageClient, 
        'I360ImageClient': I360ImageClient, 'PixabayImageClient': PixabayImageClient, 'YandexImageClient': YandexImageClient,
        'DuckduckgoImageClient': DuckduckgoImageClient, 'SogouImageClient': SogouImageClient,
    }


'''BuildImageClient'''
BuildImageClient = ImageClientBuilder().build