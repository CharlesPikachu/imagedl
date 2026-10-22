'''
Function:
    Implementation of Naive MCP Examples
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import sys, logging
from mcp.server.fastmcp import FastMCP
from imagedl import imagedl as imagedl_pkg


'''settings'''
_client = None
mcp = FastMCP("imagedl")
logging.basicConfig(stream=sys.stderr, level=logging.INFO)


def getclient(image_source=None, init_image_client_cfg=None, search_limits=1000, num_threadings=5, request_overrides=None):
    """get image client"""
    global _client
    if _client is None:
        init_image_client_cfg = init_image_client_cfg or {}
        init_image_client_cfg.setdefault("disable_print", True)
        _client = imagedl_pkg.ImageClient(
            image_source=image_source or "BaiduImageClient", init_image_client_cfg=init_image_client_cfg, search_limits=search_limits,
            num_threadings=num_threadings, request_overrides=request_overrides or {},
        )
    return _client


@mcp.tool()
def search(keyword: str, image_source: str | None = None, search_limits_overrides: int | None = None, num_threadings_overrides: int | None = None, filters: dict | None = None) -> dict:
    """Search images (metadata only)."""
    client = getclient(image_source=image_source)
    infos = client.search(
        keyword=keyword, search_limits_overrides=search_limits_overrides, num_threadings_overrides=num_threadings_overrides, filters=filters,
    )
    return {"image_infos": infos}


@mcp.tool()
def download(image_infos: list) -> dict:
    """Download images described by image_infos."""
    out = getclient().download(image_infos=image_infos)
    return {"ok": True, "downloaded": out}


'''main'''
if __name__ == "__main__":
    mcp.run(transport="stdio")