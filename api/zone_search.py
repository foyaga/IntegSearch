# -*- coding = utf-8 -*-
# @Time  : 2023/6/15 16:23
# @Author: Ifory
# @File  : zone_search.py

import json

import requests

from config.configfile import config
from module.Finger.config.data import logging


class Zone:
    def __init__(self):
        self.hunter_api = config['zone']['apiKey']
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def run(self, keyword, page, size):
        datas = []
        url = "https://0.zone/api/data/"
        data = {
            "query": keyword,
            "query_type": "site",
            "page": page,
            "pagesize": size,
            "zone_key_id": self.hunter_api
        }
        try:
            req = requests.post(url, json=data, headers=self.headers, timeout=10)
            if req.status_code != 200:
                logging.error("请求错误")
                return False
            req_dict = json.loads(req.text)
            code = req_dict['code']
            if code != 0:
                logging.error(req_dict)
                return False
            data = req_dict['data']
            logging.info(f"查询关键词为：{keyword}")
            logging.info(f"查询引擎为：zone(零零信安)")
            logging.info(f"查询结果数量：{len(data)}")
            logging.info(f"查询数量为：{size}")
            logging.info(f"查询页数为：{page}")
            for i in range(0, len(data)):
                HOST = data[i]['url']
                ip = data[i]['ip']
                port = data[i]['port']
                protocol = data[i]['service']
                country = data[i]['country']
                domain = HOST.split(':')[1].replace('/', '')
                try:
                    title = data[i]['title']
                    if len(title) > 30:
                        title = title[:30] + "..."
                except KeyError:
                    title = ''
                datas.append((HOST, ip, port, protocol, country, domain, title, keyword))
            return datas
        except requests.exceptions.ReadTimeout:
            logging.error("请求超时")
            exit(0)
