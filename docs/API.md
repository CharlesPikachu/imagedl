# Imagedl APIs

This document describes the main public API for searching and downloading images.

Main components:

- `ImageClient`: the unified high-level interface
- `BaseImageClient`: the base class for lower-level usage and extension
- `ImageClientCMD`: CLI usage

## `ImageClient`

`ImageClient` is the main entry point for searching and downloading images from one or more sources.

Module path:

```python
imagedl.imagedl.ImageClient
```

Constructor:

```python
ImageClient(
    image_sources: list | str = "BaiduImageClient",
    init_image_clients_cfg: dict = None,
    clients_threadings: dict = {},
    requests_overrides: dict = {},
    search_filters: dict = {},
)
```

Arguments:

- **`image_sources`**

  Image sources to enable.
  - Type: `list | str`
  - Default: `"BaiduImageClient"`
  
  Examples:
  ```python
  # str
  image_sources="BaiduImageClient"
  # list
  image_sources=["BaiduImageClient", "BingImageClient"]
  ```
  
  Notes:
  - A string is converted to a one-item list.
  - Invalid source names are ignored.
  - Initialization fails if no valid source remains.

- **`init_image_clients_cfg`**

  Per-source initialization config.
  - Type: `dict`
  
  Example:
  ```python
  init_image_clients_cfg={
    "BaiduImageClient": {"work_dir": "outputs/baidu"},
    "BingImageClient": {"work_dir": "outputs/bing", "max_retries": 8},
  }
  ```
  
  Common fields include:
  - `work_dir`
  - `max_retries`
  - `auto_set_proxies`
  - `random_update_ua`
  - `maintain_session`
  - `disable_print`
  - `default_search_cookies`
  - `default_download_cookies`
  
  Note:  
  - In practice, pass a per-source config dict.

- **`clients_threadings`**

  Per-source thread count used by both search and download.
  - Type: `dict`
  - Default for missing sources: `5`
  
  Example:
  ```python
  clients_threadings={
    "BaiduImageClient": 5,
    "BingImageClient": 8,
  }
  ```  

- **`requests_overrides`**

  Per-source request arguments forwarded to the underlying HTTP requests.
  - Type: `dict`
  - Default for missing sources: `{}`
  
  Typical fields:
  - `timeout`
  - `headers`
  - `proxies`
  - `cookies`
  
  Example:
  ```python
  requests_overrides={
    "BaiduImageClient": {"timeout": 10},
    "BingImageClient": {"timeout": 15},
  }
  ```

- **`search_filters`**

  Per-source search filters.
  - Type: `dict`
  - Default for missing sources: `{}`
  
  Example:
  ```python
  search_filters={
    "BaiduImageClient": {"type": "face", "size": "large"},
    "BingImageClient": {"license": "commercial", "date": "pastmonth"},
  }
  ```
  
  Notes:
  - Supported filter keys depend on the selected source.
  - Unsupported filters may be ignored or rejected by the source implementation.

#### `ImageClient.search()`

Searches images from all configured sources.

```python
ImageClient.search(keyword, search_limits_per_source: int | dict = 1000) -> dict[str, list[ImageInfo]]
```

Arguments:

- **`keyword`**

  Search keyword.
  
  Example:
  ```python
  "golden retriever"
  ```  

- **`search_limits_per_source`**

  Maximum number of results to request from each source.
  
  You can pass either:
  - one integer for all sources, or  
  - one dictionary for per-source limits
  
  Examples:
  ```python
  # int
  results = client.search("dog", search_limits_per_source=30)
  # dict
  results = client.search(
    "dog",
    search_limits_per_source={
        "BaiduImageClient": 30,
        "BingImageClient": 20,
    },
  )
  ```

Returns (A dictionary keyed by source name):

```python
{
  "BaiduImageClient": [ImageInfo, ImageInfo, ...],
  "BingImageClient": [ImageInfo, ImageInfo, ...],
}
```

Behavior:

- Sources are searched concurrently.
- Each source uses its configured thread count from `clients_threadings`.
- Each source uses its own filters and request overrides.
- If one source fails, that source returns an empty list and other sources continue.

Example:

