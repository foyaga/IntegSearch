# -*- coding = utf-8 -*-
# @Time  : 2022/11/4 11:23
# @Author: Ifory
# @File  : zoomeye.py
import os
import time

import xlwt
from prettytable import PrettyTable
from zoomeye.sdk import ZoomEye

from config import config
from lib.Finger import Finger
from lib.Finger.config.data import logging


class ZOOMEYE:
    def __init__(self):
        self.zoomeye_api = config.zoomeye_api
        self.now_time = time.strftime("%Y%m%d%H%M%S")

    def run(self, keyword, page, output, finger):
        global api
        datass = []
        try:
            api = ZoomEye(api_key=self.zoomeye_api)
            logging.info(f"zoomeye本月剩余：{api.resources_info()['resources']['search']}")
        except ValueError:
            logging.error("zoomeye api不可用，请检查配置是否正确！")
            exit(0)
        try:
            api.multi_page_search(keyword, page, resource="host")
            number = api.show_count()
            logging.info(f"查询关键词为：{keyword}")
            logging.info(f"查询结果数量：{number}")

            datas = api.dork_filter("ip,port,service,country")
            for data in datas:
                if "https" in data[2]:
                    host = "https://" + data[0] + ":" + str(data[1])
                elif 'http' in data[2]:
                    host = "http://" + data[0] + ":" + str(data[1])
                else:
                    host = data[0] + ":" + str(data[1])
                datass.append((host, data[0], data[1], data[2], data[3]))
            self.show_results(datass, finger, output)
            if output:
                self.save_excel(datass, keyword)
        except ValueError:
            logging.error("未查询到结果")


    def show_results(self, datas, finger, output):
        hosts = []
        logging.info(f'获取结果数量：{len(datas)}')
        table = PrettyTable(['HOST', 'IP', '端口', '协议', '国家'])
        table.align = 'l'

        for data in datas:
            hosts.append(data[0])
            table.add_row([data[0], data[1], data[2], data[3], data[4]])
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
        col = ('HOST', 'IP', '端口', '协议', '国家')

        for i in range(len(datas)):
            data = datas[i]
            for k in range(0, 5):
                File_Sheet.write(0, k, col[k], style_font)
                File_Sheet.write(i + 1, k, data[k], my_style)

        if not os.path.exists("result"):
            os.mkdir("result")
        File_Found.save(f"result/zoomeye_{self.now_time}.xls")
        logging.success(f'zoomeye搜索结果文件输出路径为:result/zoomeye_{self.now_time}.xls')
