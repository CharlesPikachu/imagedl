'''initialize'''
from .base import BaseImageClient
from .bing import BingImageClient
from .i360 import I360ImageClient
from .baidu import BaiduImageClient
from .sogou import SogouImageClient
from .yahoo import YahooImageClient
from .weibo import WeiboImageClient
from .pexels import PexelsImageClient
from .google import GoogleImageClient
from ..utils import BaseModuleBuilder
from .yandex import YandexImageClient
from .huaban import HuabanImageClient
from .pixabay import PixabayImageClient
from .dimtown import DimTownImageClient
from .danbooru import DanbooruImageClient
from .unsplash import UnsplashImageClient
from .gelbooru import GelbooruImageClient
from .safebooru import SafebooruImageClient
from .duckduckgo import DuckduckgoImageClient
from .everypixel import EverypixelImageClient
from .foodiesfeed import FoodiesfeedImageClient
from .freenaturestock import FreeNatureStockImageClient


'''ImageClientBuilder'''
class ImageClientBuilder(BaseModuleBuilder):
    REGISTERED_MODULES = {
        'BingImageClient': BingImageClient,              'FoodiesfeedImageClient': FoodiesfeedImageClient,            'DanbooruImageClient': DanbooruImageClient,       'HuabanImageClient': HuabanImageClient,
        'BaiduImageClient': BaiduImageClient,            'DuckduckgoImageClient': DuckduckgoImageClient,              'UnsplashImageClient': UnsplashImageClient,       'WeiboImageClient': WeiboImageClient, 
        'I360ImageClient': I360ImageClient,              'FreeNatureStockImageClient': FreeNatureStockImageClient,    'SogouImageClient': SogouImageClient,             'YandexImageClient': YandexImageClient,
        'EverypixelImageClient': EverypixelImageClient,  'GoogleImageClient': GoogleImageClient,                      'SafebooruImageClient': SafebooruImageClient,     'YahooImageClient': YahooImageClient,
        'GelbooruImageClient': GelbooruImageClient,      'PexelsImageClient': PexelsImageClient,                      'PixabayImageClient': PixabayImageClient,         'DimTownImageClient': DimTownImageClient, 
    }


'''BuildImageClient'''
BuildImageClient = ImageClientBuilder().build