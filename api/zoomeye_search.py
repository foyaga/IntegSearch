# -*- coding = utf-8 -*-
# @Time  : 2022/11/4 11:23
# @Author: Ifory
# @File  : zoomeye.py

from zoomeye.sdk import ZoomEye

from config.configfile import config
from module.Finger.config.data import logging


class ZOOMEYE:
    def __init__(self):
        self.zoomeye_api = config['zoomeye']['apiKey']

    def run(self, keyword, size):
        global api
        datass = []
        if size % 20 == 0:
            page = size // 20
        else:
            page = size // 20 + 1
        try:
            api = ZoomEye(api_key=self.zoomeye_api)
            logging.info(f"zoomeye本月剩余：{api.resources_info()['resources']['search']}")
        except ValueError:
            logging.error("zoomeye api不可用，请检查配置是否正确！")
            exit(0)
        try:
            api.multi_page_search(keyword, page, resource="host")
            number = api.show_count()
            datas = api.dork_filter("ip,port,service,country")
            logging.info(f"查询关键词为：{keyword}")
            logging.info(f"查询引擎为：zoomeye")
            logging.info(f"查询结果数量：{number}")
            logging.info(f"获取数量为：{len(datas)}")
            logging.info(f"查询页数为：{page}")

            for data in datas:
                if "*" in data[3]:
                    continue
                if "https" in data[2]:
                    host = "https://" + data[0] + ":" + str(data[1])
                elif 'http' in data[2]:
                    host = "http://" + data[0] + ":" + str(data[1])
                else:
                    host = data[0] + ":" + str(data[1])
                domain = ""
                title = ""
                datass.append((host, data[0], data[1], data[2], data[3], domain, title, keyword))
            return datass
        except ValueError:
            logging.error("未查询到结果")
