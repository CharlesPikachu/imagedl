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


'''Filter, refer to https://github.com/hellock/icrawler/blob/master/icrawler/builtin/filter.py'''
class Filter:
    def __init__(self):
        self.rules = {}
    '''addrule'''
    def addrule(self, name, format_fn, choices=None):
        assert callable(format_fn)
        assert choices is None or isinstance(choices, list)
        self.rules[name] = (format_fn, choices)
    '''apply'''
    def apply(self, options, sep=""):
        if options is None:
            return ""
        assert isinstance(options, dict)
        formatted = []
        for name, val in options.items():
            assert name in self.rules
            format_fn, choices = self.rules[name]
            if isinstance(choices, type) and not isinstance(val, choices):
                raise TypeError(f'filter option "{name}" must be a {choices.__name__}, not {type(val).__name__}')
            elif isinstance(choices, list) and val not in choices:
                raise ValueError('filter option "{}" must be one of the following: {}'.format(name, ", ".join(choices)))
            formatted.append(format_fn(val))
        return sep.join(formatted)