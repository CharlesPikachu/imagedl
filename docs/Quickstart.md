# Quick Start

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
    BingImageClient, I360ImageClient, YahooImageClient, BaiduImageClient, SogouImageClient, GoogleImageClient, YandexImageClient, PixabayImageClient, FreeImagesImageClient, PicJumboImageClient,
    DuckduckgoImageClient, UnsplashImageClient, GelbooruImageClient, SafebooruImageClient, DanbooruImageClient, PexelsImageClient, DimTownImageClient, StockSnapImageClient, LifeOfPixImageClient, 
    HuabanImageClient, FoodiesfeedImageClient, EverypixelImageClient, FreeNatureStockImageClient, WeiboImageClient, GratisoGraphyImageClient
)
~~~

To list all image sources supported by your current pyimagedl version:

```bash
python -c "from imagedl.modules import ImageClientBuilder; print(ImageClientBuilder.REGISTERED_MODULES.keys())"
```

Here are some simple examples:

~~~python
from imagedl.modules.sources import (
    BingImageClient, I360ImageClient, YahooImageClient, BaiduImageClient, SogouImageClient, GoogleImageClient, YandexImageClient, PixabayImageClient, FreeImagesImageClient, PicJumboImageClient,
    DuckduckgoImageClient, UnsplashImageClient, GelbooruImageClient, SafebooruImageClient, DanbooruImageClient, PexelsImageClient, DimTownImageClient, StockSnapImageClient, LifeOfPixImageClient, 
    HuabanImageClient, FoodiesfeedImageClient, EverypixelImageClient, FreeNatureStockImageClient, WeiboImageClient, GratisoGraphyImageClient
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
~~~

A good rule is:

- use `imagedl.ImageClient` when you want a unified interface for one or more sources
- use a direct source client when you want the shortest code for one specific source