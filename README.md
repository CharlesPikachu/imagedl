<div align="center">
  <img src="https://raw.githubusercontent.com/CharlesPikachu/imagedl/main/docs/logo.png" width="600"/>
</div>
<br />

<p align="center">
  <a href="https://imagedl.readthedocs.io/">
    <img src="https://img.shields.io/badge/docs-latest-blue" alt="docs">
  </a>
  <a href="https://pypi.org/project/pyimagedl/">
    <img src="https://img.shields.io/pypi/pyversions/pyimagedl" alt="PyPI - Python Version">
  </a>
  <a href="https://pypi.org/project/pyimagedl/">
    <img src="https://img.shields.io/pypi/v/pyimagedl" alt="PyPI">
  </a>
  <a href="https://github.com/CharlesPikachu/imagedl/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/CharlesPikachu/imagedl.svg" alt="license">
  </a>
  <a href="https://pypi.org/project/pyimagedl/">
    <img src="https://static.pepy.tech/badge/pyimagedl" alt="PyPI - Downloads">
  </a>
  <a href="https://pypi.org/project/pyimagedl/">
    <img src="https://static.pepy.tech/badge/pyimagedl/month" alt="PyPI - Downloads">
  </a>
  <a href="https://github.com/CharlesPikachu/imagedl/issues">
    <img src="https://isitmaintained.com/badge/resolution/CharlesPikachu/imagedl.svg" alt="issue resolution">
  </a>
  <a href="https://github.com/CharlesPikachu/imagedl/issues">
    <img src="https://isitmaintained.com/badge/open/CharlesPikachu/imagedl.svg" alt="open issues">
  </a>
</p>

<p align="center">
  <a href="https://imagedl.readthedocs.io/">
    <strong>📚 Documents: imagedl.readthedocs.io</strong>
  </a>
</p>

<p align="center">
  <a href="https://charlespikachu.github.io/imagedl/">
    <strong>🧪 Online API Health &amp; Demo: charlespikachu.github.io/imagedl</strong>
  </a>
  <br />
  <sub>
    <em>
      Automatically runs daily checks on all registered imagedl modules (search + download)
      via GitHub Actions and visualizes the latest results on this page.
    </em>
  </sub>
  <br /><br />
  <a href="https://charlespikachu.github.io/imagedl/">
    <img
      alt="demo"
      src="https://img.shields.io/badge/demo-online-brightgreen?style=for-the-badge"
    />
  </a>
</p>


# 🆕 What's New

- 2025-11-16: Released pyimagedl v0.2.1 — fixed some minor bugs in duckduckgo and BaseImageClient.
- 2025-11-16: Released pyimagedl v0.2.0 — upgrade ImageClient and fixed some minor bugs.
- 2025-11-10: Released pyimagedl v0.1.8 — fix logging and requirements.
- 2025-10-22: Released pyimagedl v0.1.7 — refactor codes for google and DuckDuckGo, fix base module requests bugs, and add sogou image search.
- 2025-10-22: Released pyimagedl v0.1.6 — fix serpapisearch bugs, more robust code structure, add DuckDuckGo image search.
- 2025-10-21: Released pyimagedl v0.1.5 — fix maintain session bugs, support pixabay and yandex image search.
- 2025-10-20: Released pyimagedl v0.1.4 — add a deduplication feature and support 360 image search.
- 2025-10-19: Released pyimagedl v0.1.3 — code cleanup, deprecated/invalid functions removed, new functions added.


# 📘 Introduction

Imagedl lets you search for and download images from specific websites. If you find it useful, please consider starring the repository to follow updates—thank you for your support!


# 🖼️ Supported Image Client

|  ImageClient (EN)              |  ImageClient (CN)  |   Search           |  Download            |    Code Snippet                                                                                                    |
|  :----:                        |  :----:            |   :----:           |  :----:              |    :----:                                                                                                          |
|  BaiduImageClient              |  百度图片          |   ✓                |  ✓                   |    [baidu.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/baidu.py)                |
|  BingImageClient               |  必应图片          |   ✓                |  ✓                   |    [bing.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/bing.py)                  |
|  GoogleImageClient             |  谷歌图片          |   ✓                |  ✓                   |    [google.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/google.py)              |
|  I360ImageClient               |  360图片           |   ✓                |  ✓                   |    [i360.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/i360.py)                  |
|  PixabayImageClient            |  Pixabay图片       |   ✓                |  ✓                   |    [pixabay.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/pixabay.py)            |
|  YandexImageClient             |  Yandex图片        |   ✓                |  ✓                   |    [yandex.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/yandex.py)              |
|  DuckduckgoImageClient         |  DuckDuckGo图片    |   ✓                |  ✓                   |    [duckduckgo.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/duckduckgo.py)      |
|  SogouImageClient              |  搜狗图片          |   ✓                |  ✓                   |    [sogou.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/sogou.py)                |


# 📦 Install

You have three installation methods to choose from,

```sh
# from pip
pip install pyimagedl
# from github repo method-1
pip install git+https://github.com/CharlesPikachu/imagedl.git@main
# from github repo method-2
git clone https://github.com/CharlesPikachu/imagedl.git
cd imagedl
python setup.py install
```


# ⚡ Quick Start

After a successful installation, you can run the snippet below,

```python
from imagedl import imagedl

image_client = imagedl.ImageClient(image_source='BaiduImageClient')
image_client.startcmdui()
```

Or just run `imagedl` (maybe `imagedl --help` to show usage information) from the terminal.

