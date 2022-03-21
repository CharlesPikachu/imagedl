'''
Function:
    IO相关的工具函数
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import json


'''新建文件夹'''
def touchdir(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)
        return False
    return True


'''导入配置文件'''
def loadconfig(filepath='config.json'):
    fp = open(filepath, 'r', encoding='utf-8')
    return json.load(fp)