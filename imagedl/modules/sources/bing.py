'''
Function:
    Implementation of BingImageClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import math
from lxml import etree
from urllib.parse import quote
from .base import BaseImageClient


'''BingImageClient'''
class BingImageClient(BaseImageClient):
    source = 'BingImageClient'
    def __init__(self, **kwargs):
        super(BingImageClient, self).__init__(**kwargs)
    '''_parsesearchresult'''
    def _parsesearchresult(self, search_result: str):
        image_infos = []
        html = etree.HTML(search_result)
        if not html: return image_infos
        for item in html.xpath('//a[@class="iusc"]/@m'):
            try:
                url = re.search('"murl":"(.*?)"', item).group(1)
            except:
                continue
            if not url.strip(): continue
            image_info = {
                'url': url.strip(), 'raw_data': item
            }
            image_infos.append(image_info)
        return image_infos
    '''_constructsearchurls'''
    def _constructsearchurls(self, keyword, search_limits=1000):
        base_url = 'https://cn.bing.com/images/async?q={}&first={}&count={}&cw=1536&ch=240&relp={}&tsc=ImageBasicHover&datsrc=I&layout=RowBased&mmasync=1&dgState=x*1063_y*768_h*186_c*5_i*71_r*10&IG=D6A4AD486F3A49F1BE164BC50750D641&SFX=3&iid=images.5555'
        search_urls, page_size = [], 35
        for pn in range(math.ceil(search_limits * 1.2 / page_size)):
            search_url = base_url.format(quote(keyword), pn * page_size, page_size, page_size)
            search_urls.append(search_url)
        return search_urls