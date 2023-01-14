# -*- coding = utf-8 -*-
# @Time  : 2022/12/28 16:33
# @Author: Ifory
# @File  : quake_search.py
import json
import os
import time

import requests
import xlwt
from prettytable import PrettyTable

from config import config
from lib.Finger import Finger
from lib.Finger.config.data import logging

class QUAKE:
    def __init__(self):
        self.quake_api = config.quake_api
        self.now_time = time.strftime("%Y%m%d%H%M%S")

    def run(self, keyword, page, size, output, finger):
        datas = []
        try:
            headers = {'Content-Type': 'application/json', "X-QuakeToken": self.quake_api}
            data = {"query": keyword, "start": page, "size": size}
            url = "https://quake.360.cn/api/v3/search/quake_service"

            req = requests.post(url, headers=headers, json=data)
            rsp = json.loads(req.text)
            number = rsp['meta']['pagination']['total']
            logging.info(f"查询关键词为：{keyword}")
            logging.info(f"查询结果数量：{number}")
            logging.info(f"查询页数为：{page}")

            for j in range(len(rsp['data'])):
                # print(rsp['data'])
                ip = rsp['data'][j]['ip']
                port = rsp['data'][j]['port']
                try:
                    title = rsp['data'][j]['service']['http']['title'].strip().replace(' ', '').replace('|', '')[:25]
                except KeyError:
                    title = ''
                country = rsp['data'][j]['location']['country_cn']

                hostname = rsp['data'][j]['hostname']
                host = ip + ":" + str(port)
                # print(host,ip,port,country,hostname,title)
                datas.append((host, ip, port, country, hostname, title))

            self.show_results(datas, finger, output)
            if output and datas:
                self.save_excel(datas, keyword)
        except ValueError:
            logging.error("quake api不可用，请检查配置是否正确！")
        except KeyError:
            logging.error("搜索语法错误！")


    def show_results(self, datas, finger, output):
        logging.info(f'获取结果数量：{len(datas)}')
        hosts = []
        table = PrettyTable(['HOST', 'IP', '端口', '国家', '域名', '标题'])
        table.align = 'l'

        for data in datas:
            hosts.append(data[4])
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
        File_Sheet.col(0).width = 256 * 30
        File_Sheet.col(1).width = 256 * 20
        File_Sheet.col(2).width = 256 * 20
        File_Sheet.col(3).width = 256 * 20
        File_Sheet.col(4).width = 256 * 20
        File_Sheet.col(5).width = 256 * 50
        col = ('HOST', 'IP', '端口', '国家', '域名', '标题')

        for i in range(len(datas)):
            data = datas[i]
            for k in range(0, 6):
                File_Sheet.write(0, k, col[k], style_font)
                File_Sheet.write(i + 1, k, data[k], my_style)

        if not os.path.exists("result"):
            os.mkdir("result")
        File_Found.save(f"result/quake_{self.now_time}.xls")
        logging.info(f'quake搜索结果文件输出路径为:result/quake_{self.now_time}.xls')
