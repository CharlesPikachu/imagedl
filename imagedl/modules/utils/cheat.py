'''
Function:
    Implementation of Fake Data / Class Related Functions 
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import requests


'''FakeRequestsResponse'''
class FakeRequestsResponse(requests.Response):
    def __init__(self, predefined_text: str = "", encoding: str = "utf-8", status_code: int = 200):
        super(FakeRequestsResponse, self).__init__()
        self.encoding = encoding
        self.status_code = status_code
        self._fake_text = predefined_text
        self._content = predefined_text.encode(encoding)
    '''text'''
    @property
    def text(self): return self._fake_text
    '''raise_for_status'''
    def raise_for_status(self): return None