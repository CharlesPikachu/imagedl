# Imagedl APIs

## `imagedl.imagedl.ImageClient`

`ImageClient` is a high-level interface for searching and downloading images using different backends (*e.g.*, `BaiduImageClient`, `BingImageClient` and `GoogleImageClient`) registered in `ImageClientBuilder.REGISTERED_MODULES`.
Arguments supported when initializing this class include:

- **image_source** (`str`, default: `BaiduImageClient`): Name of the image client backend to use. Must be one of the registered modules in `ImageClientBuilder.REGISTERED_MODULES`.

- **init_image_client_cfg** (`dict` or `None`, default: `None`): Extra configuration passed to the underlying image client on initialization. It is merged into a default config:
  ```python
  default_image_client_cfg = {
    "work_dir": "imagedl_outputs",
    "logger_handle": ImageClient.logger_handle,
    "type": image_source,
    "auto_set_proxies": False,
    "random_update_ua": False,
    "enable_search_curl_cffi": False,
    "enable_download_curl_cffi": False,
    "max_retries": 5,
    "maintain_session": False,
    "disable_print": False,
    "freeproxy_settings": None,
    "default_search_cookies": None,
    "default_download_cookies": None,
  }
  ```

- **search_limits** (`int`, default: `1000`): Default maximum number of images to retrieve per search. Can be overridden per call in `ImageClient.search()`.

- **num_threadings** (`int`, default: `5`): Default number of threads to use for network requests and downloads. Can be overridden per call in `ImageClient.search()` and `ImageClient.download()`.

- **request_overrides** (`dict` or `None`, default: `None`): Extra keyword arguments forwarded to `requests.get` in the underlying image client, e.g., `proxies` and `timeout`.
  These are stored and passed to both `ImageClient.search()` and `ImageClient.download()` unless overridden inside the backend.

#### `ImageClient.startcmdui`

Start an interactive command-line interface (CLI) for searching and downloading images. Intended mainly for end users running `imagedl` from the terminal.

Behavior:

- Repeatedly:
  - Prints a banner with basic information (version, work dir, usage help).
  - Prompts the user for a search keyword:  
    "Please enter keywords for the image search:"
- Special inputs:
  - `q` / `Q`: exit the program.
  - `r` / `R`: restart and return to the main menu.
- Any other input is treated as a search keyword:
  - Calls the underlying backend’s `search()`:
    - `keyword` = user input
    - `search_limits` = `ImageClient.search_limits`
    - `num_threadings` = `ImageClient.num_threadings`
    - `request_overrides` = `ImageClient.request_overrides`
  - Immediately calls the backend’s `download()` on the search results.

Example (CLI usage):

    python -m imagedl.imagedl

#### `ImageClient.search`

Perform an image search programmatically using the configured backend. This method only retrieves metadata; it does NOT download any images.

Arguments:

- **keyword** (`str`): The search query string, e.g. `"Eiffel Tower"`, `"golden retriever"`.

- **search_limits_overrides** (`int | None`, default: `None`): Per-call maximum number of images to retrieve. If `None`, falls back to `ImageClient.search_limits`.

- **num_threadings_overrides** (`int | None`, default: `None`): Per-call override for the number of threads. If `None`, falls back to `ImageClient.num_threadings`.

- **filters** (`dict | None`, default: `None`): Optional filter configuration passed directly to the backend (*e.g.*, image size, color, type), if supported by the chosen `image_source`.

Returns:

- `list`: A list of image metadata objects (backend-defined structure) that can be passed directly to `ImageClient.download()`.

Example:

    from imagedl.imagedl import ImageClient

    client = ImageClient(
        image_source="BaiduImageClient", search_limits=200, num_threadings=10,
    )

    image_infos = client.search(
        keyword="cute cat", search_limits_overrides=50,
    )

#### `ImageClient.download`

Download images from a list of image metadata entries, typically returned by `ImageClient.search()`.

Arguments:

- **image_infos** (`list`): A list of image metadata objects returned by `ImageClient.search()`. Each entry must contain enough information (e.g. URL) for the backend to download the corresponding image.

- **num_threadings_overrides** (`int | None`, default: `None`): Per-call override for the number of threads used for downloading. If `None`, falls back to `ImageClient.num_threadings`.

Returns:

- `list`: A list of image metadata objects (backend-defined structure) that can be downloaded successfully.

Example:
    
    from imagedl.imagedl import ImageClient

    client = ImageClient(work_dir="my_images")

    # 1. Search
    infos = client.search("Eiffel Tower", search_limits_overrides=30)

    # 2. Download
    client.download(infos, num_threadings_overrides=8)


## `imagedl.imagedl.modules.sources.BaseImageClient`

`BaseImageClient` is the **abstract base class** for all image search & download clients in this project.
Concrete clients inherit from it and reuse its common logic for:

- Session management (headers, cookies, user-agent, retries)
- Optional proxy auto-configuration
- Multithreaded search and download
- Progress bars and logging
- Result saving (`search_results.pkl`, `download_results.pkl`)

Current implementations built on top of `BaseImageClient` include:

