<div align="center">
  <img src="https://raw.githubusercontent.com/CharlesPikachu/imagedl/main/docs/logo.png" width="600"/>
</div>
<br />

<p align="center">
  <a href="https://imagedl.readthedocs.io/">
    <img src="https://img.shields.io/badge/docs-latest-blue" alt="Docs">
  </a>
  <a href="https://pypi.org/project/pyimagedl/">
    <img src="https://img.shields.io/pypi/pyversions/pyimagedl" alt="PyPI - Python Version">
  </a>
  <a href="https://pypi.org/project/pyimagedl/">
    <img src="https://img.shields.io/pypi/v/pyimagedl" alt="PyPI">
  </a>
  <a href="https://github.com/CharlesPikachu/imagedl/blob/main/LICENSE">
    <img src="https://badgen.net/github/license/CharlesPikachu/imagedl" alt="License" >
  </a>
  <a href="https://pypi.org/project/pyimagedl/">
    <img src="https://static.pepy.tech/badge/pyimagedl" alt="PyPI - Downloads (total)">
  </a>
  <a href="https://pypi.org/project/pyimagedl/">
    <img src="https://static.pepy.tech/badge/pyimagedl/month" alt="PyPI - Downloads (month)">
  </a>
  <a href="https://pypi.org/project/pyimagedl/">
    <img src="https://static.pepy.tech/badge/pyimagedl/week" alt="PyPI - Downloads (week)">
  </a>
  <a href="https://github.com/CharlesPikachu/imagedl/actions/workflows/check-imagedl.yml">
    <img src="https://github.com/CharlesPikachu/imagedl/actions/workflows/check-imagedl.yml/badge.svg" alt="Daily Imagedl Check">
  </a>
  <a href="https://github.com/CharlesPikachu/imagedl/issues">
    <img src="https://isitmaintained.com/badge/resolution/CharlesPikachu/imagedl.svg" alt="Issue Resolution">
  </a>
  <a href="https://github.com/CharlesPikachu/imagedl/issues">
    <img src="https://isitmaintained.com/badge/open/CharlesPikachu/imagedl.svg" alt="Open Issues">
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

<p align="center">
  <strong>学习收获更多有趣的内容, 欢迎关注微信公众号：Charles的皮卡丘</strong>
</p>


# 🆕 What's New

- 2026-04-09: Released pyimagedl v0.4.5 — fix a bug where the behavior of maintain session was inconsistent with expectations; add two new image search and download sources, jikan.moe and wiki.
- 2026-04-08: Released pyimagedl v0.4.4 — added support for three new image search and download sites: yande.re, loc.gov, and gbif.org; optimized parts of the code for better IDE hints.
- 2026-04-05: Released pyimagedl v0.4.3 — added search and download functionality for four new image websites, including NASA, iNaturalist, Picjumbo, and Openverse.


# 📘 Introduction

⚡ Imagedl is a lightweight image search and download tool designed for efficient large-scale image collection from specific websites. 
It supports multiple major sources, including Google, Baidu, Bing, 360, Pixabay, Yandex, Sogou, Yahoo, DuckDuckGo, Unsplash, Safebooru, Gelbooru, Danbooru, Huaban, Foodiesfeed, Everypixel, Weibo, and more. 
With support for diverse content such as web images, food, animals, architecture, nature, anime-style artwork, and high-resolution photography, Imagedl is well suited for constructing training and testing datasets for large models. 
If you find it useful, please star the repository ⭐ to support development and keep up with future updates.


# 🖼️ Supported Image Client

