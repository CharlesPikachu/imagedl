'''
Function:
    Implementation of Misc Utils
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import copy


'''lowerdictkeys'''
def lowerdictkeys(data: dict):
    if not isinstance(data, dict): return data
    data_new = dict()
    for k, v in data.items():
        if isinstance(k, str):
            data_new[k.lower()] = copy.deepcopy(v)
        else:
            data_new[k] = copy.deepcopy(v)
    return data_new