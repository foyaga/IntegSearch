# -*- coding = utf-8 -*-
# @Time  : 2022/12/28 16:33
# @Author: Ifory
# @File  : quake_search.py
import json

import requests

from config.configfile import config
from module.Finger.config.data import logging


class QUAKE:
    def __init__(self):
        self.quake_api = config['quake']['apiKey']

    def run(self, keyword, page, size):
        datas = []
        try:
            headers = {'Content-Type': 'application/json', "X-QuakeToken": self.quake_api}
            data = {"query": keyword, "start": page, "size": size}
            url = "https://quake.360.cn/api/v3/search/quake_service"

            req = requests.post(url, headers=headers, json=data)
            rsp = json.loads(req.text)
            if rsp['code'] != 0:
                logging.error(rsp)
                exit(0)
            number = rsp['meta']['pagination']['total']
            logging.info(f"查询关键词为：{keyword}")
            logging.info(f"查询引擎为：quake")
            logging.info(f"查询结果数量：{number}")
            logging.info(f"查询数量为：{size}")
            logging.info(f"查询页数为：{page}")

            for j in range(len(rsp['data'])):
                ip = rsp['data'][j]['ip']
                port = rsp['data'][j]['port']
                try:
                    title = rsp['data'][j]['service']['http']['title'].strip().replace(' ', '').replace('|', '')
                    if len(title) > 30:
                        title = title[:30   ] + "..."
                except KeyError:
                    title = ''
                country = rsp['data'][j]['location']['country_cn']
                try:
                    hostname = rsp['data'][j]['domain']
                except KeyError:
                    hostname = rsp['data'][j]['hostname']
                host = ip + ":" + str(port)
                protocol = rsp['data'][j]['service']['name']
                datas.append((host, ip, port, protocol, country, hostname, title, keyword))
            return datas
        except ValueError:
            logging.error("quake api不可用，请检查配置是否正确！")
        except KeyError:
            logging.error("搜索语法错误！")
