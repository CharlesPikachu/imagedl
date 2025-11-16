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
QUERY = "Cute Animals"
MAX_SEARCH = 10
MAX_DL_PER_CLIENT = 10
RESULTS_ROOT = Path("daily_test_results")
SEARCH_SUPPLEMENT = { # It seems that the server used in the GitHub Action cannot access Baidu or DuckDuckGo search APIs, so we will skip the check and use SEARCH_SUPPLEMENT.
    'BaiduImageClient': [
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/2437059527.jpg', 'https://img1.baidu.com/it/u=2136025053,3600010570&fm=253&fmt=auto&app=138&f=JPEG?w=684&h=500', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/2437059527.jpg', 'https://img1.baidu.com/it/u=2136025053,3600010570&fm=253&fmt=auto&app=138&f=JPEG?w=684&h=500', 'https://img1.baidu.com/it/u=2136025053,3600010570&fm=253&fmt=auto&app=138&f=JPEG?w=684&h=500'], 'identifier': 'https://hellorfimg.zcool.cn/large/2437059527.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000001'}, 
        {'candidate_urls': ['https://res.cqnews.net/contentcloud/1/REPRINT/DEFAULT/PICTURE/2024/6/12/2712af869d1941519bde373972276dce_wh1024x683.png', 'https://img0.baidu.com/it/u=3264526225,4087639899&fm=253&fmt=auto&app=138&f=JPEG?w=750&h=500', 'https:\\/\\/res.cqnews.net\\/contentcloud\\/1\\/REPRINT\\/DEFAULT\\/PICTURE\\/2024\\/6\\/12\\/2712af869d1941519bde373972276dce_wh1024x683.png', 'https://img0.baidu.com/it/u=3264526225,4087639899&fm=253&fmt=auto&app=138&f=JPEG?w=750&h=500', 'https://img0.baidu.com/it/u=3264526225,4087639899&fm=253&fmt=auto&app=138&f=JPEG?w=750&h=500'], 'identifier': 'https://res.cqnews.net/contentcloud/1/REPRINT/DEFAULT/PICTURE/2024/6/12/2712af869d1941519bde373972276dce_wh1024x683.png', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000002'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/1233741550.jpg', 'https://img1.baidu.com/it/u=3553895812,2082396333&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=711', 'https://img1.baidu.com/it/u=3553895812,2082396333&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=711', 'https://img1.baidu.com/it/u=3553895812,2082396333&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=711'], 'identifier': 'https://hellorfimg.zcool.cn/large/1233741550.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000003'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/2176938441.jpg', 'https://img0.baidu.com/it/u=2313549378,3634789340&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=1003', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/2176938441.jpg', 'https://img0.baidu.com/it/u=2313549378,3634789340&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=1003', 'https://img0.baidu.com/it/u=2313549378,3634789340&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=1003'], 'identifier': 'https://hellorfimg.zcool.cn/large/2176938441.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000004'}, 
        {'candidate_urls': ['https://sns-img-qc.xhscdn.com/1000g00825n5upvsfk0005og56t2k1br4h2caimo?imageView2/2/w/1080/format/webp', 'https://img2.baidu.com/it/u=4002502342,974647948&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=598', 'https:\\/\\/sns-img-qc.xhscdn.com\\/1000g00825n5upvsfk0005og56t2k1br4h2caimo?imageView2\\/2\\/w\\/1080\\/format\\/webp', 'https://img2.baidu.com/it/u=4002502342,974647948&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=598', 'https://img2.baidu.com/it/u=4002502342,974647948&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=598'], 'identifier': 'https://sns-img-qc.xhscdn.com/1000g00825n5upvsfk0005og56t2k1br4h2caimo?imageView2/2/w/1080/format/webp', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000005'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/1231725424.jpg', 'https://img0.baidu.com/it/u=487269389,408963465&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=711', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/1231725424.jpg', 'https://img0.baidu.com/it/u=487269389,408963465&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=711', 'https://img0.baidu.com/it/u=487269389,408963465&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=711'], 'identifier': 'https://hellorfimg.zcool.cn/large/1231725424.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000006'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/2064331421.jpg', 'https://img0.baidu.com/it/u=4029056166,2683816480&fm=253&fmt=auto&app=138&f=JPEG?w=681&h=500', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/2064331421.jpg', 'https://img0.baidu.com/it/u=4029056166,2683816480&fm=253&fmt=auto&app=138&f=JPEG?w=681&h=500', 'https://img0.baidu.com/it/u=4029056166,2683816480&fm=253&fmt=auto&app=138&f=JPEG?w=681&h=500'], 'identifier': 'https://hellorfimg.zcool.cn/large/2064331421.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000007'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/1233741484.jpg', 'https://img0.baidu.com/it/u=3431333854,392395905&fm=253&fmt=auto&app=138&f=JPEG?w=612&h=500', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/1233741484.jpg', 'https://img0.baidu.com/it/u=3431333854,392395905&fm=253&fmt=auto&app=138&f=JPEG?w=612&h=500', 'https://img0.baidu.com/it/u=3431333854,392395905&fm=253&fmt=auto&app=138&f=JPEG?w=612&h=500'], 'identifier': 'https://hellorfimg.zcool.cn/large/1233741484.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000008'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/2019207875.jpg', 'https://img2.baidu.com/it/u=3249534435,4290580926&fm=253&fmt=auto&app=138&f=JPEG?w=681&h=500', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/2019207875.jpg', 'https://img2.baidu.com/it/u=3249534435,4290580926&fm=253&fmt=auto&app=138&f=JPEG?w=681&h=500', 'https://img2.baidu.com/it/u=3249534435,4290580926&fm=253&fmt=auto&app=138&f=JPEG?w=681&h=500'], 'identifier': 'https://hellorfimg.zcool.cn/large/2019207875.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000009'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/2370942201.jpg', 'https://img1.baidu.com/it/u=729429281,1056475161&fm=253&fmt=auto&app=138&f=JPEG?w=682&h=500', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/2370942201.jpg', 'https://img1.baidu.com/it/u=729429281,1056475161&fm=253&fmt=auto&app=138&f=JPEG?w=682&h=500', 'https://img1.baidu.com/it/u=729429281,1056475161&fm=253&fmt=auto&app=138&f=JPEG?w=682&h=500'], 'identifier': 'https://hellorfimg.zcool.cn/large/2370942201.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000010'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/1607454556.jpg', 'https://img0.baidu.com/it/u=650212355,3180006971&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=533', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/1607454556.jpg', 'https://img0.baidu.com/it/u=650212355,3180006971&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=533', 'https://img0.baidu.com/it/u=650212355,3180006971&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=533'], 'identifier': 'https://hellorfimg.zcool.cn/large/1607454556.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000011'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/1596836053.jpg', 'https://img1.baidu.com/it/u=1326755787,4175852877&fm=253&fmt=auto&app=138&f=JPEG?w=681&h=500', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/1596836053.jpg', 'https://img1.baidu.com/it/u=1326755787,4175852877&fm=253&fmt=auto&app=138&f=JPEG?w=681&h=500', 'https://img1.baidu.com/it/u=1326755787,4175852877&fm=253&fmt=auto&app=138&f=JPEG?w=681&h=500'], 'identifier': 'https://hellorfimg.zcool.cn/large/1596836053.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000012'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/17120116.jpg', 'https://img1.baidu.com/it/u=1998639155,1545215799&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=532', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/17120116.jpg', 'https://img1.baidu.com/it/u=1998639155,1545215799&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=532', 'https://img1.baidu.com/it/u=1998639155,1545215799&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=532'], 'identifier': 'https://hellorfimg.zcool.cn/large/17120116.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000013'}, 
        {'candidate_urls': ['https://gd-hbimg.huaban.com/9fbf183f22d4f2efd7cb34e62f7cb4f39556605f735a9-g0TwW4_fw658', 'https://img1.baidu.com/it/u=153847336,4074460856&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=707', 'https:\\/\\/gd-hbimg.huaban.com\\/9fbf183f22d4f2efd7cb34e62f7cb4f39556605f735a9-g0TwW4_fw658', 'https://img1.baidu.com/it/u=153847336,4074460856&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=707', 'https://img1.baidu.com/it/u=153847336,4074460856&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=707'], 'identifier': 'https://gd-hbimg.huaban.com/9fbf183f22d4f2efd7cb34e62f7cb4f39556605f735a9-g0TwW4_fw658', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000014'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/1233741604.jpg', 'https://img0.baidu.com/it/u=3138962401,2160198931&fm=253&fmt=auto&app=138&f=JPEG?w=612&h=500', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/1233741604.jpg', 'https://img0.baidu.com/it/u=3138962401,2160198931&fm=253&fmt=auto&app=138&f=JPEG?w=612&h=500', 'https://img0.baidu.com/it/u=3138962401,2160198931&fm=253&fmt=auto&app=138&f=JPEG?w=612&h=500'], 'identifier': 'https://hellorfimg.zcool.cn/large/1233741604.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000015'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/2236746669.jpg', 'https://img2.baidu.com/it/u=998092317,652740840&fm=253&fmt=auto&app=138&f=JPEG?w=794&h=500', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/2236746669.jpg', 'https://img2.baidu.com/it/u=998092317,652740840&fm=253&fmt=auto&app=138&f=JPEG?w=794&h=500', 'https://img2.baidu.com/it/u=998092317,652740840&fm=253&fmt=auto&app=138&f=JPEG?w=794&h=500'], 'identifier': 'https://hellorfimg.zcool.cn/large/2236746669.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000016'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/1231722790.jpg', 'https://img1.baidu.com/it/u=4010721003,935360174&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=711', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/1231722790.jpg', 'https://img1.baidu.com/it/u=4010721003,935360174&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=711', 'https://img1.baidu.com/it/u=4010721003,935360174&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=711'], 'identifier': 'https://hellorfimg.zcool.cn/large/1231722790.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000017'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/2236746695.jpg', 'https://img1.baidu.com/it/u=2953466308,4223051481&fm=253&fmt=auto&app=138&f=JPEG?w=794&h=500', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/2236746695.jpg', 'https://img1.baidu.com/it/u=2953466308,4223051481&fm=253&fmt=auto&app=138&f=JPEG?w=794&h=500', 'https://img1.baidu.com/it/u=2953466308,4223051481&fm=253&fmt=auto&app=138&f=JPEG?w=794&h=500'], 'identifier': 'https://hellorfimg.zcool.cn/large/2236746695.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000018'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/2373054257.jpg', 'https://img0.baidu.com/it/u=261552302,2751682913&fm=253&fmt=auto&app=138&f=JPEG?w=682&h=500', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/2373054257.jpg', 'https://img0.baidu.com/it/u=261552302,2751682913&fm=253&fmt=auto&app=138&f=JPEG?w=682&h=500', 'https://img0.baidu.com/it/u=261552302,2751682913&fm=253&fmt=auto&app=138&f=JPEG?w=682&h=500'], 'identifier': 'https://hellorfimg.zcool.cn/large/2373054257.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000019'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/158111432.jpg', 'https://img0.baidu.com/it/u=3143341012,3199663218&fm=253&fmt=auto&app=138&f=JPEG?w=882&h=500', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/158111432.jpg', 'https://img0.baidu.com/it/u=3143341012,3199663218&fm=253&fmt=auto&app=138&f=JPEG?w=882&h=500', 'https://img0.baidu.com/it/u=3143341012,3199663218&fm=253&fmt=auto&app=138&f=JPEG?w=882&h=500'], 'identifier': 'https://hellorfimg.zcool.cn/large/158111432.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000020'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/1233741523.jpg', 'https://img1.baidu.com/it/u=78971349,4168486351&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=711', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/1233741523.jpg', 'https://img1.baidu.com/it/u=78971349,4168486351&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=711', 'https://img1.baidu.com/it/u=78971349,4168486351&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=711'], 'identifier': 'https://hellorfimg.zcool.cn/large/1233741523.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000021'}, 
        {'candidate_urls': ['https://hbimg.b0.upaiyun.com/6925f8c2a43fb4c6bd781073239eebd951da458b5ad13-8nZ8Sg_fw658', 'https://img2.baidu.com/it/u=404361699,2148481436&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=776', 'https:\\/\\/hbimg.b0.upaiyun.com\\/6925f8c2a43fb4c6bd781073239eebd951da458b5ad13-8nZ8Sg_fw658', 'https://img2.baidu.com/it/u=404361699,2148481436&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=776', 'https://img2.baidu.com/it/u=404361699,2148481436&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=776'], 'identifier': 'https://hbimg.b0.upaiyun.com/6925f8c2a43fb4c6bd781073239eebd951da458b5ad13-8nZ8Sg_fw658', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000022'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/1284714829.jpg', 'https://img0.baidu.com/it/u=3518453307,2237170288&fm=253&fmt=auto&app=138&f=JPEG?w=654&h=500', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/1284714829.jpg', 'https://img0.baidu.com/it/u=3518453307,2237170288&fm=253&fmt=auto&app=138&f=JPEG?w=654&h=500', 'https://img0.baidu.com/it/u=3518453307,2237170288&fm=253&fmt=auto&app=138&f=JPEG?w=654&h=500'], 'identifier': 'https://hellorfimg.zcool.cn/large/1284714829.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000023'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/1625850256.jpg?x-image-process=image/format,webp', 'https://img0.baidu.com/it/u=13977428,2245298674&fm=253&fmt=auto&app=138&f=JPEG?w=681&h=500', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/1625850256.jpg?x-image-process=image\\/format,webp', 'https://img0.baidu.com/it/u=13977428,2245298674&fm=253&fmt=auto&app=138&f=JPEG?w=681&h=500', 'https://img0.baidu.com/it/u=13977428,2245298674&fm=253&fmt=auto&app=138&f=JPEG?w=681&h=500'], 'identifier': 'https://hellorfimg.zcool.cn/large/1625850256.jpg?x-image-process=image/format,webp', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000024'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/2278023137.jpg', 'https://img0.baidu.com/it/u=67333205,1886979999&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=949', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/2278023137.jpg', 'https://img0.baidu.com/it/u=67333205,1886979999&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=949', 'https://img0.baidu.com/it/u=67333205,1886979999&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=949'], 'identifier': 'https://hellorfimg.zcool.cn/large/2278023137.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000025'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/1284275206.jpg?x-image-process=image/format,webp', 'https://img2.baidu.com/it/u=240572267,3438783617&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=533', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/1284275206.jpg?x-image-process=image\\/format,webp', 'https://img2.baidu.com/it/u=240572267,3438783617&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=533', 'https://img2.baidu.com/it/u=240572267,3438783617&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=533'], 'identifier': 'https://hellorfimg.zcool.cn/large/1284275206.jpg?x-image-process=image/format,webp', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000026'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/1792498645.jpg', 'https://img2.baidu.com/it/u=1368813230,1956862888&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=533', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/1792498645.jpg', 'https://img2.baidu.com/it/u=1368813230,1956862888&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=533', 'https://img2.baidu.com/it/u=1368813230,1956862888&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=533'], 'identifier': 'https://hellorfimg.zcool.cn/large/1792498645.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000027'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/1441794707.jpg', 'https://img1.baidu.com/it/u=1325956228,1122946288&fm=253&fmt=auto&app=138&f=JPEG?w=681&h=500', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/1441794707.jpg', 'https://img1.baidu.com/it/u=1325956228,1122946288&fm=253&fmt=auto&app=138&f=JPEG?w=681&h=500', 'https://img1.baidu.com/it/u=1325956228,1122946288&fm=253&fmt=auto&app=138&f=JPEG?w=681&h=500'], 'identifier': 'https://hellorfimg.zcool.cn/large/1441794707.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000028'}, 
        {'candidate_urls': ['https://hellorfimg.zcool.cn/large/790365352.jpg', 'https://img1.baidu.com/it/u=982048691,2691142154&fm=253&fmt=auto&app=138&f=JPEG?w=612&h=500', 'https:\\/\\/hellorfimg.zcool.cn\\/large\\/790365352.jpg', 'https://img1.baidu.com/it/u=982048691,2691142154&fm=253&fmt=auto&app=138&f=JPEG?w=612&h=500', 'https://img1.baidu.com/it/u=982048691,2691142154&fm=253&fmt=auto&app=138&f=JPEG?w=612&h=500'], 'identifier': 'https://hellorfimg.zcool.cn/large/790365352.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000029'}, 
        {'candidate_urls': ['https://image.made-in-china.com/226f3j00ShPqgAGtHbcz/Panda-Stuffed-Animals-Plush-Cute-Plushies-for-Animal-Themed-Parties-Teacher-Student-Award-Animal-Toys-for-Baby.jpg', 'https://img0.baidu.com/it/u=3573392075,3375140279&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=625', 'https:\\/\\/image.made-in-china.com\\/226f3j00ShPqgAGtHbcz\\/Panda-Stuffed-Animals-Plush-Cute-Plushies-for-Animal-Themed-Parties-Teacher-Student-Award-Animal-Toys-for-Baby.jpg', 'https://img0.baidu.com/it/u=3573392075,3375140279&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=625', 'https://img0.baidu.com/it/u=3573392075,3375140279&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=625'], 'identifier': 'https://image.made-in-china.com/226f3j00ShPqgAGtHbcz/Panda-Stuffed-Animals-Plush-Cute-Plushies-for-Animal-Themed-Parties-Teacher-Student-Award-Animal-Toys-for-Baby.jpg', 'work_dir': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals', 'file_path': 'tmp/BaiduImageClient/2025-11-17-01-21-12 CuteAnimals/00000030'}
    ],
    'DuckduckgoImageClient': [
        {'candidate_urls': ['https://factanimal.com/wp-content/uploads/2023/03/cute-red-panda.jpg', 'https://tse2.mm.bing.net/th/id/OIP.VfDky4sH9WXVvFdeX_3u8gHaFj?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': 'd897acdebce82be775a3e3c2fa33e3ed3a118802a47d59852e56e8424b9d62d9', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000001'}, 
        {'candidate_urls': ['https://wallpaperaccess.com/full/536212.jpg', 'https://tse1.mm.bing.net/th/id/OIP.njhyujYlPlmG0kWsDEiM1wHaEK?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': '45ca5a9ce196ca8da5bbd3fb09497f2f32f6bd801e3ba62431e489f1c2188c8e', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000002'}, 
        {'candidate_urls': ['https://wallpaperaccess.com/full/536225.jpg', 'https://tse2.mm.bing.net/th/id/OIP.-lLcfOTkjVbvL5UNwrbU7QHaGY?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': '64926ffe32f85c8745fe53227f2ffa39d3f68068c7e3c759872e6c82ace2084d', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000003'}, 
        {'candidate_urls': ['http://getwallpapers.com/wallpaper/full/4/a/5/947707-cute-baby-animals-wallpapers-1920x1080-for-samsung-galaxy.jpg', 'https://tse4.mm.bing.net/th/id/OIP.8aEA1f5eHphr2AOZIg60QgHaEK?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': 'c0c338347b941ae63fdd4eefec2e5e1a42beb9ada719ec48a945a95bc12aec00', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000004'}, 
        {'candidate_urls': ['http://getwallpapers.com/wallpaper/full/c/6/1/947646-cute-baby-animals-wallpapers-1920x1080-for-4k-monitor.jpg', 'https://tse2.mm.bing.net/th/id/OIP.GJXNE3UwRCViRKQCL8IpZQHaEK?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': '94a79e1139eb6405eb392e083a31c2e06c25464c5b4251e07a1d1d0fc3ec1e2b', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000005'}, 
        {'candidate_urls': ['https://wallpaperaccess.com/full/472834.jpg', 'https://tse3.explicit.bing.net/th/id/OIP.OxaflzR6K6NFabaHJZQBLQHaEo?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': 'b5cc01b0a1436f622955b1accbb31fcba78d089e4115b326f4234bd27d22e0d0', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000006'}, 
        {'candidate_urls': ['https://wallpapercave.com/wp/wp2698601.jpg', 'https://tse2.mm.bing.net/th/id/OIP.fwe9vMRy5BCXFQmNvUbbOwHaF6?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': '70465c66879b5586f73fe5a8df3600e4c0f56f8ac98539a003c74ae7144a3e20', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000007'}, 
        {'candidate_urls': ['http://www.pixelstalk.net/wp-content/uploads/2016/07/Cute-Baby-Animal-Backgrounds-HD.jpg', 'https://tse2.mm.bing.net/th/id/OIP.hg0L_o99bK6wVMhM1QMEzQHaEK?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': 'da606646ce37bee01dd56e1d20b32cfa4257172942e36a7ceeaa43fd29cbf13f', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000008'}, 
        {'candidate_urls': ['http://www.pixelstalk.net/wp-content/uploads/2016/07/Cute-Baby-Animal-HD-Wallpapers.jpg', 'https://tse4.mm.bing.net/th/id/OIP.llqUqM6RGqvVNpoFaSW-vwHaFj?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': '20a0e24658ea058bc85541c844d3e1cb18a5f9302e6c0f6d8e62d4983fd0f83d', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000009'}, 
        {'candidate_urls': ['https://www.pixelstalk.net/wp-content/uploads/2016/03/Cute-animal-wallpapers-hd-desktop.jpg', 'https://tse1.mm.bing.net/th/id/OIP._jSVFu5xKnj-dY9Ux9gAdgHaEo?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': '5b590ffad36b7389191ffb19bdf39ab6312bb3af67fe89338d9fc12e23e0ecfb', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000010'}, 
        {'candidate_urls': ['https://wallpapers.com/images/hd/cute-animals-ducklings-in2o609mezane8yh.jpg', 'https://tse3.mm.bing.net/th/id/OIP.BX2P4HFvCQp78DBjzsnZkgHaFu?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': '95091b744a43581d7bc56f8073fbe658df95ded3917850097690b6ddddfefac2', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000011'}, 
        {'candidate_urls': ['https://www.funoramic.com/wp-content/uploads/2017/06/34-Super-Cute-Animals-31.jpg', 'https://tse4.mm.bing.net/th/id/OIP.F7KfhUWtR0KppghotnGVmwHaH8?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': 'd0e800689e9335658034b052b4c4a558a4645437607d2c63c5d0601d87ad8af0', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000012'}, 
        {'candidate_urls': ['https://images1.wionews.com/images/wion/900x1600/2023/3/20/1679293106992_redpanda.jpg', 'https://tse2.mm.bing.net/th/id/OIP.JCtwtC15kbi-LOzP_ETC2wHaNK?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': '3d8acb3504ae63c6920ea5de228af03f30ac155bf633a9c495e191e88d176655', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000013'}, 
        {'candidate_urls': ['http://www.pixelstalk.net/wp-content/uploads/2016/03/Cute-Animal-Wallpapers-For-Desktop-Background-Full-Screen.jpg', 'https://tse2.explicit.bing.net/th/id/OIP.W-3Ild9dzIlmJtOihVk89wHaEK?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': 'c50c0a69f95db5a1cae42c0144e2368a3cdb41c946f00e5b809ae9a06297ded7', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000014'}, 
        {'candidate_urls': ['http://getwallpapers.com/wallpaper/full/8/e/1/947804-new-cute-baby-animals-wallpapers-2048x1366-for-meizu.jpg', 'https://tse4.mm.bing.net/th/id/OIP.QLm3H03EkksY_5QbS7_FIgHaE8?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': '97362cda9f7c0a75d35baccba88260dc2e7c72c55866d960ba5db1120318aebb', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000015'}, 
        {'candidate_urls': ['https://s.yimg.com/ny/api/res/1.2/EGtyL1uI1TiVskJZElLN_A--/YXBwaWQ9aGlnaGxhbmRlcjt3PTk2MDtoPTYxOQ--/https://media.zenfs.com/en/loveexploring_uk_835/05f9d10ce7e11a857058221ed7cb3810', 'https://tse1.mm.bing.net/th/id/OIP.w-IGSXBvKyHu9GwLCg_3ZQHaEx?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': '4bb3281d57fcca4692c07739d3e6df8d97d25d5e11e473dfcaa65b14366c3d8e', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000016'}, 
        {'candidate_urls': ['https://i.pinimg.com/originals/d2/ae/f7/d2aef7899b4bcc753e59af6190de085e.jpg', 'https://tse1.mm.bing.net/th/id/OIP.267Tfga4T7EtLZrsUVc7bQHaKp?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': 'e30bec6c93c8b475efc4ff1d590d7f2414c59914a0232050d4086c95ae9adaaf', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000017'}, 
        {'candidate_urls': ['https://www.reliablecounter.com/blog/wp-content/uploads/2018/06/panda.jpg', 'https://tse1.mm.bing.net/th/id/OIP.1UV4uuBiNiuFEoNcoCLnXgHaEK?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': '37f726685798517e9ab3e4d0d7f538ccd1b58542fce5c138b5c50f2b05039737', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000018'}, 
        {'candidate_urls': ['https://i2.wp.com/earthnworld.com/wp-content/uploads/2017/07/Red-Panda.jpg?ssl=1', 'https://tse4.mm.bing.net/th/id/OIP.WWdCoq0JWU4Hw4fVqsGrzwHaE5?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': 'd87e196884a1b1cdee3d2341c9f369f4e55e67a012f642595fa4846a1668ca44', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000019'}, 
        {'candidate_urls': ['https://www.pixelstalk.net/wp-content/uploads/2016/07/Cute-Baby-Animal-Background-Free-Download.jpg', 'https://tse4.mm.bing.net/th/id/OIP.lySI9slWhMpdL0NiLbzHQAHaEK?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': '40c38ba9c098c3489859399af575ff5f3e7fcdb0ac6dbaf2b1bebf3124d646a3', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000020'}, 
        {'candidate_urls': ['http://www.pixelstalk.net/wp-content/uploads/2016/03/Cute-Animal-1920x1080-wallpaper-HD.jpg', 'https://tse2.mm.bing.net/th/id/OIP.-X8GzC2pxuKfgUrILlaXhwHaEK?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': '4c251900068914f6f301bb565f150eea105208cc2306636ad348b4a05755482d', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000021'}, 
        {'candidate_urls': ['http://getwallpapers.com/wallpaper/full/5/2/e/947825-widescreen-cute-baby-animals-wallpapers-1920x1200.jpg', 'https://tse1.mm.bing.net/th/id/OIP.eL3k1RkSjZE4AYHJW3b5nwHaEo?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': 'f1f424ad06b9ed859fc6e7fa4de944cd3cd70d913976536607167a1689eb2ffa', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000022'}, 
        {'candidate_urls': ['https://www.pixelstalk.net/wp-content/uploads/2016/03/Cute-Animal-Wallpaper-HD-desktop.jpg', 'https://tse1.mm.bing.net/th/id/OIP.g8GvZl4kA1u3xtPUBvXGmAHaEK?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': '9a4ee22016e9408a01d86cc48bdd14642463b6929281a6cea1c1f8d0e8aa9fe8', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000023'}, 
        {'candidate_urls': ['https://www.pixelstalk.net/wp-content/uploads/images2/Animal-Wallpapers-Bear-Baby-Cute.jpg', 'https://tse1.mm.bing.net/th/id/OIP.FDq-oveJuhE6UeCJFcCHYgHaEo?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': '9b157b136aee3046c016ce9b237236b0e987b6ad2eec314628f343aa66d1d33b', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000024'}, 
        {'candidate_urls': ['http://www.hickerphoto.com/images/1024/pictures-f76t7426.jpg', 'https://tse4.mm.bing.net/th/id/OIP.e2xavh0T3pch8R4bmca08AHaE7?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': '0083f0db2fddd78180cd2fe9d550f9a7a31fd73d17bf76ac2b1ed891e1e2047b', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000025'}, 
        {'candidate_urls': ['http://getwallpapers.com/wallpaper/full/2/6/9/645339.jpg', 'https://tse1.mm.bing.net/th/id/OIP.IVCG-7ENHxDVEptLWevSVAHaEo?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': 'f6a1b7caa3c52eeeda43cf5c7415ba505cb7893b8e09f810ecc995cfa8b41cd0', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000026'}, 
        {'candidate_urls': ['https://wallpapercave.com/wp/wp1816915.jpg', 'https://tse4.mm.bing.net/th/id/OIP.3cJJwriO26CBgCb5FaQ80QHaEo?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': 'dbaa688b9720bb9d18aa5a239e56a5afc39b3902b64bcf3dc422e42e8be4824f', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000027'}, 
        {'candidate_urls': ['https://cdn.openart.ai/stable_diffusion/f7ea89e3d8aae70a86e32faaf4e09a49aeb371b0_2000x2000.webp', 'https://tse4.mm.bing.net/th/id/OIP.fLERB_C7ZpcBnUrj5vFPQAHaHa?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': '2c947595f98b926d00473ea07b1b26ad75482bc9df9b96142e32d4cc97620dfa', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000028'}, 
        {'candidate_urls': ['https://i.pinimg.com/originals/a6/94/c2/a694c2f6dac7497974c391c7ecb0e337.jpg', 'https://tse2.mm.bing.net/th/id/OIP.hytRnXp9YILuS2xPu3ZTZQHaI6?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': '9a4bf17b45506e4632b0afb3f3155ee0e185e6ade859da8ec0e56098dffc85e0', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000029'}, 
        {'candidate_urls': ['http://4.bp.blogspot.com/-t7X9Kh_gADM/TaPGkx7f0NI/AAAAAAAAHCo/4LwpjAeoj5k/s1600/cheetah-animal-wallpaper.jpg', 'https://tse4.mm.bing.net/th/id/OIP.c6XWplSU3XukvR2SOGWYAwHaFj?cb=ucfimg2&pid=Api&ucfimg=1'], 'identifier': '38cc8b925a93b1481d13e0bb3805b08996a3bf61493f1e9725547995dd1113fa', 'work_dir': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals', 'file_path': 'tmp/DuckduckgoImageClient/2025-11-17-01-38-43 CuteAnimals/00000030'}
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
    print(f"Query: {QUERY}")
    # iter
    for client_name, client_module in ImageClientBuilder.REGISTERED_MODULES.items():
        print(f"\n[Module] {client_name}")
        client: BaseImageClient = client_module(disable_print=False, work_dir=tmp_dir, auto_set_proxies=False)
        status = {
            "name": client_name, "search_ok": False, "download_ok": False, "ok": False, "n_results": 0,
            "n_downloaded": 0, "error": None, "downloaded_images": [], "search_samples": [],
        }
        target_dir: Path = base_results_dir / client_name
        # --search checking
        try:
            if client_name in ['BaiduImageClient', 'DuckduckgoImageClient'] and runningingithubactions():
                image_infos = SEARCH_SUPPLEMENT[client_name]
            else:
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