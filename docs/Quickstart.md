# Quick Start

After installing imagedl, you can use the following few lines of code to quickly get started with it,

```python
from imagedl import imagedl

image_client = imagedl.ImageClient(image_source='BaiduImageClient')
image_client.startcmdui()
```

where `image_source` is used to specify the image search and download engine.
Of course, you can equivalently enter `imagedl -i "BaiduImageClient"` in the terminal to execute the above code.
`imagedl --help` displays the basic usage of the command-line tool.

```bash
Usage: imagedl [OPTIONS]

Options:
  --version                       Show the version and exit.
  -k, --keyword TEXT              The keywords for the image search. If left
                                  empty, an interactive terminal will open
                                  automatically.
  -i, --image-source, --image_source [bingimageclient|baiduimageclient|googleimageclient|i360imageclient|pixabayimageclient|yandeximageclient|duckduckgoimageclient|sogouimageclient|yahooimageclient|unsplashimageclient|danbooruimageclient|safebooruimageclient|gelbooruimageclient|pexelsimageclient|huabanimageclient]
                                  The image search and download source.
                                  [default: BaiduImageClient]
  -s, --search-limits, --search_limits INTEGER RANGE
                                  Scale of image downloads.  [default: 1000;
                                  1<=x<=100000000.0]
  -n, --num-threadings, --num_threadings INTEGER RANGE
                                  Number of threads used.  [default: 5;
                                  1<=x<=256]
  -c, --init-image-client-cfg, --init_image_client_cfg TEXT
                                  Client config such as `work_dir` as a JSON
                                  string.
  -r, --request-overrides, --request_overrides TEXT
                                  Requests.get (or Requests.post) kwargs such
                                  as `headers` and `proxies` as a JSON string.
  --help                          Show this message and exit.
```

For class `imagedl.ImageClient`, the acceptable arguments include,

- `image_source` (`str`, default: `'BaiduImageClient'`): The image search and download source, including `['BaiduImageClient', 'BingImageClient', 'GoogleImageClient', 'I360ImageClient', 'PixabayImageClient', 'YandexImageClient', 'DuckduckgoImageClient', 'SogouImageClient', 'YahooImageClient', 'UnsplashImageClient', 'GelbooruImageClient', 'SafebooruImageClient', 'DanbooruImageClient', 'PexelsImageClient', 'HuabanImageClient']`.
- `init_image_client_cfg` (`dict`, default: `{}`): Client initialization configuration such as `{'work_dir': 'images', 'max_retries': 5}`.
- `search_limits` (`int`, default: `1000`): Scale of image downloads.
- `num_threadings` (`int`, default: `5`): Number of threads used.
- `request_overrides` (`dict`, default: `{}`): `requests.get` (or `requests.post`) kwargs such as `{'headers': {'User-Agent': xxx}, 'proxies': {}}`.

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

In the code above, `search_limits_overrides` overrides the `search_limits` argument set when initializing `imagedl.ImageClient`, and `num_threadings_overrides` works in the same way.
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

Then you can also call the image downloading function to download the images found by the search. The code is as follows,

```python
from imagedl import imagedl

image_client = imagedl.ImageClient(image_source='DuckduckgoImageClient', search_limits=1000, num_threadings=5)
image_infos = image_client.search('cut animals', search_limits_overrides=10, num_threadings_overrides=1)
image_client.download(image_infos=image_infos)
```

If you prefer not to use the unified interface, you can also import a specific image search engine directly, as in the following code,

```python
from imagedl.modules.sources import (
    BingImageClient, I360ImageClient, YahooImageClient, BaiduImageClient, SogouImageClient, GoogleImageClient, YandexImageClient, PixabayImageClient, 
    DuckduckgoImageClient, UnsplashImageClient, GelbooruImageClient, SafebooruImageClient, DanbooruImageClient, PexelsImageClient, DimTownImageClient,
    HuabanImageClient
)

# bing tests
client = BingImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# 360 tests
client = I360ImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# baidu tests
client = BaiduImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# sogou tests
client = SogouImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# google tests
client = GoogleImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# yandex tests
client = YandexImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# pixabay tests
client = PixabayImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# duckduckgo tests
client = DuckduckgoImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# yahoo tests
client = YahooImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# unsplash tests
client = UnsplashImageClient()
image_infos = client.search('Cute Dogs', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# gelbooru tests
client = GelbooruImageClient()
image_infos = client.search('pikachu', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# safebooru tests
client = SafebooruImageClient()
image_infos = client.search('pikachu', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# danbooru tests
client = DanbooruImageClient()
image_infos = client.search('pikachu', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# pexels tests
client = PexelsImageClient()
image_infos = client.search('animals', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# dimtown tests 
client = DimTownImageClient()
image_infos = client.search('JK', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
# huaban tests 
client = HuabanImageClient()
image_infos = client.search('JK', search_limits=10, num_threadings=1)
client.download(image_infos, num_threadings=1)
```