# -*- coding = utf-8 -*-
# @Time  : 2022/11/4 11:27
# @Author: Ifory
# @File  : hunter.py
import base64
import json

import requests

from config.configfile import config
from module.Finger.config.data import logging


class HUNTER:
    def __init__(self):
        self.hunter_api = config['hunter']['apiKey']
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def run(self, keyword, page, size):
        datas = []
        search = str(base64.urlsafe_b64encode(keyword.encode("utf-8")), 'utf8')
        url = f"https://hunter.qianxin.com/openApi/search?api-key={self.hunter_api}&search={search}&page={page}&page_size={size}&is_web=3"

        req = requests.get(url, headers=self.headers)
        rsp = json.loads(req.text)
        if rsp['code'] != 200 and rsp['code'] != 40205:
            logging.error(rsp)
            if rsp['code'] == 40204:
                exit(0)
            return False
        consume_quota = rsp['data']['consume_quota']
        rest_quota = rsp['data']['rest_quota']
        logging.info(f"查询关键词为：{keyword}")
        logging.info(f"查询引擎为：hunter")
        logging.info(f"查询结果数量：{rsp['data']['total']}")
        logging.info(f"查询数量为：{size}")
        logging.info(f"查询页数为：{page}")
        logging.info((consume_quota, rest_quota))
        if rsp['data']['arr']:
            for arr in rsp['data']['arr']:
                url = arr['url']
                ip = arr['ip']
                port = arr['port']
                title = arr['web_title']
                if len(title) > 30:
                    title = title[:30] + "..."
                protocol = arr['protocol']
                country = arr['country']
                domain = ""
                datas.append((url, ip, port, protocol, country, domain, title, keyword))
            return datas
