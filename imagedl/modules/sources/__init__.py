'''initialize'''
from .base import BaseImageClient
from .bing import BingImageClient
from .i360 import I360ImageClient
from .baidu import BaiduImageClient
from .sogou import SogouImageClient
from .yahoo import YahooImageClient
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
        'BingImageClient': BingImageClient, 'BaiduImageClient': BaiduImageClient, 'GoogleImageClient': GoogleImageClient, 'FoodiesfeedImageClient': FoodiesfeedImageClient, 
        'PixabayImageClient': PixabayImageClient, 'YandexImageClient': YandexImageClient, 'DuckduckgoImageClient': DuckduckgoImageClient, 'SogouImageClient': SogouImageClient, 
        'YahooImageClient': YahooImageClient, 'UnsplashImageClient': UnsplashImageClient, 'SafebooruImageClient': SafebooruImageClient, 'DanbooruImageClient': DanbooruImageClient,
        'GelbooruImageClient': GelbooruImageClient, 'PexelsImageClient': PexelsImageClient, 'DimTownImageClient': DimTownImageClient, 'HuabanImageClient': HuabanImageClient,
        'I360ImageClient': I360ImageClient, 'EverypixelImageClient': EverypixelImageClient, 'FreeNatureStockImageClient': FreeNatureStockImageClient,
    }


'''BuildImageClient'''
BuildImageClient = ImageClientBuilder().build