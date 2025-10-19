'''
Function:
    Implementation of ImageClients test
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from imagedl.modules.sources.bing import BingImageClient
from imagedl.modules.sources.baidu import BaiduImageClient
from imagedl.modules.sources.google import GoogleImageClient


# bing tests
client = BingImageClient(auto_set_proxies=False, auto_set_headers=False)
image_infos = client.search('美女', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# baidu tests
client = BaiduImageClient(auto_set_proxies=False, auto_set_headers=False)
image_infos = client.search('美女', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# google tests
client = GoogleImageClient(auto_set_proxies=False, auto_set_headers=False)
image_infos = client.search('美女', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)