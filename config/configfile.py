# -*- coding = utf-8 -*-
# @Time  : 2022/11/4 11:28
# @Author: Ifory
# @File  : configfile.py
import yaml

try:
    with open('config.yaml', 'r', encoding='utf8') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
except FileNotFoundError:
    print('配置文件不存在，请检查配置文件路径！')
    exit()
