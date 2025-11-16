'''
Function:
    Implementation of quickly checking the effectiveness of imagedl
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import json
import shutil
import contextlib
from pathlib import Path
from datetime import datetime, timezone
from imagedl.modules import ImageClientBuilder


'''settings'''
QUERY = "Cute Animals"
MAX_SEARCH = 10
MAX_DL_PER_CLIENT = 10
RESULTS_ROOT = Path("daily_test_results")


'''ensuredir'''
def ensuredir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


'''cd'''
@contextlib.contextmanager
def cd(newdir: Path):
    prev = os.getcwd()
    os.chdir(str(newdir))
    try: yield
    finally: os.chdir(prev)


'''main'''
def main():
    # basic info
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    timestamp = now.isoformat()
    base_results_dir = RESULTS_ROOT
    ensuredir(base_results_dir)
    tmp_dir = 'tmp'
    # init summary
    modules_summary = []
    print(f"=== imagedl daily check @ {timestamp} (UTC) ===")
    print(f"Query: {QUERY}")
    # iter
    for client_name, client_module in ImageClientBuilder.REGISTERED_MODULES.items():
        print(f"\n[Module] {client_name}")
        if client_name in ['BaiduImageClient', 'DuckduckgoImageClient']:
            client = client_module(
                disable_print=False, work_dir=tmp_dir, auto_set_proxies=True, max_retries=20,
                proxy_sources=['QiyunipProxiedSession', 'FreeproxylistProxiedSession', 'KuaidailiProxiedSession', 'KxdailiProxiedSession']
            )
        else:
            client = client_module(disable_print=False, work_dir=tmp_dir, auto_set_proxies=False)
        status = {
            "name": client_name, "search_ok": False, "download_ok": False, "ok": False, "n_results": 0,
            "n_downloaded": 0, "error": None, "downloaded_images": [], "search_samples": [],
        }
        target_dir: Path = base_results_dir / client_name
        # --search checking
        try:
            image_infos = client.search(QUERY, search_limits=MAX_SEARCH, num_threadings=2)
            n_results = len(image_infos) if image_infos is not None else 0
            status["n_results"] = n_results
            status["search_ok"] = n_results > 0
            status["search_samples"] = [info['candidate_urls'][0] for info in (image_infos or [])[:3]]
            print(f"  Search results: {n_results} (Success)" if status["search_ok"] else f"  Search results: {n_results} (NULL)")
        except Exception as err:
            status["error"] = f"search_error: {type(err).__name__}: {err}"
            print(f"  !! Search failed: {status['error']}")
            modules_summary.append(status)
            shutil.rmtree(tmp_dir, ignore_errors=True)
            continue
        if not status["search_ok"]:
            modules_summary.append(status)
            shutil.rmtree(tmp_dir, ignore_errors=True)
            continue
        # --download checking
        try:
            subset = image_infos[:MAX_DL_PER_CLIENT]
            client.download(subset, num_threadings=1)
            n_downloaded = len([os.path.join(r, f) for r, _, fs in os.walk(tmp_dir) for f in fs if f.lower().endswith(('.jpg','.jpeg','.png','.gif','.bmp','.tif','.tiff','.webp'))])
            status["n_downloaded"] = n_downloaded
            status["download_ok"] = status["n_downloaded"] > 0
            print(f"  Downloaded images: {n_downloaded} (Success)" if status["download_ok"] else f"  Downloaded images: {n_downloaded} (NULL)")
        except Exception as err:
            msg = f"download_error: {type(err).__name__}: {err}"
            status["error"] = f"{status['error']} | {msg}" if status["error"] else msg
            print(f"  !! Download failed: {msg}")
            modules_summary.append(status)
            shutil.rmtree(tmp_dir, ignore_errors=True)
            continue
        if not status["download_ok"]:
            modules_summary.append(status)
            shutil.rmtree(tmp_dir, ignore_errors=True)
            continue
        # --moving to target_dir
        shutil.rmtree(target_dir, ignore_errors=True); os.makedirs(target_dir)
        [shutil.move(os.path.join(r, f), target_dir) for r, _, fs in os.walk(tmp_dir) for f in fs if f.lower().endswith(('.jpg','.jpeg','.png','.gif','.bmp','.tif','.tiff','.webp'))]
        shutil.rmtree(tmp_dir, ignore_errors=True)
        status["downloaded_images"] = [str(p.as_posix()) for p in target_dir.glob("*")]
        # --summary
        status["ok"] = bool(status["search_ok"] and status["download_ok"])
        modules_summary.append(status)
    # write to 
    payload = {
        "date": date_str, "timestamp_utc": timestamp, "query": QUERY, "max_search": MAX_SEARCH, "max_download_per_client": MAX_DL_PER_CLIENT, "modules": modules_summary,
    }
    summary_path = base_results_dir / f"summary_{date_str}.json"
    ensuredir(summary_path.parent)
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    latest_path = base_results_dir / "summary_latest.json"
    with latest_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"\nSaved summary to {summary_path} and {latest_path}")


'''init'''
if __name__ == "__main__":
    main()