|  ImageClient (EN)                                            |  ImageClient (CN)                                         |   Search           |  Download            |    Code Snippet                                                                                                            |
|  :----:                                                      |  :----:                                                   |   :----:           |  :----:              |    :----:                                                                                                                  |
|  [BaiduImageClient](https://image.baidu.com/)                |  [百度图片](https://image.baidu.com/)                     |   ✔️               |  ✔️                  |    [baidu.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/baidu.py)                        |
|  [BingImageClient](https://www.bing.com/images)              |  [必应图片](https://www.bing.com/images)                  |   ✔️               |  ✔️                  |    [bing.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/bing.py)                          |
|  [DuckduckgoImageClient](https://duckduckgo.com/)            |  [DuckDuckGo图片](https://duckduckgo.com/)                |   ✔️               |  ✔️                  |    [duckduckgo.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/duckduckgo.py)              |
|  [DanbooruImageClient](https://danbooru.donmai.us/)          |  [Danbooru动漫图片](https://danbooru.donmai.us/)          |   ✔️               |  ✔️                  |    [danbooru.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/danbooru.py)                  |
|  [DimTownImageClient](https://dimtown.com/home)              |  [次元小镇](https://dimtown.com/home)                     |   ✔️               |  ✔️                  |    [dimtown.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/dimtown.py)                    |
|  [EverypixelImageClient](https://www.everypixel.com/)        |  [Everypixel](https://www.everypixel.com/)                |   ✔️               |  ✔️                  |    [everypixel.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/everypixel.py)              |
|  [FoodiesfeedImageClient](https://www.foodiesfeed.com/)      |  [Foodiesfeed美食图片](https://www.foodiesfeed.com/)      |   ✔️               |  ✔️                  |    [foodiesfeed.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/foodiesfeed.py)            |
|  [FreeNatureStockImageClient](https://freenaturestock.com/)  |  [FreeNatureStock自然图片](https://freenaturestock.com/)  |   ✔️               |  ✔️                  |    [freenaturestock.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/freenaturestock.py)    |
|  [FreeImagesImageClient](https://www.freeimages.com/)        |  [Freeimages](https://www.freeimages.com/)                |   ✔️               |  ✔️                  |    [freeimages.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/freeimages.py)              |
|  [GoogleImageClient](https://images.google.com/)             |  [谷歌图片](https://images.google.com/)                   |   ✔️               |  ✔️                  |    [google.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/google.py)                      |
|  [GelbooruImageClient](https://gelbooru.com/)                |  [Gelbooru动漫图片](https://gelbooru.com/)                |   ✔️               |  ✔️                  |    [gelbooru.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/gelbooru.py)                  |
|  [GratisoGraphyImageClient](https://gratisography.com/)      |  [GratisoGraphy创意图片网站](https://gratisography.com/)  |   ✔️               |  ✔️                  |    [gratisography.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/gratisography.py)        |
|  [GBIFImageClient](https://www.gbif.org/)                    |  [全球生物多样性物种图库](https://www.gbif.org/)          |   ✔️               |  ✔️                  |    [gbif.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/gbif.py)                          |
|  [HuabanImageClient](https://huaban.com/)                    |  [花瓣网](https://huaban.com/)                            |   ✔️               |  ✔️                  |    [huaban.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/huaban.py)                      |
|  [I360ImageClient](https://image.so.com/)                    |  [360图片](https://image.so.com/)                         |   ✔️               |  ✔️                  |    [i360.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/i360.py)                          |
|  [INaturalistImageClient](https://www.inaturalist.org/)      |  [iNaturalist物种数据库](https://www.inaturalist.org/)    |   ✔️               |  ✔️                  |    [inaturalist.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/inaturalist.py)            |
|  [JikanImageClient](https://jikan.moe/)                      |  [Jikan动漫角色图](https://jikan.moe/)                    |   ✔️               |  ✔️                  |    [jikan.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/jikan.py)                        |
|  [LifeOfPixImageClient](https://www.lifeofpix.com/)          |  [LifeOfPix](https://www.lifeofpix.com/)                  |   ✔️               |  ✔️                  |    [lifeofpix.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/lifeofpix.py)                |
|  [LocGovImageClient](https://www.loc.gov/)                   |  [美国国会图书馆](https://www.loc.gov/)                   |   ✔️               |  ✔️                  |    [locgov.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/locgov.py)                      |
|  [NASAImageClient](https://www.nasa.gov/)                    |  [NASA](https://www.nasa.gov/)                            |   ✔️               |  ✔️                  |    [nasa.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/nasa.py)                          |
|  [OpenverseImageClient](https://openverse.org/)              |  [Openverse](https://openverse.org/)                      |   ✔️               |  ✔️                  |    [openverse.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/openverse.py)                |
|  [PixabayImageClient](https://pixabay.com/zh/photos/)        |  [Pixabay高清图片](https://pixabay.com/zh/photos/)        |   ✔️               |  ✔️                  |    [pixabay.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/pixabay.py)                    |
|  [PexelsImageClient](https://www.pexels.com/zh-cn/)          |  [Pexels高清图片](https://www.pexels.com/zh-cn/)          |   ✔️               |  ✔️                  |    [pexels.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/pexels.py)                      |
|  [PicJumboImageClient](https://picjumbo.com/)                |  [PicJumbo免费高清图库](https://picjumbo.com/)            |   ✔️               |  ✔️                  |    [picjumbo.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/picjumbo.py)                  |
|  [SogouImageClient](https://pic.sogou.com/)                  |  [搜狗图片](https://pic.sogou.com/)                       |   ✔️               |  ✔️                  |    [sogou.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/sogou.py)                        |
|  [SafebooruImageClient](https://safebooru.org/)              |  [Safebooru动漫图片](https://safebooru.org/)              |   ✔️               |  ✔️                  |    [safebooru.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/safebooru.py)                |
|  [StockSnapImageClient](https://stocksnap.io/)               |  [StockSnap.io](https://stocksnap.io/)                    |   ✔️               |  ✔️                  |    [stocksnap.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/stocksnap.py)                |
|  [UnsplashImageClient](https://unsplash.com/)                |  [Unsplash图片](https://unsplash.com/)                    |   ✔️               |  ✔️                  |    [unsplash.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/unsplash.py)                  |
|  [WeiboImageClient](https://m.weibo.cn/)                     |  [微博图片](https://m.weibo.cn/)                          |   ✔️               |  ✔️                  |    [weibo.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/weibo.py)                        |
|  [WikipediaImageClient](https://en.wikipedia.org/wiki/Wiki)  |  [维基百科](https://en.wikipedia.org/wiki/Wiki)           |   ✔️               |  ✔️                  |    [wikipedia.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/wikipedia.py)                |
|  [YandexImageClient](https://yandex.com/images/)             |  [Yandex图片](https://yandex.com/images/)                 |   ✔️               |  ✔️                  |    [yandex.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/yandex.py)                      |
|  [YahooImageClient](https://images.search.yahoo.com/)        |  [雅虎图片](https://images.search.yahoo.com/)             |   ✔️               |  ✔️                  |    [yahoo.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/yahoo.py)                        |
|  [YandeImageClient](https://yande.re/post)                   |  [Yande.re二次元原画](https://yande.re/post)              |   ✔️               |  ✔️                  |    [yande.py](https://github.com/CharlesPikachu/imagedl/blob/main/imagedl/modules/sources/yande.py)                        |


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

Please note that some image sources need to be crawled using [DrissionPage](https://www.drissionpage.cn/), such as `EverypixelImageClient` and `GoogleImageClient`. 
If DrissionPage cannot find a suitable browser in the current environment, it will automatically download the latest compatible beta version of Google Chrome for the current system. 
So if you notice that the program is downloading a browser, there is no need to be overly concerned.


# ⚡ Quick Start

`imagedl` is built around `imagedl.ImageClient`. 

In the current implementation, `ImageClient` accepts one or more sources through `image_sources`, and lets you configure each source with `init_image_clients_cfg`, `clients_threadings`, `requests_overrides`, and `search_filters`. 

When no source is specified, the default source is `BaiduImageClient`.

#### The simplest working example

Start with one source like `"BaiduImageClient"` and `"BingImageClient"` and a small search limit. This is the easiest way to confirm that your environment is set up correctly.

~~~python
import random
from imagedl import imagedl

client = imagedl.ImageClient(image_sources=["BaiduImageClient"], init_image_clients_cfg={})
search_results = client.search(keyword="cute cats", search_limits_per_source=10)
downloaded_results = client.download(image_infos=search_results)

print(f"found {sum(len(v) for v in search_results.values())} items")
print(f"downloaded {len(downloaded_results)} items")
print('random example >>> ')
print(random.choice(downloaded_results))
~~~

In the current API, `search()` returns a dictionary whose keys are source names and whose values are lists of `ImageInfo` objects. The updated `download()` method can now accept either:

- the original dictionary returned by `search()`
- a flat list of `ImageInfo` objects

So the normal workflow is now simply: *search -> download*

#### CLI options

The package also defines a command-line interface with these main options:

```bash
Usage: imagedl [OPTIONS]

Options:
  --version                       Show the version and exit.
  -k, --keyword TEXT              The keywords for the image search. If left
                                  empty, an interactive terminal will open
                                  automatically.
  -s, --image-sources, --image_sources TEXT
                                  The image search and download sources.
                                  [default: BaiduImageClient]
  -c, --init-image-clients-cfg, --init_image_clients_cfg TEXT
                                  Config such as `work_dir` for each image
                                  client as a JSON string.
  -o, --requests-overrides, --requests_overrides TEXT
                                  Requests.get / Requests.post kwargs such as
                                  `headers` and `proxies` for each image
                                  client as a JSON string.
  -t, --clients-threadings, --clients_threadings TEXT
                                  Number of threads used for each image client
                                  as a JSON string.
  -f, --search-filters, --search_filters TEXT
                                  Search filters for each image client as a
                                  JSON string.
  -l, --search-limits-per-source, --search_limits_per_source INTEGER RANGE
                                  Scale of image downloads.  [default: 1000;
                                  1<=x<=100000000.0]
  --help                          Show this message and exit.
```

The demonstration of running `imagedl -k "猫咪" -s "BaiduImageClient" -l 1000` is as follows,

<div align="center">
  <img src="https://github.com/CharlesPikachu/imagedl/raw/main/docs/screenshot.gif" width="600"/>
</div>
<br />

#### What happens during search and download

Each source searches independently, using its own thread count, request overrides, and filters. 
During searching, duplicate items are removed, and each result is assigned a unique save path automatically. 
During downloading, the package groups results by source, tries the candidate image URLs one by one, detects the real file extension from the downloaded content, and then saves the file.

#### Where files are saved

By default, files are saved under `imagedl_outputs`. The actual folder structure is:

~~~text
imagedl_outputs/
  <SourceName>/
    <timestamp> <keyword>/
      00000001.<ext>
      00000002.<ext>
      ...
      search_results.pkl
      download_results.pkl
~~~

The search stage writes `search_results.pkl`, and the download stage writes `download_results.pkl`. 
Image filenames are numbered automatically, and the extension is added after the file content is successfully recognized.

#### Main arguments of `ImageClient`

The most important arguments are:

- `image_sources`: a string or list of source names, such as `"BaiduImageClient"` or `["BaiduImageClient", "DuckduckgoImageClient"]`
- `init_image_clients_cfg`: per-source initialization settings such as `work_dir`, `max_retries`, `maintain_session`, `cookies`, and curl-cffi-related options
- `clients_threadings`: per-source thread counts used for search and download
- `requests_overrides`: per-source request arguments such as custom headers or proxies
- `search_filters`: per-source filter settings
- `search_limits_per_source`: the number of images to search for each source when calling `search()`

Internally, each source is initialized with defaults such as `work_dir="imagedl_outputs"`, `max_retries=5`, `maintain_session=False`, `auto_set_proxies=False`, `random_update_ua=False`, `logger_handle=LoggerHandle()` and disabled curl-cffi options unless you override them.

#### Save images to a custom folder

You can set a different output folder for each source through `init_image_clients_cfg`.

~~~python
from imagedl import imagedl

client = imagedl.ImageClient(
    image_sources=["BaiduImageClient"],
    init_image_clients_cfg={
        "BaiduImageClient": {
            "work_dir": "my_images",
            "max_retries": 8
        }
    }
)

search_results = client.search("sunset beach", search_limits_per_source=10)
client.download(image_infos=search_results)
~~~

This is the recommended way to control where your files are saved.

#### Search from multiple sources

You can search several sources at once. In that case, it is usually best to configure thread count and output directory per source.
Here is a simple example:

~~~python
from imagedl import imagedl

client = imagedl.ImageClient(
    image_sources=["BaiduImageClient", "DuckduckgoImageClient"],
    init_image_clients_cfg={
        "BaiduImageClient": {"work_dir": "outputs/baidu"},
        "DuckduckgoImageClient": {"work_dir": "outputs/ddg"}
    },
    clients_threadings={
        "BaiduImageClient": 4,
        "DuckduckgoImageClient": 4
    }
)

search_results = client.search(
    keyword="golden retriever",
    search_limits_per_source={
        "BaiduImageClient": 10,
        "DuckduckgoImageClient": 10
    }
)

client.download(image_infos=search_results)
~~~

When `search_limits_per_source` is a single number, that same limit is applied to every source. When it is a dictionary, each source uses its own limit.

#### Add request headers or proxies

Use `requests_overrides` when you need custom headers, cookies, or proxies for a specific source.

~~~python
from imagedl import imagedl

client = imagedl.ImageClient(
    image_sources=["BaiduImageClient"],
    init_image_clients_cfg={},
    requests_overrides={
        "BaiduImageClient": {
            "headers": {
                "User-Agent": "Mozilla/5.0"
            },
            "proxies": {
                "http": "http://127.0.0.1:7890",
                "https": "http://127.0.0.1:7890"
            }
        }
    }
)

search_results = client.search("mountains", search_limits_per_source=5)
client.download(image_infos=search_results)
~~~

The package forwards these values to the underlying request calls for that source.

#### A simple way to use one source directly

If you only want to test or use a single website, you can import a concrete source client directly from `imagedl.modules.sources`. This is a very simple and beginner-friendly way to start.

~~~python
from imagedl.modules.sources import BaiduImageClient

client = BaiduImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
~~~

In this direct-source style:

- `search()` returns a list of `ImageInfo` objects
- `download()` takes that list directly
- you do not need `imagedl.ImageClient`
- you do not need to pass `image_sources`

This style is convenient when you only care about one source and want the shortest possible code.

You can choose from many built-in source clients:

~~~python
from imagedl.modules.sources import (
    BingImageClient, I360ImageClient, YahooImageClient, BaiduImageClient, SogouImageClient, GoogleImageClient, YandexImageClient, PixabayImageClient, FreeImagesImageClient, PicJumboImageClient, EverypixelImageClient,
    DuckduckgoImageClient, UnsplashImageClient, GelbooruImageClient, SafebooruImageClient, DanbooruImageClient, PexelsImageClient, DimTownImageClient, StockSnapImageClient, LifeOfPixImageClient, OpenverseImageClient, 
    FoodiesfeedImageClient, FreeNatureStockImageClient, WeiboImageClient, GratisoGraphyImageClient, INaturalistImageClient, NASAImageClient, HuabanImageClient, GBIFImageClient, LocGovImageClient, WikipediaImageClient,
	YandeImageClient, JikanImageClient
)
~~~

To list all image sources supported by your current pyimagedl version:

```bash
python -c "from imagedl.modules import ImageClientBuilder; print(ImageClientBuilder.REGISTERED_MODULES.keys())"
```

Here are some simple examples:

~~~python
from imagedl.modules.sources import (
    BingImageClient, I360ImageClient, YahooImageClient, BaiduImageClient, SogouImageClient, GoogleImageClient, YandexImageClient, PixabayImageClient, FreeImagesImageClient, PicJumboImageClient, EverypixelImageClient,
    DuckduckgoImageClient, UnsplashImageClient, GelbooruImageClient, SafebooruImageClient, DanbooruImageClient, PexelsImageClient, DimTownImageClient, StockSnapImageClient, LifeOfPixImageClient, OpenverseImageClient, 
    FoodiesfeedImageClient, FreeNatureStockImageClient, WeiboImageClient, GratisoGraphyImageClient, INaturalistImageClient, NASAImageClient, HuabanImageClient, GBIFImageClient, LocGovImageClient, WikipediaImageClient,
	YandeImageClient, JikanImageClient
)

# bing
client = BingImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# 360
client = I360ImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# baidu
client = BaiduImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# sogou
client = SogouImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# google
client = GoogleImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# yandex
client = YandexImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# pixabay
client = PixabayImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# duckduckgo
client = DuckduckgoImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# yahoo
client = YahooImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# unsplash
client = UnsplashImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# gelbooru
client = GelbooruImageClient()
image_infos = client.search('pikachu', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# safebooru
client = SafebooruImageClient()
image_infos = client.search('pikachu', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# danbooru
client = DanbooruImageClient()
image_infos = client.search('pikachu', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# pexels
client = PexelsImageClient()
image_infos = client.search('animals', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# dimtown
client = DimTownImageClient()
image_infos = client.search('JK', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# huaban
client = HuabanImageClient()
image_infos = client.search('JK', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# foodiesfeed
client = FoodiesfeedImageClient()
image_infos = client.search('pizza', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# everypixel
client = EverypixelImageClient()
image_infos = client.search('animals', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# freenaturestock
client = FreeNatureStockImageClient()
image_infos = client.search('mountains', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# weibo (cookies required)
client = WeiboImageClient(default_search_cookies='xxxx')
image_infos = client.search('animals', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# stocksnap 
client = StockSnapImageClient()
image_infos = client.search('mountains', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# freeimages 
client = FreeImagesImageClient()
image_infos = client.search('mountains', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# lifeofpix 
client = LifeOfPixImageClient()
image_infos = client.search('mountains', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# gratisography 
client = GratisoGraphyImageClient()
image_infos = client.search('mountains', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# picjumbo 
client = PicJumboImageClient()
image_infos = client.search('mountains', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# openverse 
client = OpenverseImageClient()
image_infos = client.search('pikachu', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# inaturalist
client = INaturalistImageClient()
image_infos = client.search('Red Panda', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# nasa
client = NASAImageClient()
image_infos = client.search('James Webb', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# gbif
client = GBIFImageClient()
image_infos = client.search('jellyfish', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# loc.gov
client = LocGovImageClient()
image_infos = client.search('apollo 11', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# yande
client = YandeImageClient()
image_infos = client.search('pikachu', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# wiki
client = WikipediaImageClient()
image_infos = client.search('pikachu', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)

# jikan
client = JikanImageClient()
image_infos = client.search('pikachu', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
~~~

A good rule is:

- use `imagedl.ImageClient` when you want a unified interface for one or more sources
- use a direct source client when you want the shortest code for one specific source


# 💡 Recommended Projects

| Project                                                    | ⭐ Stars                                                                                                                                               | 📦 Version                                                                                                 | ⏱ Last Update                                                                                                                                                                   | 🛠 Repository                                                        |
| -------------                                              | ---------                                                                                                                                             | -----------                                                                                                | ----------------                                                                                                                                                                 | --------                                                             |
| 🎵 **Musicdl**<br/>轻量级无损音乐下载器                    | [![Stars](https://img.shields.io/github/stars/CharlesPikachu/musicdl?style=flat-square)](https://github.com/CharlesPikachu/musicdl)                   | [![Version](https://img.shields.io/pypi/v/musicdl)](https://pypi.org/project/musicdl)                      | [![Last Commit](https://img.shields.io/github/last-commit/CharlesPikachu/musicdl?style=flat-square)](https://github.com/CharlesPikachu/musicdl/commits/master)                   | [🛠 Repository](https://github.com/CharlesPikachu/musicdl)           |
| 🎬 **Videodl**<br/>轻量级高清无水印视频下载器              | [![Stars](https://img.shields.io/github/stars/CharlesPikachu/videodl?style=flat-square)](https://github.com/CharlesPikachu/videodl)                   | [![Version](https://img.shields.io/pypi/v/videofetch)](https://pypi.org/project/videofetch)                | [![Last Commit](https://img.shields.io/github/last-commit/CharlesPikachu/videodl?style=flat-square)](https://github.com/CharlesPikachu/videodl/commits/master)                   | [🛠 Repository](https://github.com/CharlesPikachu/videodl)           |
| 🖼️ **Imagedl**<br/>轻量级海量图片搜索下载器                | [![Stars](https://img.shields.io/github/stars/CharlesPikachu/imagedl?style=flat-square)](https://github.com/CharlesPikachu/imagedl)                   | [![Version](https://img.shields.io/pypi/v/pyimagedl)](https://pypi.org/project/pyimagedl)                  | [![Last Commit](https://img.shields.io/github/last-commit/CharlesPikachu/imagedl?style=flat-square)](https://github.com/CharlesPikachu/imagedl/commits/main)                     | [🛠 Repository](https://github.com/CharlesPikachu/imagedl)           |
| 🌐 **FreeProxy**<br/>全球海量高质量免费代理采集器          | [![Stars](https://img.shields.io/github/stars/CharlesPikachu/freeproxy?style=flat-square)](https://github.com/CharlesPikachu/freeproxy)               | [![Version](https://img.shields.io/pypi/v/pyfreeproxy)](https://pypi.org/project/pyfreeproxy)              | [![Last Commit](https://img.shields.io/github/last-commit/CharlesPikachu/freeproxy?style=flat-square)](https://github.com/CharlesPikachu/freeproxy/commits/master)               | [🛠 Repository](https://github.com/CharlesPikachu/freeproxy)         |
| 🌐 **MusicSquare**<br/>简易音乐搜索下载和播放网页          | [![Stars](https://img.shields.io/github/stars/CharlesPikachu/musicsquare?style=flat-square)](https://github.com/CharlesPikachu/musicsquare)           | [![Version](https://img.shields.io/pypi/v/musicdl)](https://pypi.org/project/musicdl)                      | [![Last Commit](https://img.shields.io/github/last-commit/CharlesPikachu/musicsquare?style=flat-square)](https://github.com/CharlesPikachu/musicsquare/commits/main)             | [🛠 Repository](https://github.com/CharlesPikachu/musicsquare)       |
| 🌐 **FreeGPTHub**<br/>真正免费的GPT统一接口                | [![Stars](https://img.shields.io/github/stars/CharlesPikachu/FreeGPTHub?style=flat-square)](https://github.com/CharlesPikachu/FreeGPTHub)             | [![Version](https://img.shields.io/pypi/v/freegpthub)](https://pypi.org/project/freegpthub)                | [![Last Commit](https://img.shields.io/github/last-commit/CharlesPikachu/FreeGPTHub?style=flat-square)](https://github.com/CharlesPikachu/FreeGPTHub/commits/main)               | [🛠 Repository](https://github.com/CharlesPikachu/FreeGPTHub)        |


# 📚 Citation

If you use this project in your research, please cite the repository.

```
@misc{imagedl2022,
    author = {Zhenchao Jin},
    title = {Imagedl: Search and download images from specific websites},
    year = {2022},
    publisher = {GitHub},
    journal = {GitHub repository},
    howpublished = {\url{https://github.com/CharlesPikachu/imagedl/}},
}
```


# 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=CharlesPikachu/imagedl&type=date&legend=top-left)](https://www.star-history.com/#CharlesPikachu/imagedl&type=date&legend=top-left)


# ☕ Appreciation (赞赏 / 打赏)

| WeChat Appreciation QR Code (微信赞赏码)                                                                                       | Alipay Appreciation QR Code (支付宝赞赏码)                                                                                     |
| :--------:                                                                                                                     | :----------:                                                                                                                   |
| <img src="https://raw.githubusercontent.com/CharlesPikachu/imagedl/main/.github/pictures/wechat_reward.jpg" width="260" />     | <img src="https://raw.githubusercontent.com/CharlesPikachu/imagedl/main/.github/pictures/alipay_reward.png" width="260" />     |


# 📱 WeChat Official Account (微信公众号):

Charles的皮卡丘 (*Charles_pikachu*)  
![img](https://raw.githubusercontent.com/CharlesPikachu/imagedl/main/docs/pikachu.jpg)