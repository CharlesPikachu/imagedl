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
  image_sources="BaiduImageClient"
  ```
  ```python
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
  results = client.search("dog", search_limits_per_source=30)
  ```  
  ```python
  results = client.search(
    "dog",
    search_limits_per_source={
        "BaiduImageClient": 30,
        "BingImageClient": 20,
    },
  )
  ```  

Returns:

A dictionary keyed by source name:

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