For class `ImageClient`, the acceptable arguments include,

- `image_source` (`str`, default: `'BaiduImageClient'`): The image search and download source, including `['BaiduImageClient', 'BingImageClient', 'GoogleImageClient', 'I360ImageClient', 'PixabayImageClient', 'YandexImageClient', 'DuckduckgoImageClient', 'SogouImageClient']`.
- `init_image_client_cfg` (`dict`, default: `{}`): Client initialization configuration such as `{'work_dir': 'images', 'max_retries': 5}`.
- `search_limits` (`int`, default: `1000`): Scale of image downloads.
- `num_threadings` (`int`, default: `5`): Number of threads used.
- `request_overrides` (`dict`, default: `{}`): Requests.get (or Requests.post) kwargs such as `{'headers': {'User-Agent': xxx}, 'proxies': {}}`.

The demonstration is as follows,

<div align="center">
  <img src="https://github.com/CharlesPikachu/imagedl/raw/main/docs/screenshot.gif" width="600"/>
</div>
<br />

If you just want to do an image search, you can also do it like this,

```python
from imagedl import imagedl

image_client = imagedl.ImageClient(image_source='DuckduckgoImageClient', search_limits=1000, num_threadings=5)
image_infos = image_client.search('cut animals', search_limits_overrides=10, num_threadings_overrides=1)
print(image_infos)
```

In the code above, `search_limits_overrides` overrides the `search_limits` parameter set when initializing `ImageClient`, and `num_threadings_overrides` works in the same way.
The output of this code looks like,

```python
[
    {
        "candidate_urls": [
            "https://img.freepik.com/.../cut-animal-cartoon-bundle-set_508290-2349.jpg",
            "https://tse2.mm.bing.net/th/id/OIP.vD-8G0MjAMREv1bYbKaqEwHaHa..."
        ],
        "raw_data": {
            "height": 626,
            "width": 626,
            "image": "https://img.freepik.com/.../cut-animal-cartoon-bundle-set_508290-2349.jpg",
            "image_token": "fbff471d31328...",
            "thumbnail": "https://tse2.mm.bing.net/th/id/OIP.vD-8G0MjAMREv1bYbKaqEwHaHa...",
            "thumbnail_token": "4ca07ad2aab9...",
            "source": "Bing",
            "title": "Premium Vector | Cut animal cartoon bundle set",
            "url": "https://www.freepik.com/premium-vector/cut-animal-cartoon-bundle-set_25750969.htm"
        },
        "identifier": "fbff471d31328...",
        "work_dir": "imagedl_outputs\\DuckduckgoImageClient\\2025-11-16-22-34-25 cutanimals",
        "file_path": "imagedl_outputs\\DuckduckgoImageClient\\2025-11-16-22-34-25 cutanimals\\00000001"
    },
    ...
]
```

Then you can also call the image downloading function to download the images found by the search. The code is as follows:

```python
from imagedl import imagedl

image_client = imagedl.ImageClient(image_source='DuckduckgoImageClient', search_limits=1000, num_threadings=5)
image_infos = image_client.search('cut animals', search_limits_overrides=10, num_threadings_overrides=1)
image_client.download(image_infos=image_infos)
```


# 💡 Recommended Projects

- [Games](https://github.com/CharlesPikachu/Games): Create interesting games in pure python.
- [DecryptLogin](https://github.com/CharlesPikachu/DecryptLogin): APIs for loginning some websites by using requests.
- [Musicdl](https://github.com/CharlesPikachu/musicdl): A lightweight music downloader written in pure python.
- [Videodl](https://github.com/CharlesPikachu/videodl): A lightweight video downloader written in pure python.
- [Pytools](https://github.com/CharlesPikachu/pytools): Some useful tools written in pure python.
- [PikachuWeChat](https://github.com/CharlesPikachu/pikachuwechat): Play WeChat with itchat-uos.
- [Pydrawing](https://github.com/CharlesPikachu/pydrawing): Beautify your image or video.
- [ImageCompressor](https://github.com/CharlesPikachu/imagecompressor): Image compressors written in pure python.
- [FreeProxy](https://github.com/CharlesPikachu/freeproxy): Collecting free proxies from internet.
- [Paperdl](https://github.com/CharlesPikachu/paperdl): Search and download paper from specific websites.
- [Sciogovterminal](https://github.com/CharlesPikachu/sciogovterminal): Browse "The State Council Information Office of the People's Republic of China" in the terminal.
- [CodeFree](https://github.com/CharlesPikachu/codefree): Make no code a reality.
- [DeepLearningToys](https://github.com/CharlesPikachu/deeplearningtoys): Some deep learning toys implemented in pytorch.
- [DataAnalysis](https://github.com/CharlesPikachu/dataanalysis): Some data analysis projects in charles_pikachu.
- [Imagedl](https://github.com/CharlesPikachu/imagedl): Search and download images from specific websites.
- [Pytoydl](https://github.com/CharlesPikachu/pytoydl): A toy deep learning framework built upon numpy.
- [NovelDL](https://github.com/CharlesPikachu/noveldl): Search and download novels from some specific websites.


# 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=CharlesPikachu/imagedl&type=date&legend=top-left)](https://www.star-history.com/#CharlesPikachu/imagedl&type=date&legend=top-left)


# 📱 WeChat Official Account (微信公众号):

Charles的皮卡丘 (*Charles_pikachu*)  
![img](https://raw.githubusercontent.com/CharlesPikachu/imagedl/main/docs/pikachu.jpg)