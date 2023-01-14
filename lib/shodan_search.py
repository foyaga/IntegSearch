# -*- coding = utf-8 -*-
# @Time  : 2022/11/4 11:21
# @Author: Ifory
# @File  : shodan.py

import os
import time

import shodan
import xlwt
from prettytable import PrettyTable

from config import config
from lib.Finger import Finger
from lib.Finger.config.data import logging


class SHADAN:
    def __init__(self):
        self.shodan_api = config.shodan_api
        self.now_time = time.strftime("%Y%m%d%H%M%S")

    def run(self, keyword, page, size, output, finger):
        datas = []
        api = shodan.Shodan(self.shodan_api)
        try:
            pages = size // 100
            count = 0
            for i in range(1, pages+2):
                results = api.search(keyword, page=page)
                # print(results)
                if i == 1:
                    logging.info(f"查询关键词为：{keyword}")
                    logging.info(f"查询结果数量：{results['total']}")
                    logging.info(f"查询页数为：{page}")
                for result in results['matches']:
                    if count == size:
                        break
                    else:
                        count += 1
                    hostnames = result['hostnames']
                    ip = result['ip_str']
                    port = result['port']
                    country = result['location']['country_name']
                    try:
                        product = result['product']
                    except KeyError:
                        product = ""
                    try:
                        title = result['http']['title'].strip()[:20]
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
                    datas.append((host, ip, port, product, country, title, hostnames))

            self.show_results(datas, finger, output)

            if output and datas:
                self.save_excel(datas, keyword)
        except shodan.exception.APIError as e:
            print(e)
            logging.error("shodan api请求出错！")

    def show_results(self, datas, finger, output):
        hosts = []
        logging.info(f'获取数量为：{len(datas)}')
        table = PrettyTable(['HOST', 'IP', '端口', '产品', '国家', '标题'])
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
        File_Sheet.col(0).width = 256 * 30
        File_Sheet.col(1).width = 256 * 20
        File_Sheet.col(2).width = 256 * 20
        File_Sheet.col(3).width = 256 * 30
        File_Sheet.col(4).width = 256 * 20
        File_Sheet.col(5).width = 256 * 40
        File_Sheet.col(6).width = 256 * 30
        col = ('HOST', 'IP', '端口', '产品', '国家', '标题', '域名')

        for i in range(len(datas)):
            data = datas[i]
            for k in range(0, 7):
                File_Sheet.write(0, k, col[k], style_font)
                File_Sheet.write(i + 1, k, data[k], my_style)

        if not os.path.exists("result"):
            os.mkdir("result")
        File_Found.save(f"result/shodan_{self.now_time}.xls")
        logging.info(f'shodan搜索结果文件输出路径为:result/shodan_{self.now_time}.xls')
