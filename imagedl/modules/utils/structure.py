'''
Function:
    Implementation of ImageInfo
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import uuid
from typing import Any, Dict
from dataclasses import dataclass, field


'''ImageInfo'''
@dataclass
class ImageInfo:
    source: str = ""
    raw_data: Any = None
    download_url: str = ""
    candidate_download_urls: list[str] = field(default_factory=list)
    description: str = ""
    identifier: str = ""
    work_dir: str = "./"
    ext: str = "jpg"
    save_name: str = f"{str(uuid.uuid4())}.jpg"
    save_path: str = os.path.join(work_dir, save_name)
    ext_detect_result: Dict[str, Any] = field(default_factory=dict)
    download_headers: Dict[str, Any] = field(default_factory=dict)
    download_cookies: Dict[str, Any] = field(default_factory=dict)
    extra: Dict[str, Any] = field(default_factory=dict)
    '''corefields'''
    @classmethod
    def corefields(cls) -> set[str]: return set(cls.__dataclass_fields__.keys()) - {"extra"}
    '''getitem'''
    def __getitem__(self, key: str) -> Any:
        if key in self.corefields(): return getattr(self, key)
        if key in self.extra: return self.extra[key]
        raise KeyError(key)
    '''setitem'''
    def __setitem__(self, key: str, value: Any) -> None:
        if key in self.corefields(): setattr(self, key, value)
        else: self.extra[key] = value
    '''getattr'''
    def __getattr__(self, name: str) -> Any:
        if "extra" in self.__dict__ and name in self.extra: return self.extra[name]
        raise AttributeError(f"{self.__class__.__name__!r} object has no attribute {name!r}")
    '''setattr'''
    def __setattr__(self, name: str, value: Any) -> None:
        core = set(type(self).__dataclass_fields__.keys())
        if name in core: object.__setattr__(self, name, value)
        else:
            if "extra" not in self.__dict__: object.__setattr__(self, "extra", {})
            self.extra[name] = value
    '''todict'''
    def todict(self) -> Dict[str, Any]:
        (data := {k: getattr(self, k) for k in self.corefields()}).update(self.extra)
        return data
    '''fromdict'''
    @classmethod
    def fromdict(cls, data: Dict[str, Any]) -> "ImageInfo":
        core = cls.corefields()
        core_data = {k: data[k] for k in data if k in core}
        extra_data = {k: data[k] for k in data if k not in core}
        obj = cls(**core_data); obj.extra.update(extra_data)
        return obj