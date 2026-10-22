'''
Function:
    Implementation of Misc Utils
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from __future__ import annotations
import re
import copy
import imghdr
import filetype
import functools
from PIL import Image
from io import BytesIO
from pathlib import Path
from http.cookies import SimpleCookie
from urllib.parse import urlsplit, unquote
from typing import Optional, Dict, Any, Protocol, Callable


'''usedownloadheaderscookies'''
def usedownloadheaderscookies(func):
    @functools.wraps(func)
    def wrapper(self: ClientProtocolObj, *args, **kwargs):
        self.default_headers = self.default_download_headers
        if hasattr(self, 'default_download_cookies'): self.default_cookies = self.default_download_cookies
        if hasattr(self, 'enable_download_curl_cffi'): self.enable_curl_cffi = self.enable_download_curl_cffi
        if hasattr(self, '_initsession'): self._initsession()
        return func(self, *args, **kwargs)
    return wrapper


'''useparseheaderscookies'''
def useparseheaderscookies(func):
    @functools.wraps(func)
    def wrapper(self: ClientProtocolObj, *args, **kwargs):
        self.default_headers = self.default_parse_headers
        if hasattr(self, 'default_parse_cookies'): self.default_cookies = self.default_parse_cookies
        if hasattr(self, 'enable_parse_curl_cffi'): self.enable_curl_cffi = self.enable_parse_curl_cffi
        if hasattr(self, '_initsession'): self._initsession()
        return func(self, *args, **kwargs)
    return wrapper


'''usesearchheaderscookies'''
def usesearchheaderscookies(func):
    @functools.wraps(func)
    def wrapper(self: ClientProtocolObj, *args, **kwargs):
        self.default_headers = self.default_search_headers
        if hasattr(self, 'default_search_cookies'): self.default_cookies = self.default_search_cookies
        if hasattr(self, 'enable_search_curl_cffi'): self.enable_curl_cffi = self.enable_search_curl_cffi
        if hasattr(self, '_initsession'): self._initsession()
        return func(self, *args, **kwargs)
    return wrapper


'''lowerdictkeys'''
def lowerdictkeys(data: dict):
    if not isinstance(data, dict): return data
    return {k.lower() if isinstance(k, str) else k: copy.deepcopy(v) for k, v in data.items()}


'''cookies2dict'''
def cookies2dict(cookies: str | dict = None) -> dict:
    if not cookies: cookies = {}
    if isinstance(cookies, dict): return cookies
    if isinstance(cookies, str): (c := SimpleCookie()).load(cookies); return {k: morsel.value for k, morsel in c.items()}
    raise TypeError(f'cookies type is "{type(cookies)}", expect cookies to "str" or "dict" or "None".')


'''cookies2string'''
def cookies2string(cookies: str | dict = None) -> str:
    if not cookies: cookies = ""
    if isinstance(cookies, str): return cookies
    if isinstance(cookies, dict): return (lambda c: ([c.__setitem__(k, "" if v is None else str(v)) for k, v in cookies.items()], "; ".join(m.OutputString() for m in c.values()))[1])(SimpleCookie())
    raise TypeError(f'cookies type is "{type(cookies)}", expect cookies to "str" or "dict" or "None".')


'''hashablesth'''
def hashablesth(obj):
    return tuple((k, hashablesth(v)) for k, v in sorted(obj.items())) if isinstance(obj, dict) else tuple(hashablesth(x) for x in obj) if isinstance(obj, list) else tuple(sorted(hashablesth(x) for x in obj)) if isinstance(obj, set) else obj


'''dedupkeeporder'''
def dedupkeeporder(seq):
    seen, out = set(), []
    for item in seq: (seen.add(key), out.append(item)) if (key := hashablesth(item)) not in seen else None
    return out


'''searchdictbykey'''
def searchdictbykey(obj, target_key: str | list | tuple | set) -> list:
    results, target_key = [], [target_key] if isinstance(target_key, str) else target_key
    if isinstance(obj, dict):
        for k, v in obj.items(): results += ([v] if k in target_key else []) + searchdictbykey(v, target_key)
    elif isinstance(obj, list):
        for item in obj: results.extend(searchdictbykey(item, target_key))
    return dedupkeeporder(results)


'''ClientProtocolObj'''
class ClientProtocolObj(Protocol):
    default_headers: dict[str, str]
    default_search_headers: dict[str, str]
    default_parse_headers: dict[str, str]
    default_download_headers: dict[str, str]
    default_cookies: dict[str, str]
    default_search_cookies: dict[str, str]
    default_parse_cookies: dict[str, str]
    default_download_cookies: dict[str, str]
    enable_curl_cffi: bool
    enable_search_curl_cffi: bool
    enable_parse_curl_cffi: bool
    enable_download_curl_cffi: bool
    _initsession: Callable[..., Any]


'''Filter, refer to https://github.com/hellock/icrawler/blob/master/icrawler/builtin/filter.py'''
class Filter:
    def __init__(self):
        self.rules = {}
    '''addrule'''
    def addrule(self, name: str, format_fn: Any, choices: Any = None):
        assert callable(format_fn) and (choices is None or isinstance(choices, list) or isinstance(choices, type))
        self.rules[name] = (format_fn, choices)
    '''formatone'''
    def formatone(self, name, val):
        format_fn, choices = self.rules[name]
        if isinstance(choices, type) and not isinstance(val, choices): raise TypeError(f'filter option "{name}" must be a {choices.__name__}, not {type(val).__name__}')
        elif isinstance(choices, list) and val not in choices: raise ValueError('filter option "{}" must be one of the following: {}'.format(name, ", ".join(choices)))
        return format_fn(val)
    '''apply'''
    def apply(self, options, sep: str = ""):
        if options is None or (not isinstance(options, dict)): return ""
        return sep.join([self.formatone(name, val) for name, val in options.items()])


