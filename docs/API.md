# Imagedl APIs


## `imagedl.imagedl.ImageClient`

`ImageClient` is a high-level interface for searching and downloading images using different backends (e.g. `BaiduImageClient`, `BingImageClient` and `GoogleImageClient`) registered in `ImageClientBuilder.REGISTERED_MODULES`.
Arguments supported when initializing this class include:

- **image_source** (`str`, default: `BaiduImageClient`): Name of the image client backend to use. Must be one of the registered modules in ImageClientBuilder.REGISTERED_MODULES.

- **init_image_client_cfg** (`dict` or `None`, default: `None`): Extra configuration passed to the underlying image client on initialization. It is merged into a default config:
  ```python
  default_image_client_cfg = {
    "work_dir": "imagedl_outputs",
    "logger_handle": ImageClient.logger_handle,
    "type": image_source,
	"auto_set_proxies": True,
	"random_update_ua": False,
	"max_retries": 5,
	"maintain_session": False,
	"disable_print": False,
	"proxy_sources": None,
  }
  ```

- **search_limits** (`int`, default: `1000`): Default maximum number of images to retrieve per search. Can be overridden per call in `ImageClient.search()`.

- **num_threadings** (`int`, default: `5`): Default number of threads to use for network requests and downloads. Can be overridden per call in `ImageClient.search()` and `ImageClient.download()`.

- **request_overrides** (`dict` or `None`, default: `None`): Extra keyword arguments forwarded to `requests.get` in the underlying image client, e.g., `proxies` and `timeout`.
  These are stored and passed to both `ImageClient.search()` and `ImageClient.download()` unless overridden inside the backend.

#### `ImageClient.startcmdui`

#### `ImageClient.search`

#### `ImageClient.download`