- `imagedl.imagedl.modules.sources.BaiduImageClient`
- `imagedl.imagedl.modules.sources.BingImageClient`
- `imagedl.imagedl.modules.sources.DuckduckgoImageClient`
- `imagedl.imagedl.modules.sources.DanbooruImageClient`
- `imagedl.imagedl.modules.sources.DimTownImageClient`
- `imagedl.imagedl.modules.sources.EverypixelImageClient`
- `imagedl.imagedl.modules.sources.FoodiesfeedImageClient`
- `imagedl.imagedl.modules.sources.GoogleImageClient`
- `imagedl.imagedl.modules.sources.GelbooruImageClient`
- `imagedl.imagedl.modules.sources.HuabanImageClient`
- `imagedl.imagedl.modules.sources.I360ImageClient`
- `imagedl.imagedl.modules.sources.PixabayImageClient`
- `imagedl.imagedl.modules.sources.PexelsImageClient`
- `imagedl.imagedl.modules.sources.SogouImageClient`
- `imagedl.imagedl.modules.sources.SafebooruImageClient`
- `imagedl.imagedl.modules.sources.UnsplashImageClient`
- `imagedl.imagedl.modules.sources.YandexImageClient`
- `imagedl.imagedl.modules.sources.YahooImageClient`

In most cases, users do **not** instantiate `BaseImageClient` directly. 
Instead, they use high-level wrappers such as `BaiduImageClient`. 
However, the external **API surface** of all clients is the same as `BaseImageClient` (`search` + `download`).
Arguments supported when initializing this class include:

- **auto_set_proxies** (`bool`, default: `False`): If `True`, randomly assign a free proxy fetched by `freeproxy.ProxiedSessionClient` (details refer to [FreeProxy](https://github.com/CharlesPikachu/freeproxy)) for each request.

- **random_update_ua** (`bool`, default: `False`): If `True`, randomly updates the `User-Agent` header before each request (using `fake_useragent.UserAgent().random`), providing additional variability.

- **enable_search_curl_cffi** (`bool`, default: `False`): If `True`, `curl_cffi.requests.Session` is adopted for each search request.

- **enable_download_curl_cffi** (`bool`, default: `False`): If `True`, `curl_cffi.requests.Session` is adopted for each download request.

- **max_retries** (`int`, default: `5`): Maximum number of retry attempts in `BaseImageClient.get()` / `BaseImageClient.post()` when requests fail or return non-200 HTTP status codes.

- **maintain_session** (`bool`, default: `False`): If `False`: a new `requests.Session` is created before each request. If `True`: the same session is reused across requests. Combined with `random_update_ua`, this controls how “sticky” your session is.

- **logger_handle** (`LoggerHandle` or `None`, default: `None`): Logger used for informational messages and error reporting. If `None`, a default `LoggerHandle` instance is created.

- **disable_print** (`bool`, default: `False`): If `True`, suppresses console printing in `LoggerHandle` (logging still happens internally).

- **work_dir** (`str`, default: `"imagedl_outputs"`): Root directory for all outputs produced by this client. Under this directory, the client will create per-source and per-search subfolders, for example:
  - `imagedl_outputs/BaiduImageClient/2025-11-19-18-30-00 cat/`
  - Inside each search folder:
    - `search_results.pkl`
    - `download_results.pkl`
    - image files: `00000001.jpg`, `00000002.png`, ...

- **freeproxy_settings** (`dict` or `None`, default: `None`): Arguments passed when instantiating `freeproxy.ProxiedSessionClient`. If `None`, defaults to `dict(disable_print=True, proxy_sources=['ProxiflyProxiedSession'], max_tries=20, init_proxied_session_cfg={})` when `auto_set_proxies=True`.

- **default_search_cookies** (`dict` or `None`, default: `None`): Default cookies used for each search request.

- **default_download_cookies** (`dict` or `None`, default: `None`): Default cookies used for each download request.

#### `BaseImageClient.search`

Argument:

- **keyword** (`str`): Search keyword / query sent to the image provider (e.g., `"Eiffel Tower"`, `"golden retriever"`).

- **search_limits** (`int`, default: `1000`): Target maximum number of image records to retrieve. Exact behavior depends on how `BaseImageClient._constructsearchurls` is implemented in the subclass.

- **num_threadings** (`int`, default: `5`): Number of worker threads used to fetch search pages in parallel. Each thread runs `BaseImageClient._search`, pulling URLs from the shared `search_urls` list.

- **filters** (`dict` or `None`, default: `None`): Optional filter configuration that subclasses may use to refine search results (*e.g.*, image size, color, type). The structure is client-specific.

- **request_overrides** (`dict` or `None`, default: `None`): Extra keyword arguments forwarded to `requests.get` for search requests (e.g., `timeout`, `headers`, `proxies`). These are merged on top of the session’s default headers and proxy settings.

Returns:

- `list` of `image_info` dicts. The exact keys are determined by the subclass, but `BaseImageClient` expects at least:
  - `identifier`: a unique ID used for deduplication.
  - `candidate_urls`: list of candidate image URLs for downloading.
  - After the search pipeline, it also fills:
    - `work_dir`: per-search directory.
    - `file_path`: **base** file path (without extension) reserved for downloading.

#### `BaseImageClient.download`

Argument:

- **image_infos** (`list`): List of image metadata entries produced by `BaseImageClient.search()`, or loaded from `search_results.pkl`. Each entry should contain at least:

  - `work_dir`: directory where the image should be saved.
  - `file_path`: base file path (without extension).
  - `candidate_urls`: list of URLs to try when downloading the image.

- **num_threadings** (`int`, default: `5`): Number of worker threads to use for downloading images in parallel.

- **request_overrides** (`dict` or `None`, default: `None`): Extra keyword arguments forwarded to `requests.get` for **download** requests (*e.g.*, `timeout`, per-request headers or proxies). These options override or extend the session-level defaults.

Returns:

- `list` of `downloaded_image_info` dicts. For each successfully downloaded image:

  - `file_path` is updated to include the actual file extension (e.g. `.../00000001.jpg`).
  - Other fields are copied from the original `image_info`.