'''ImageExtensionUtils'''
class ImageExtensionUtils():
    PILLOW_FORMAT_TO_EXT = {"JPEG": "jpg", "JPG": "jpg", "PNG": "png", "GIF": "gif", "BMP": "bmp", "WEBP": "webp", "TIFF": "tif", "TIF": "tif", "ICO": "ico", "PPM": "ppm", "PGM": "pgm", "PBM": "pbm", "HEIF": "heif", "HEIC": "heic", "AVIF": "avif", "MPO": "mpo", "DDS": "dds", "PCX": "pcx", "TGA": "tga", "JPEG2000": "jp2"}
    '''extfromimageurlpath'''
    @staticmethod
    def extfromimageurlpath(url: str, image_exts: tuple | list) -> str | None:
        if not url or not isinstance(url, str): return None
        ext_cre = re.compile(r"\.(" + "|".join(image_exts) + r")(?=$|[^\w])", re.IGNORECASE)
        u = url.split("#", 1)[0].split("?", 1)[0].strip()
        try: path = urlsplit(u).path or u
        except Exception: path = u
        if not (path := unquote(path).rstrip("/")): return None
        if not (matches := list(ext_cre.finditer(path.rsplit("/", 1)[-1]))): return None
        ext = matches[-1].group(1).lower()
        return "jpg" if ext == "jpeg" else ("tif" if ext == "tiff" else ext)
    '''normalizeext'''
    @staticmethod
    def normalizeext(ext: Optional[str]) -> Optional[str]:
        if not ext: return None
        ext = ext.lower().strip().lstrip(".")
        return "jpg" if ext == "jpeg" else ("tif" if ext == "tiff" else ext)
    '''readbytesfrompath'''
    @staticmethod
    def readbytesfrompath(path: str | Path) -> bytes:
        with open(str(path), "rb") as fp: return fp.read()
    '''detectimagefile'''
    @staticmethod
    def detectimagefile(image_path: Optional[str | Path] = None, binary_content: Optional[bytes] = None) -> Dict[str, Any]:
        # init
        if image_path is None and binary_content is None: raise ValueError("image_path or binary_content should be given")
        if binary_content is None and image_path is not None: binary_content = ImageExtensionUtils.readbytesfrompath(image_path)
        result = {"ok": False, "ext": None, "detector": None}
        # 1) imghdr
        try:
            ext = imghdr.what(None, h=binary_content) if binary_content is not None else imghdr.what(str(image_path)) if image_path is not None else None
            if (ext := ImageExtensionUtils.normalizeext(ext)) is not None: return {"ok": True, "ext": ext, "detector": "imghdr"}
        except Exception:
            pass
        # 2) filetype
        try:
            kind = filetype.guess(binary_content) if binary_content is not None else filetype.guess(str(image_path)) if image_path is not None else None
            if kind is not None:
                if (getattr(kind, "mime", "") or "").startswith("image/") and ((ext := ImageExtensionUtils.normalizeext(getattr(kind, "extension", None))) is not None):
                    return {"ok": True, "ext": ext, "detector": "filetype"}
        except Exception:
            pass
        # 3) pillow
        try:
            if binary_content is not None:
                with Image.open(BytesIO(binary_content)) as img: fmt = getattr(img, "format", None)
            else:
                with Image.open(str(image_path)) as img: fmt = getattr(img, "format", None)
            ext = ImageExtensionUtils.normalizeext(ImageExtensionUtils.PILLOW_FORMAT_TO_EXT.get(str(fmt).upper()) if fmt else None)
            if ext is not None: return {"ok": True, "ext": ext, "detector": "pillow"}
        except Exception:
            pass
        # 4) failure
        return result