```python
from imagedl.imagedl import ImageClient

client = ImageClient(
    image_sources=["BaiduImageClient", "BingImageClient"],
    init_image_clients_cfg={
        "BaiduImageClient": {"work_dir": "outputs"},
        "BingImageClient": {"work_dir": "outputs"},
    },
    clients_threadings={
        "BaiduImageClient": 5,
        "BingImageClient": 8,
    },
    requests_overrides={
        "BaiduImageClient": {"timeout": 10},
        "BingImageClient": {"timeout": 10},
    },
    search_filters={
        "BaiduImageClient": {"size": "large"},
        "BingImageClient": {"date": "pastmonth"},
    },
)

results = client.search(
    "mountain lake",
    search_limits_per_source={
        "BaiduImageClient": 20,
        "BingImageClient": 20,
    },
)
```
  
#### `ImageClient.download()`

Downloads images returned by `ImageClient.search()`.

```python
ImageClient.download(image_infos: list[ImageInfo] | dict[str, list[ImageInfo]]) -> list[ImageInfo]
```

Arguments:

- **`image_infos`**

  Can be either:
  - a dictionary returned by `ImageClient.search()`, or
  - a flat list of `ImageInfo`
  
  Examples:  
  ```python
  # dict
  downloaded = client.download(results)
  # flat list
  flat_list = results["BaiduImageClient"]
  downloaded = client.download(flat_list)
  ```

Returns (A flat list of successfully downloaded `ImageInfo` objects):

```python
[ImageInfo, ImageInfo, ...]
```

Behavior:

- If a dict is passed in, it is flattened automatically.
- Images are regrouped internally by source before downloading.
- Each source uses its configured thread count and request overrides.

Example:

```python
results = client.search("puppy", search_limits_per_source=20)
downloaded = client.download(results)

print(results.keys())
print(len(downloaded))
```

#### `ImageClient.startcmdui()`

Starts the interactive command-line interface.

Behavior:

- prints basic program information
- asks for a search keyword
- runs `ImageClient.search()`
- immediately runs `ImageClient.download()`

Special inputs:

- `q` or `Q`: quit
- `r` or `R`: restart

Example:

```python
client.startcmdui(search_limits_per_source=50)
```

#### Output Files

After search and download, the code saves metadata as pickle files.

Typical files:

- `search_results.pkl`
- `download_results.pkl`

Images are saved under a timestamped directory similar to:

```text
<work_dir>/<source>/<timestamp> <keyword>/
```

Example:

```text
imagedl_outputs/BaiduImageClient/2026-03-29-10-30-15 cute cat/
```

## `BaseImageClient`

`BaseImageClient` is the base class for lower-level source clients.
It is useful when you want to extend the project or directly control a specific backend including,

- `imagedl.imagedl.modules.sources.BaiduImageClient`
- `imagedl.imagedl.modules.sources.BingImageClient`
- `imagedl.imagedl.modules.sources.DuckduckgoImageClient`
- `imagedl.imagedl.modules.sources.DanbooruImageClient`
- `imagedl.imagedl.modules.sources.DimTownImageClient`
- `imagedl.imagedl.modules.sources.EverypixelImageClient`
- `imagedl.imagedl.modules.sources.FoodiesfeedImageClient`
- `imagedl.imagedl.modules.sources.FreeNatureStockImageClient`
- `imagedl.imagedl.modules.sources.FreeImagesImageClient`
- `imagedl.imagedl.modules.sources.FlickrImageClient`
- `imagedl.imagedl.modules.sources.GoogleImageClient`
- `imagedl.imagedl.modules.sources.GelbooruImageClient`
- `imagedl.imagedl.modules.sources.GratisoGraphyImageClient`
- `imagedl.imagedl.modules.sources.GBIFImageClient`
- `imagedl.imagedl.modules.sources.HuabanImageClient`
- `imagedl.imagedl.modules.sources.I360ImageClient`
- `imagedl.imagedl.modules.sources.INaturalistImageClient`
- `imagedl.imagedl.modules.sources.JikanImageClient`
- `imagedl.imagedl.modules.sources.LifeOfPixImageClient`
- `imagedl.imagedl.modules.sources.LocGovImageClient`
- `imagedl.imagedl.modules.sources.NASAImageClient`
- `imagedl.imagedl.modules.sources.OpenverseImageClient`
- `imagedl.imagedl.modules.sources.PixabayImageClient`
- `imagedl.imagedl.modules.sources.PexelsImageClient`
- `imagedl.imagedl.modules.sources.PicJumboImageClient`
- `imagedl.imagedl.modules.sources.SogouImageClient`
- `imagedl.imagedl.modules.sources.SafebooruImageClient`
- `imagedl.imagedl.modules.sources.StockSnapImageClient`
- `imagedl.imagedl.modules.sources.UnsplashImageClient`
- `imagedl.imagedl.modules.sources.WeiboImageClient`
- `imagedl.imagedl.modules.sources.WikipediaImageClient`
- `imagedl.imagedl.modules.sources.YandexImageClient`
- `imagedl.imagedl.modules.sources.YahooImageClient`
- `imagedl.imagedl.modules.sources.YandeImageClient`

