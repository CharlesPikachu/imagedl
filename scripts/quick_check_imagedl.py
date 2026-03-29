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
from imagedl.modules import ImageClientBuilder, BaseImageClient


'''settings'''
QUERiES = ["Pikachu", "JK", "Cute Animals", "Mountains", "Girls"]
MAX_SEARCH = 10
MAX_DL_PER_CLIENT = 10
RESULTS_ROOT = Path("daily_test_results")
IMAGE_EXTENSIONS = (".rgb", ".gif", ".pbm", ".pgm", ".ppm", ".tif", ".tiff", ".rast", ".xbm", ".jpeg", ".jpg", ".bmp", ".png", ".webp", ".exr", ".svg", ".avif", ".heic", ".heif")
SEARCH_SUPPLEMENT = { # It seems that the server used in the GitHub Action cannot access some search APIs, so we will skip the check and use SEARCH_SUPPLEMENT.
    'BaiduImageClient': [
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/2437059527.jpg', 'https://img1.baidu.com/it/u=2136025053,3600010570&fm=253&fmt=auto&app=138&f=JPEG?w=684&h=500', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/2437059527.jpg', 'https://img1.baidu.com/it/u=2136025053,3600010570&fm=253&fmt=auto&app=138&f=JPEG?w=684&h=500', 'https://img1.baidu.com/it/u=2136025053,3600010570&fm=253&fmt=auto&app=138&f=JPEG?w=684&h=500'], 'identifier': 'https://hellorfimg.zcool.cn/large/2437059527.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000001'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/1233741523.jpg', 'https://img1.baidu.com/it/u=78971349,4168486351&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=711', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/1233741523.jpg', 'https://img1.baidu.com/it/u=78971349,4168486351&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=711', 'https://img1.baidu.com/it/u=78971349,4168486351&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=711'], 'identifier': 'https://hellorfimg.zcool.cn/large/1233741523.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000021'}, 
        {'candidate_urls': ['https://hbimg.b0.upaiyun.com/6925f8c2a43fb4c6bd781073239eebd951da458b5ad13-8nZ8Sg_fw658', 'https://img2.baidu.com/it/u=404361699,2148481436&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=776', 'https:\\/\\/hbimg.b0.upaiyun.com\\/6925f8c2a43fb4c6bd781073239eebd951da458b5ad13-8nZ8Sg_fw658', 'https://img2.baidu.com/it/u=404361699,2148481436&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=776', 'https://img2.baidu.com/it/u=404361699,2148481436&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=776'], 'identifier': 'https://hbimg.b0.upaiyun.com/6925f8c2a43fb4c6bd781073239eebd951da458b5ad13-8nZ8Sg_fw658', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000022'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/1284714829.jpg', 'https://img0.baidu.com/it/u=3518453307,2237170288&fm=253&fmt=auto&app=138&f=JPEG?w=654&h=500', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/1284714829.jpg', 'https://img0.baidu.com/it/u=3518453307,2237170288&fm=253&fmt=auto&app=138&f=JPEG?w=654&h=500', 'https://img0.baidu.com/it/u=3518453307,2237170288&fm=253&fmt=auto&app=138&f=JPEG?w=654&h=500'], 'identifier': 'https://hellorfimg.zcool.cn/large/1284714829.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000023'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/1625850256.jpg?x-image-process=image/format,webp', 'https://img0.baidu.com/it/u=13977428,2245298674&fm=253&fmt=auto&app=138&f=JPEG?w=681&h=500', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/1625850256.jpg?x-image-process=image\\/format,webp', 'https://img0.baidu.com/it/u=13977428,2245298674&fm=253&fmt=auto&app=138&f=JPEG?w=681&h=500', 'https://img0.baidu.com/it/u=13977428,2245298674&fm=253&fmt=auto&app=138&f=JPEG?w=681&h=500'], 'identifier': 'https://hellorfimg.zcool.cn/large/1625850256.jpg?x-image-process=image/format,webp', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000024'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/2278023137.jpg', 'https://img0.baidu.com/it/u=67333205,1886979999&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=949', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/2278023137.jpg', 'https://img0.baidu.com/it/u=67333205,1886979999&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=949', 'https://img0.baidu.com/it/u=67333205,1886979999&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=949'], 'identifier': 'https://hellorfimg.zcool.cn/large/2278023137.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000025'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/1284275206.jpg?x-image-process=image/format,webp', 'https://img2.baidu.com/it/u=240572267,3438783617&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=533', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/1284275206.jpg?x-image-process=image\\/format,webp', 'https://img2.baidu.com/it/u=240572267,3438783617&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=533', 'https://img2.baidu.com/it/u=240572267,3438783617&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=533'], 'identifier': 'https://hellorfimg.zcool.cn/large/1284275206.jpg?x-image-process=image/format,webp', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000026'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/1792498645.jpg', 'https://img2.baidu.com/it/u=1368813230,1956862888&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=533', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/1792498645.jpg', 'https://img2.baidu.com/it/u=1368813230,1956862888&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=533', 'https://img2.baidu.com/it/u=1368813230,1956862888&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=533'], 'identifier': 'https://hellorfimg.zcool.cn/large/1792498645.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000027'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/1441794707.jpg', 'https://img1.baidu.com/it/u=1325956228,1122946288&fm=253&fmt=auto&app=138&f=JPEG?w=681&h=500', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/1441794707.jpg', 'https://img1.baidu.com/it/u=1325956228,1122946288&fm=253&fmt=auto&app=138&f=JPEG?w=681&h=500', 'https://img1.baidu.com/it/u=1325956228,1122946288&fm=253&fmt=auto&app=138&f=JPEG?w=681&h=500'], 'identifier': 'https://hellorfimg.zcool.cn/large/1441794707.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000028'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/790365352.jpg', 'https://img1.baidu.com/it/u=982048691,2691142154&fm=253&fmt=auto&app=138&f=JPEG?w=612&h=500', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/790365352.jpg', 'https://img1.baidu.com/it/u=982048691,2691142154&fm=253&fmt=auto&app=138&f=JPEG?w=612&h=500', 'https://img1.baidu.com/it/u=982048691,2691142154&fm=253&fmt=auto&app=138&f=JPEG?w=612&h=500'], 'identifier': 'https://hellorfimg.zcool.cn/large/790365352.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000029'}, 
    ],
    'UnsplashImageClient': [
        {'candidate_urls': ['https://images.unsplash.com/photo-1578956919791-af7615c94b90?ixid=M3wxMjA3fDB8MXxzZWFyY2h8M3x8Q3V0ZSUyMEFuaW1hbHN8ZW58MHx8fHwxNzY1NzU4Mzg3fDA&ixlib=rb-4.1.0', 'https://images.unsplash.com/photo-1578956919791-af7615c94b90?crop=entropy&cs=srgb&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8M3x8Q3V0ZSUyMEFuaW1hbHN8ZW58MHx8fHwxNzY1NzU4Mzg3fDA&ixlib=rb-4.1.0&q=85', 'https://images.unsplash.com/photo-1578956919791-af7615c94b90?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8M3x8Q3V0ZSUyMEFuaW1hbHN8ZW58MHx8fHwxNzY1NzU4Mzg3fDA&ixlib=rb-4.1.0&q=80&w=1080', 'https://images.unsplash.com/photo-1578956919791-af7615c94b90?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8M3x8Q3V0ZSUyMEFuaW1hbHN8ZW58MHx8fHwxNzY1NzU4Mzg3fDA&ixlib=rb-4.1.0&q=80&w=400', 'https://images.unsplash.com/photo-1578956919791-af7615c94b90?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8M3x8Q3V0ZSUyMEFuaW1hbHN8ZW58MHx8fHwxNzY1NzU4Mzg3fDA&ixlib=rb-4.1.0&q=80&w=200', 'https://s3.us-west-2.amazonaws.com/images.unsplash.com/small/photo-1578956919791-af7615c94b90'], 'identifier': 'JDzoTGfoogA', 'work_dir': 'tmp/UnsplashImageClient/2025-12-15-08-28-25 CuteAnimals', 'file_path': 'tmp/UnsplashImageClient/2025-12-15-08-28-25 CuteAnimals/00000003'}, 
        {'candidate_urls': ['https://images.unsplash.com/photo-1560114928-40f1f1eb26a0?ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTB8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0', 'https://images.unsplash.com/photo-1560114928-40f1f1eb26a0?crop=entropy&cs=srgb&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTB8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=85', 'https://images.unsplash.com/photo-1560114928-40f1f1eb26a0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTB8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=80&w=1080', 'https://images.unsplash.com/photo-1560114928-40f1f1eb26a0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTB8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=80&w=400', 'https://images.unsplash.com/photo-1560114928-40f1f1eb26a0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTB8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=80&w=200', 'https://s3.us-west-2.amazonaws.com/images.unsplash.com/small/photo-1560114928-40f1f1eb26a0'], 'identifier': 'RCfi7vgJjUY', 'work_dir': 'tmp/UnsplashImageClient/2025-12-15-08-28-25 CuteAnimals', 'file_path': 'tmp/UnsplashImageClient/2025-12-15-08-28-25 CuteAnimals/00000010'}, 
        {'candidate_urls': ['https://images.unsplash.com/photo-1548210775-eaa794f59b92?ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTF8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0', 'https://images.unsplash.com/photo-1548210775-eaa794f59b92?crop=entropy&cs=srgb&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTF8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=85', 'https://images.unsplash.com/photo-1548210775-eaa794f59b92?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTF8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=80&w=1080', 'https://images.unsplash.com/photo-1548210775-eaa794f59b92?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTF8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=80&w=400', 'https://images.unsplash.com/photo-1548210775-eaa794f59b92?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTF8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=80&w=200', 'https://s3.us-west-2.amazonaws.com/images.unsplash.com/small/photo-1548210775-eaa794f59b92'], 'identifier': 'fG1rP1UOGXs', 'work_dir': 'tmp/UnsplashImageClient/2025-12-15-08-28-25 CuteAnimals', 'file_path': 'tmp/UnsplashImageClient/2025-12-15-08-28-25 CuteAnimals/00000011'}, 
        {'candidate_urls': ['https://images.unsplash.com/photo-1451303688941-9e06d4b1277a?ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTJ8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0', 'https://images.unsplash.com/photo-1451303688941-9e06d4b1277a?crop=entropy&cs=srgb&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTJ8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=85', 'https://images.unsplash.com/photo-1451303688941-9e06d4b1277a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTJ8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=80&w=1080', 'https://images.unsplash.com/photo-1451303688941-9e06d4b1277a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTJ8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=80&w=400', 'https://images.unsplash.com/photo-1451303688941-9e06d4b1277a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTJ8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=80&w=200', 'https://s3.us-west-2.amazonaws.com/images.unsplash.com/small/photo-1451303688941-9e06d4b1277a'], 'identifier': 'GYumuBnTqKc', 'work_dir': 'tmp/UnsplashImageClient/2025-12-15-08-28-25 CuteAnimals', 'file_path': 'tmp/UnsplashImageClient/2025-12-15-08-28-25 CuteAnimals/00000012'}, 
        {'candidate_urls': ['https://images.unsplash.com/photo-1541364983171-a8ba01e95cfc?ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTR8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0', 'https://images.unsplash.com/photo-1541364983171-a8ba01e95cfc?crop=entropy&cs=srgb&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTR8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=85', 'https://images.unsplash.com/photo-1541364983171-a8ba01e95cfc?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTR8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=80&w=1080', 'https://images.unsplash.com/photo-1541364983171-a8ba01e95cfc?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTR8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=80&w=400', 'https://images.unsplash.com/photo-1541364983171-a8ba01e95cfc?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTR8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=80&w=200', 'https://s3.us-west-2.amazonaws.com/images.unsplash.com/small/photo-1541364983171-a8ba01e95cfc'], 'identifier': 'pOUA8Xay514', 'work_dir': 'tmp/UnsplashImageClient/2025-12-15-08-28-25 CuteAnimals', 'file_path': 'tmp/UnsplashImageClient/2025-12-15-08-28-25 CuteAnimals/00000014'}, 
        {'candidate_urls': ['https://images.unsplash.com/photo-1560743641-3914f2c45636?ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTV8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0', 'https://images.unsplash.com/photo-1560743641-3914f2c45636?crop=entropy&cs=srgb&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTV8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=85', 'https://images.unsplash.com/photo-1560743641-3914f2c45636?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTV8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=80&w=1080', 'https://images.unsplash.com/photo-1560743641-3914f2c45636?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTV8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=80&w=400', 'https://images.unsplash.com/photo-1560743641-3914f2c45636?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTV8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=80&w=200', 'https://s3.us-west-2.amazonaws.com/images.unsplash.com/small/photo-1560743641-3914f2c45636'], 'identifier': '1VgfQdCuX-4', 'work_dir': 'tmp/UnsplashImageClient/2025-12-15-08-28-25 CuteAnimals', 'file_path': 'tmp/UnsplashImageClient/2025-12-15-08-28-25 CuteAnimals/00000015'}, 
        {'candidate_urls': ['https://images.unsplash.com/photo-1514571948039-d3cb9e8f9750?ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTZ8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0', 'https://images.unsplash.com/photo-1514571948039-d3cb9e8f9750?crop=entropy&cs=srgb&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTZ8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=85', 'https://images.unsplash.com/photo-1514571948039-d3cb9e8f9750?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTZ8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=80&w=1080', 'https://images.unsplash.com/photo-1514571948039-d3cb9e8f9750?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTZ8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=80&w=400', 'https://images.unsplash.com/photo-1514571948039-d3cb9e8f9750?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTZ8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=80&w=200', 'https://s3.us-west-2.amazonaws.com/images.unsplash.com/small/photo-1514571948039-d3cb9e8f9750'], 'identifier': 'pueU9kKIkXw', 'work_dir': 'tmp/UnsplashImageClient/2025-12-15-08-28-25 CuteAnimals', 'file_path': 'tmp/UnsplashImageClient/2025-12-15-08-28-25 CuteAnimals/00000016'}, 
        {'candidate_urls': ['https://images.unsplash.com/photo-1559214369-a6b1d7919865?ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTh8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0', 'https://images.unsplash.com/photo-1559214369-a6b1d7919865?crop=entropy&cs=srgb&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTh8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=85', 'https://images.unsplash.com/photo-1559214369-a6b1d7919865?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTh8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=80&w=1080', 'https://images.unsplash.com/photo-1559214369-a6b1d7919865?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTh8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=80&w=400', 'https://images.unsplash.com/photo-1559214369-a6b1d7919865?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTh8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=80&w=200', 'https://s3.us-west-2.amazonaws.com/images.unsplash.com/small/photo-1559214369-a6b1d7919865'], 'identifier': 'KNMbRhf5IT8', 'work_dir': 'tmp/UnsplashImageClient/2025-12-15-08-28-25 CuteAnimals', 'file_path': 'tmp/UnsplashImageClient/2025-12-15-08-28-25 CuteAnimals/00000018'}, 
        {'candidate_urls': ['https://images.unsplash.com/photo-1502780402662-acc01c084a25?ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTl8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0', 'https://images.unsplash.com/photo-1502780402662-acc01c084a25?crop=entropy&cs=srgb&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTl8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=85', 'https://images.unsplash.com/photo-1502780402662-acc01c084a25?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTl8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=80&w=1080', 'https://images.unsplash.com/photo-1502780402662-acc01c084a25?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTl8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=80&w=400', 'https://images.unsplash.com/photo-1502780402662-acc01c084a25?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTl8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=80&w=200', 'https://s3.us-west-2.amazonaws.com/images.unsplash.com/small/photo-1502780402662-acc01c084a25'], 'identifier': '2slBHG3HtdA', 'work_dir': 'tmp/UnsplashImageClient/2025-12-15-08-28-25 CuteAnimals', 'file_path': 'tmp/UnsplashImageClient/2025-12-15-08-28-25 CuteAnimals/00000019'}, 
        {'candidate_urls': ['https://images.unsplash.com/photo-1504006833117-8886a355efbf?ixid=M3wxMjA3fDB8MXxzZWFyY2h8MjB8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0', 'https://images.unsplash.com/photo-1504006833117-8886a355efbf?crop=entropy&cs=srgb&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MjB8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=85', 'https://images.unsplash.com/photo-1504006833117-8886a355efbf?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MjB8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=80&w=1080', 'https://images.unsplash.com/photo-1504006833117-8886a355efbf?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MjB8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=80&w=400', 'https://images.unsplash.com/photo-1504006833117-8886a355efbf?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MjB8fEN1dGUlMjBBbmltYWxzfGVufDB8fHx8MTc2NTc1ODM4N3ww&ixlib=rb-4.1.0&q=80&w=200', 'https://s3.us-west-2.amazonaws.com/images.unsplash.com/small/photo-1504006833117-8886a355efbf'], 'identifier': 'bKhETeDV1WM', 'work_dir': 'tmp/UnsplashImageClient/2025-12-15-08-28-25 CuteAnimals', 'file_path': 'tmp/UnsplashImageClient/2025-12-15-08-28-25 CuteAnimals/00000020'}
    ],
    'EverypixelImageClient': [
        {'candidate_urls': ['https://image.everypixel.com/blockchain/preview/0b/78/0b78dfb8f8a94dc68fddba122eb00383.jpg'], 'raw_data': {}, 'identifier': '16535908708498906655', 'work_dir': 'tmp/EverypixelImageClient/2026-02-11-16-10-57 animals', 'file_path': 'tmp/EverypixelImageClient/2026-02-11-16-10-57 animals/00000001'}, 
        {'candidate_urls': ['https://image.everypixel.com/blockchain/70/94/7094e958-d679-43e3-ab66-4f39625fa81e.jpg'], 'raw_data': {}, 'identifier': '1615603247486835090', 'work_dir': 'tmp/EverypixelImageClient/2026-02-11-16-10-57 animals', 'file_path': 'tmp/EverypixelImageClient/2026-02-11-16-10-57 animals/00000002'}, 
        {'candidate_urls': ['https://image.everypixel.com/blockchain/e0/57/e057bf9f-6bbb-4bb8-b466-df6d203e771d.jpg'], 'raw_data': {}, 'identifier': '2276294493219687570', 'work_dir': 'tmp/EverypixelImageClient/2026-02-11-16-10-57 animals', 'file_path': 'tmp/EverypixelImageClient/2026-02-11-16-10-57 animals/00000003'}, 
        {'candidate_urls': ['https://image.everypixel.com/blockchain/preview/71/b1/71b15b55376e48cb925eddac9bf0edcb.jpg'], 'raw_data': {}, 'identifier': '12497667937246440531', 'work_dir': 'tmp/EverypixelImageClient/2026-02-11-16-10-57 animals', 'file_path': 'tmp/EverypixelImageClient/2026-02-11-16-10-57 animals/00000005'}, 
        {'candidate_urls': ['https://image.everypixel.com/blockchain/4f/89/4f897aac-e6fa-4e93-b788-96e11f551635.jpg'], 'raw_data': {}, 'identifier': '8668484780732368779', 'work_dir': 'tmp/EverypixelImageClient/2026-02-11-16-10-57 animals', 'file_path': 'tmp/EverypixelImageClient/2026-02-11-16-10-57 animals/00000006'}, 
        {'candidate_urls': ['https://image.everypixel.com/blockchain/preview/9b/a3/9ba32bc13eb24ce5a6f3db4943e09966.jpg'], 'raw_data': {}, 'identifier': '6516945962049324033', 'work_dir': 'tmp/EverypixelImageClient/2026-02-11-16-10-57 animals', 'file_path': 'tmp/EverypixelImageClient/2026-02-11-16-10-57 animals/00000007'}, 
        {'candidate_urls': ['https://image.everypixel.com/blockchain/6d/fc/6dfc104a-6a6e-449d-9c0e-35323ea7d576.jpg'], 'raw_data': {}, 'identifier': '741921713100709295', 'work_dir': 'tmp/EverypixelImageClient/2026-02-11-16-10-57 animals', 'file_path': 'tmp/EverypixelImageClient/2026-02-11-16-10-57 animals/00000008'}, 
        {'candidate_urls': ['https://image.everypixel.com/blockchain/preview/1c/1a/1c1a67c7bca8439f9a77923110efad75.jpg'], 'raw_data': {}, 'identifier': '8846301030990552764', 'work_dir': 'tmp/EverypixelImageClient/2026-02-11-16-10-57 animals', 'file_path': 'tmp/EverypixelImageClient/2026-02-11-16-10-57 animals/00000009'}, 
        {'candidate_urls': ['https://image.everypixel.com/blockchain/b1/8d/b18d680a-be7d-4272-8069-e875c8cee457.jpg'], 'raw_data': {}, 'identifier': '4464702561003756688', 'work_dir': 'tmp/EverypixelImageClient/2026-02-11-16-10-57 animals', 'file_path': 'tmp/EverypixelImageClient/2026-02-11-16-10-57 animals/00000010'}
    ],
}


'''ensuredir'''
def ensuredir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


'''runningingithubactions'''
def runningingithubactions() -> bool:
    return (
        os.getenv("GITHUB_ACTIONS", "").lower() == "true"
        and os.getenv("CI", "").lower() == "true"
    )


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
    print(f"Query: {', '.join(QUERiES)}")
    # iter
    for client_name, client_module in ImageClientBuilder.REGISTERED_MODULES.items():
        print(f"\n[Module] {client_name}")
        client: BaseImageClient = client_module(disable_print=False, work_dir=tmp_dir, auto_set_proxies=False)
        status = {"name": client_name, "search_ok": False, "download_ok": False, "ok": False, "n_results": 0, "n_downloaded": 0, "error": None, "downloaded_images": [], "search_samples": []}
        target_dir: Path = base_results_dir / client_name
        # --search checking
        try:
            if client_name in SEARCH_SUPPLEMENT and runningingithubactions():
                image_infos = SEARCH_SUPPLEMENT[client_name]
            elif client_name in {'FreeNatureStockImageClient'}:
                image_infos = client.search(QUERiES[3], search_limits=MAX_SEARCH, num_threadings=2)
            else:
                image_infos = client.search(QUERiES[0], search_limits=MAX_SEARCH, num_threadings=2)
            for image_info in image_infos: image_info.raw_data = {}
            n_results = len(image_infos) if image_infos is not None else 0
            status["n_results"] = n_results
            status["search_ok"] = n_results > 0
            status["search_samples"] = [info.candidate_download_urls[0] for info in (image_infos or [])[:3]]
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
            n_downloaded = len([os.path.join(r, f) for r, _, fs in os.walk(tmp_dir) for f in fs if f.lower().endswith(IMAGE_EXTENSIONS)])
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
        [shutil.move(os.path.join(r, f), target_dir) for r, _, fs in os.walk(tmp_dir) for f in fs if f.lower().endswith(IMAGE_EXTENSIONS)]
        shutil.rmtree(tmp_dir, ignore_errors=True)
        status["downloaded_images"] = [str(p.as_posix()) for p in target_dir.glob("*")]
        # --summary
        status["ok"] = bool(status["search_ok"] and status["download_ok"])
        modules_summary.append(status)
    # write to 
    payload = {
        "date": date_str, "timestamp_utc": timestamp, "query": ', '.join(QUERiES), "max_search": MAX_SEARCH, "max_download_per_client": MAX_DL_PER_CLIENT, "modules": modules_summary,
    }
    summary_path = base_results_dir / "summary_latest.json"
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"\nSaved summary to {summary_path}")


'''init'''
if __name__ == "__main__":
    main()
