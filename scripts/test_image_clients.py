'''
Function:
    Implementation of Dedicated ImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from imagedl.modules.sources import (
    BingImageClient, I360ImageClient, YahooImageClient, BaiduImageClient, SogouImageClient, GoogleImageClient, YandexImageClient, PixabayImageClient, 
    DuckduckgoImageClient, UnsplashImageClient, GelbooruImageClient, SafebooruImageClient, DanbooruImageClient, PexelsImageClient, DimTownImageClient,
    HuabanImageClient, FoodiesfeedImageClient, EverypixelImageClient
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
# everypixel tests (cookies required)
client = EverypixelImageClient(default_search_cookies='client_id=e30f48e30aba6693e1302ac195e2e452; session_id=6ce6d099-06a7-404d-a63c-eb3a31e0acb9; userStatus=0; _ga=GA1.1.859071961.1770791608; cookie_popup_shown=1; _ga_7VBKBQ1JV6=GS2.1.s1770792674$o1$g1$t1770794235$j60$l0$h0; cf_clearance=enQ5xgDuEaSfid3kS7wxefIMDpRiHB3Yx4OxHUIqSTU-1770796404-1.2.1.1-ouhuNokK67vPqQ7zJYVq9FF3RG3tyOR_PrVj81VN_S2.NhMug.T_Y5kVzWdiRq0Br0hT0XPzaKIFDjC5WzUg6LR12K1olooapyvrxjCJzWlWGASxMc1Nc7iCBLWSd46oNqacv0cfwlPhw0vsjFaCxs0BXTqTEvRmlNLniamkr8vCv6gziegTOEUsXnL127W_MLqG_Ld17FYcG3XDYHHu1gCI3I7Jm5qTn.3q0mflsmY; _ga_FLYERKMCP5=GS2.1.s1770791608$o1$g1$t1770796826$j57$l0$h0')
image_infos = client.search('animals', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)