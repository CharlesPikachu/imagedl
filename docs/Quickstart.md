# Quick Start

#### Uniform ImageClient

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


#### Dedicated ImageClient

Example code for searching and downloading images on different platforms such as Baidu and Google is as follows,

```python
from imagedl.modules.sources.bing import BingImageClient
from imagedl.modules.sources.i360 import I360ImageClient
from imagedl.modules.sources.baidu import BaiduImageClient
from imagedl.modules.sources.sogou import SogouImageClient
from imagedl.modules.sources.google import GoogleImageClient
from imagedl.modules.sources.yandex import YandexImageClient
from imagedl.modules.sources.pixabay import PixabayImageClient
from imagedl.modules.sources.duckduckgo import DuckduckgoImageClient

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
```