Module path:

```python
imagedl.imagedl.modules.sources.BaseImageClient
```

Constructor:

```python
BaseImageClient(
    auto_set_proxies: bool = False,
    random_update_ua: bool = False,
    enable_search_curl_cffi: bool = False,
    enable_download_curl_cffi: bool = False,
    max_retries: int = 5,
    logger_handle = None,
    maintain_session: bool = False,
    disable_print: bool = False,
    work_dir: str = "imagedl_outputs",
    freeproxy_settings: dict = None,
    default_search_cookies: dict = None,
    default_download_cookies: dict = None,
)
```

Arguments:

- **`work_dir`**

  Root output directory.

- **`max_retries`**

  Maximum retry count for HTTP requests.

- **`auto_set_proxies`**

  Whether to automatically fetch and use proxies.

- **`random_update_ua`**

  Whether to randomize the User-Agent between requests.

- **`maintain_session`**

  Whether to keep a persistent session.

- **`default_search_cookies`**

  Default cookies used for searching.

- **`default_download_cookies`**

  Default cookies used for downloading.

#### `BaseImageClient.search()`

Searches within a single source client.

```python
BaseImageClient.search(
    keyword: str,
    search_limits: int = 1000,
    num_threadings: int = 5,
    filters: dict = None,
    request_overrides: dict = None,
    main_process_context = None,
    main_progress_id = None,
    main_progress_lock = None,
) -> list[ImageInfo]
```

Behavior:

- Returns a list of `ImageInfo`
- Removes duplicate items by identifier
- Assigns output file paths to each result
- Saves search results to `search_results.pkl`

Example:

```python
client = SomeConcreteImageClient(work_dir="outputs")
items = client.search(
    keyword="sunset",
    search_limits=50,
    num_threadings=5,
    filters={},
    request_overrides={"timeout": 10},
)
```

#### `BaseImageClient.download()`

Downloads images for a single source client.

```python
BaseImageClient.download(
    image_infos: list[ImageInfo],
    num_threadings: int = 5,
    request_overrides: dict = None,
) -> list[ImageInfo]
```

Behavior:

- Returns only successfully downloaded items
- Detects file extension automatically
- Saves download results to `download_results.pkl`

Example:

```python
downloaded = client.download(
    image_infos=items,
    num_threadings=8,
    request_overrides={"timeout": 10},
)
```

## `ImageClientCMD` (CLI Usage)

The project also provides a command-line entry.

- Basic command is `imagedl`. If no keyword is provided, interactive mode is opened.

- Search directly from CLI:

  ```bash
  imagedl -k "cute cat"
  ```

- Multi-source Example:

  ```bash
  imagedl -k "mountain lake" \
    -s "BaiduImageClient,BingImageClient" \
    -c '{"BaiduImageClient": {"work_dir": "outputs"}, "BingImageClient": {"work_dir": "outputs"}}' \
    -t '{"BaiduImageClient": 5, "BingImageClient": 8}' \
    -o '{"BaiduImageClient": {"timeout": 10}, "BingImageClient": {"timeout": 10}}' \
    -f '{"BaiduImageClient": {"size": "large"}, "BingImageClient": {"date": "pastmonth"}}' \
    -l 20
  ```

- CLI Options:

  - `-k`, `--keyword`: search keyword
  - `-s`, `--image-sources`: comma-separated source names
  - `-c`, `--init-image-clients-cfg`: JSON string for per-source initialization config
  - `-o`, `--requests-overrides`: JSON string for per-source request overrides
  - `-t`, `--clients-threadings`: JSON string for per-source thread counts
  - `-f`, `--search-filters`: JSON string for per-source filters
  - `-l`, `--search-limits-per-source`: max number of results per source

- Usage Notes:
 
  - Pass a dictionary for `init_image_clients_cfg`.
  - `search()` returns a dict grouped by source.
  - `download()` accepts either that dict or a flat list.
  - Thread counts are configured through `clients_threadings`.
  - Request overrides and filters are configured per source.
  - Supported filter keys depend on the source.

