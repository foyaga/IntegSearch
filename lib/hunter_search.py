# -*- coding = utf-8 -*-
# @Time  : 2022/11/4 11:27
# @Author: Ifory
# @File  : hunter.py
import base64
import json
import os
import random
import time

import requests
import xlwt
from prettytable import PrettyTable

from config import config
from lib.Finger import Finger
from lib.Finger.config.data import logging

class HUNTER:
    def __init__(self):
        self.hunter_api = config.hunter_api
        self.now_time = time.strftime("%Y%m%d%H%M%S")
        self.headers = {
            "User-Agent": random.choice(config.user_agents)
        }

    def run(self, keyword, page, size, output, finger):
        datas = []
        search = str(base64.urlsafe_b64encode(keyword.encode("utf-8")), 'utf8')
        url = f"https://hunter.qianxin.com/openApi/search?api-key={self.hunter_api}&search={search}&page={page}&page_size={size}&is_web=3"

        req = requests.get(url, headers=self.headers)
        rsp = json.loads(req.text)
        if rsp['code'] != 200:
            print(rsp)
            exit(0)
        consume_quota = rsp['data']['consume_quota']
        rest_quota = rsp['data']['rest_quota']
        logging.info(f"查询关键词为：{keyword}")
        logging.info(f"查询结果数量：{rsp['data']['total']}")
        logging.info(f"查询数量为：{size}")
        logging.info(f"查询页数为：{page}")
        logging.info((consume_quota, rest_quota))
        if rsp['data']['arr']:
            for arr in rsp['data']['arr']:
                # print(arr)
                url = arr['url']
                ip = arr['ip']
                port = arr['port']
                title = arr['web_title'][20:]
                protocol = arr['protocol']
                country = arr['country']
                datas.append((url, ip, port, protocol, country, title))

            self.show_results(datas, finger, output)
            if output:
                self.save_excel(datas, keyword)
        else:
            logging.error("未查询到结果")

    def show_results(self, datas, finger, output):
        hosts = []
        table = PrettyTable(['URL', 'IP', '端口', '协议', '国家', '标题'])
        table.align = 'l'

        for data in datas:
            hosts.append(data[0])
            table.add_row([data[0], data[1], data[2], data[3], data[4], data[5]])
        print(table)
        if finger:
            Finger.main(hosts, output)

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
        File_Sheet.col(0).width = 256 * 40
        File_Sheet.col(1).width = 256 * 20
        File_Sheet.col(2).width = 256 * 20
        File_Sheet.col(3).width = 256 * 20
        File_Sheet.col(4).width = 256 * 20
        File_Sheet.col(5).width = 256 * 50
        col = ('URL', 'IP', '端口', '协议', '国家', '标题')

        for i in range(len(datas)):
            data = datas[i]
            for k in range(0, 6):
                File_Sheet.write(0, k, col[k], style_font)
                File_Sheet.write(i + 1, k, data[k], my_style)

        if not os.path.exists("result"):
            os.mkdir("result")
        File_Found.save(f"result/hunter_{self.now_time}.xls")
        logging.info(f'hunter搜索结果文件输出路径为:result/hunter_{self.now_time}.xls')
