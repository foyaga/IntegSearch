import base64
import json
import time
from urllib.parse import quote

import requests

from config.configfile import config
from module.Finger.config.data import logging


class Fofa:
    def __init__(self):
        self.email = config['fofa']['email']
        self.key = config['fofa']['key']
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        self.sign = True

    def run(self, keyword1, page, size):
        result = []
        keyword = quote(str(base64.b64encode(keyword1.encode()), encoding='utf-8'))
        url = f"https://fofa.info/api/v1/search/all" \
              f"?email={self.email}&key={self.key}&qbase64={keyword}&full=false&fields=host,ip,port,protocol,country_name,domain,title&size={size}&page={page}"
        while True:
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                datas = json.loads(response.text)
                is_error = datas['error']
                if is_error:
                    logging.error(datas)
                    exit(0)

                logging.info(f"查询关键词为：{keyword1}")
                logging.info(f"查询引擎为：fofa")
                logging.info(f"查询结果数量：{datas['size']}")
                logging.info(f"获取数量为：{size}")
                logging.info(f"查询页数为：{page}")

                for i in range(len(datas["results"])):
                    data = datas["results"][i]
                    title = data[6].strip()
                    if len(title) > 30:
                        title = title[:30] + "..."
                    host = "http://" + data[0] if data[3] == 'http' else data[0]
                    port = int(data[2])
                    result.append((host, data[1], port, data[3], data[4], data[5], title, keyword1))
                break
            except requests.exceptions.ReadTimeout:
                logging.error("请求超时")
            except requests.exceptions.ConnectionError:
                logging.error("网络超时")
            except json.decoder.JSONDecodeError:
                logging.error("获取失败，请重试")
            except Exception as e:
                logging.error(f"获取失败{e}")
            if self.sign:
                self.sign = False
            else:
                exit(0)
            time.sleep(5)
        return result
