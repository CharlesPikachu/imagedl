'''
Function:
    Implementation of Dedicated ImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from imagedl.modules.sources import (
    BingImageClient, I360ImageClient, YahooImageClient, BaiduImageClient, SogouImageClient, GoogleImageClient, YandexImageClient, PixabayImageClient, FreeImagesImageClient, PicJumboImageClient, EverypixelImageClient,
    DuckduckgoImageClient, UnsplashImageClient, GelbooruImageClient, SafebooruImageClient, DanbooruImageClient, PexelsImageClient, DimTownImageClient, StockSnapImageClient, LifeOfPixImageClient, OpenverseImageClient, 
    FoodiesfeedImageClient, FreeNatureStockImageClient, WeiboImageClient, GratisoGraphyImageClient, INaturalistImageClient, NASAImageClient, HuabanImageClient, GBIFImageClient, LocGovImageClient, WikipediaImageClient,
	YandeImageClient, JikanImageClient, FlickrImageClient,
)

# bing tests
client = BingImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# 360 tests
client = I360ImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# baidu tests
client = BaiduImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# sogou tests
client = SogouImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# google tests
client = GoogleImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# yandex tests
client = YandexImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# pixabay tests
client = PixabayImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# duckduckgo tests
client = DuckduckgoImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# yahoo tests
client = YahooImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# unsplash tests
client = UnsplashImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# gelbooru tests
client = GelbooruImageClient()
image_infos = client.search('pikachu', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# safebooru tests
client = SafebooruImageClient()
image_infos = client.search('pikachu', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# danbooru tests
client = DanbooruImageClient()
image_infos = client.search('pikachu', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# pexels tests
client = PexelsImageClient()
image_infos = client.search('animals', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# dimtown tests 
client = DimTownImageClient()
image_infos = client.search('JK', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# huaban tests 
client = HuabanImageClient()
image_infos = client.search('JK', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# foodiesfeed tests 
client = FoodiesfeedImageClient()
image_infos = client.search('pizza', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# everypixel tests
client = EverypixelImageClient()
image_infos = client.search('animals', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# freenaturestock tests 
client = FreeNatureStockImageClient()
image_infos = client.search('mountains', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# weibo tests (cookies required)
client = WeiboImageClient(default_search_cookies='xxxx')
image_infos = client.search('animals', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# stocksnap tests 
client = StockSnapImageClient()
image_infos = client.search('mountains', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# freeimages tests 
client = FreeImagesImageClient()
image_infos = client.search('mountains', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# lifeofpix tests 
client = LifeOfPixImageClient()
image_infos = client.search('mountains', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# gratisography tests 
client = GratisoGraphyImageClient()
image_infos = client.search('mountains', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# picjumbo tests
client = PicJumboImageClient()
image_infos = client.search('mountains', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# openverse tests
client = OpenverseImageClient()
image_infos = client.search('pikachu', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# inaturalist tests
client = INaturalistImageClient()
image_infos = client.search('Red Panda', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# nasa tests
client = NASAImageClient()
image_infos = client.search('James Webb', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# gbif tests
client = GBIFImageClient()
image_infos = client.search('jellyfish', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# loc.gov tests
client = LocGovImageClient()
image_infos = client.search('apollo 11', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# yande tests
client = YandeImageClient()
image_infos = client.search('pikachu', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# wiki tests
client = WikipediaImageClient()
image_infos = client.search('pikachu', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# jikan tests
client = JikanImageClient()
image_infos = client.search('pikachu', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# flickr tests
client = FlickrImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)