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
from .picjumbo import PicJumboImageClient
from .safebooru import SafebooruImageClient
from .stocksnap import StockSnapImageClient
from .lifeofpix import LifeOfPixImageClient
from .openverse import OpenverseImageClient
from .duckduckgo import DuckduckgoImageClient
from .freeimages import FreeImagesImageClient
from .everypixel import EverypixelImageClient
from .inaturalist import INaturalistImageClient
from .foodiesfeed import FoodiesfeedImageClient
from .gratisography import GratisoGraphyImageClient
from .freenaturestock import FreeNatureStockImageClient


'''ImageClientBuilder'''
class ImageClientBuilder(BaseModuleBuilder):
    REGISTERED_MODULES = {
        'BingImageClient': BingImageClient,              'FoodiesfeedImageClient': FoodiesfeedImageClient,            'DanbooruImageClient': DanbooruImageClient,         'HuabanImageClient': HuabanImageClient,
        'BaiduImageClient': BaiduImageClient,            'DuckduckgoImageClient': DuckduckgoImageClient,              'UnsplashImageClient': UnsplashImageClient,         'WeiboImageClient': WeiboImageClient, 
        'I360ImageClient': I360ImageClient,              'FreeNatureStockImageClient': FreeNatureStockImageClient,    'SogouImageClient': SogouImageClient,               'YandexImageClient': YandexImageClient,
        'EverypixelImageClient': EverypixelImageClient,  'GoogleImageClient': GoogleImageClient,                      'SafebooruImageClient': SafebooruImageClient,       'YahooImageClient': YahooImageClient,
        'GelbooruImageClient': GelbooruImageClient,      'PexelsImageClient': PexelsImageClient,                      'PixabayImageClient': PixabayImageClient,           'DimTownImageClient': DimTownImageClient, 
        'StockSnapImageClient': StockSnapImageClient,    'FreeImagesImageClient': FreeImagesImageClient,              'LifeOfPixImageClient': LifeOfPixImageClient,       'GratisoGraphyImageClient': GratisoGraphyImageClient,
        'PicJumboImageClient': PicJumboImageClient,      'OpenverseImageClient': OpenverseImageClient,                'INaturalistImageClient': INaturalistImageClient,
    }


'''BuildImageClient'''
BuildImageClient = ImageClientBuilder().build