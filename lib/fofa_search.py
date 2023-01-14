import base64
import json
import os
import random
import time
from urllib.parse import quote

import requests
import xlwt
from prettytable import PrettyTable

from config import config
from lib.Finger import Finger
from lib.Finger.config.data import logging

class Fofa:
    def __init__(self):
        self.email = config.fofa_email
        self.key = config.fofa_key
        self.headers = {
            "User-Agent": random.choice(config.user_agents)
        }
        self.now_time = time.strftime("%Y%m%d%H%M%S")
        if not self.check():
            logging.error("fofa api不可用，请检查配置是否正确！")
            exit(0)

    def run(self, keyword1, page, size, output, finger):
        keyword = quote(str(base64.b64encode(keyword1.encode()), encoding='utf-8'))
        url = f"https://fofa.info/api/v1/search/all?email={self.email}&key={self.key}&qbase64={keyword}&full=false&fields=host,ip,port,protocol,country_name,title&size={size}&page={page}"
        try:
            response = requests.get(url, timeout=10, headers=self.headers)
            datas = json.loads(response.text)

            logging.info(f"查询关键词为：{keyword1}")
            logging.info(f"查询结果数量：{datas['size']}")
            logging.info(f"获取数量为：{size}")
            logging.info(f"查询页数为：{page}")

            self.show_results(datas, finger, output)

            if output and datas["results"]:
                self.save_excel(datas, keyword1)

        except requests.exceptions.ReadTimeout:
            logging.error("请求超时")
        except requests.exceptions.ConnectionError:
            logging.error("网络超时")
        except json.decoder.JSONDecodeError:
            logging.error("获取失败，请重试")
        except Exception as e:
            logging.error(f"获取失败{e}")

    def show_results(self, datas, finger, output):
        hosts = []
        table = PrettyTable(['HOST', 'IP', '端口', '协议', '国家', '标题'])
        table.align = 'l'

        for i in range(len(datas["results"])):
            data = datas["results"][i]
            title = data[5].strip()[:30]
            host = "http://"+data[0] if data[3] == 'http' else data[0]
            hosts.append(host)
            table.add_row([host, data[1], data[2], data[3], data[4], title])
        print(table)
        if finger:
            Finger.main(hosts, output)

    def check(self):
        try:
            if self.email and self.key:
                auth_url = "https://fofa.info/api/v1/info/my?email={0}&key={1}".format(self.email, self.key)
                response = requests.get(auth_url, timeout=10, headers=self.headers)
                if self.email in response.text:
                    return True
                else:
                    return False
            else:
                return False
        except:
            return False

    def save_excel(self, datas, keyword):
        keyword = keyword.replace(":", "")[:30]
        File_Found = xlwt.Workbook(encoding='utf-8')  # 工作簿
        File_Sheet = File_Found.add_sheet(keyword, cell_overwrite_ok=True)  # 工作表
        File_Sheet.set_panes_frozen('1')  # 设置冻结为真
        File_Sheet.set_horz_split_pos(1)  # 水平冻结
        my_style = xlwt.XFStyle()
        alignment = xlwt.Alignment()
        alignment.horz = 0x01
        alignment.vert = 0x01
        my_style.alignment = alignment
        font = xlwt.Font()
        font.bold = True
        style_font = xlwt.XFStyle()
        style_font.font = font
        File_Sheet.col(0).width = 256 * 30
        File_Sheet.col(1).width = 256 * 20
        File_Sheet.col(2).width = 256 * 20
        File_Sheet.col(3).width = 256 * 20
        File_Sheet.col(4).width = 256 * 20
        File_Sheet.col(5).width = 256 * 40
        col = ('HOST', 'IP', '端口', '协议', '国家', '标题')

        for i in range(len(datas["results"])):
            data = datas["results"][i]
            for k in range(0, 6):
                File_Sheet.write(0, k, col[k], style_font)
                if k == 0:
                    host = "http://" + data[0] if data[3] == "http" else data[0]
                    File_Sheet.write(i + 1, k, host)
                elif k == 5:
                    title = data[5].strip()
                    File_Sheet.write(i + 1, k, title)
                elif k == 2:
                    File_Sheet.write(i + 1, k, int(data[k]), my_style)
                else:
                    File_Sheet.write(i + 1, k, data[k])

        if not os.path.exists("result"):
            os.mkdir("result")
        File_Found.save(f"result/fofa_{self.now_time}.xls")
        logging.info(f'fofa搜索结果文件输出路径为:result/fofa_{self.now_time}.xls')
