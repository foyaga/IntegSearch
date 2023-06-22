# -*- coding = utf-8 -*-
# @Time  : 2022/11/4 11:21
# @Author: Ifory
# @File  : shodan.py

import shodan

from config.configfile import config
from module.Finger.config.data import logging


class SHADAN:
    def __init__(self):
        self.shodan_api = config['shodan']['apiKey']

    def run(self, keyword, page, size):
        datas = []
        api = shodan.Shodan(self.shodan_api)
        try:
            pages = size // 100
            count = 0
            for i in range(1, pages + 2):
                results = api.search(keyword, page=page)
                if i == 1:
                    logging.info(f"查询关键词为：{keyword}")
                    logging.info(f"查询引擎为：shodan")
                    logging.info(f"查询结果数量：{len(results['matches'])}")
                    logging.info(f"查询数量为：{size}")
                    logging.info(f"查询页数为：{page}")
                for result in results['matches']:
                    if count == size:
                        break
                    else:
                        count += 1
                    hostnames = ""
                    ip = result['ip_str']
                    port = result['port']
                    country = result['location']['country_name']
                    try:
                        product = result['product']
                    except KeyError:
                        product = ""
                    try:
                        title = result['http']['title'].strip()
                        if len(title) > 30:
                            title = title[:30] + "..."
                    except KeyError:
                        title = ""
                    except TypeError:
                        title = ""
                    except AttributeError:
                        title = ""

                    if title and ("HTTPS" in title or port == 443):
                        host = "https://" + ip + ":" + str(port)
                    else:
                        host = ip + ":" + str(port)
                    datas.append((host, ip, port, product, country, hostnames, title, keyword))
                return datas
        except shodan.exception.APIError as e:
            logging.error(e)
            logging.error("shodan api请求出错！")
            exit(0)
