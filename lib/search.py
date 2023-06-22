# -*- coding = utf-8 -*-
# @Time  : 2023/4/1 15:20
# @Author: Ifory
# @File  : search.py.py
from api import fofa_search, hunter_search, quake_search, shodan_search, zoomeye_search, github_search, zone_search
from config.configfile import config
from lib import process


class Search:
    def __init__(self, args, keyword=None):
        self.args = args
        self.page = args.page if args.page else config['base']['page']
        self.size = args.size if args.size else config['base']['size']
        self.keyword = keyword if keyword else args.keyword

        if args.type == "fofa":
            result = fofa_search.Fofa().run(self.keyword, self.page, self.size)
            if result:
                self.modular(result)
        elif args.type == "shodan":
            result = shodan_search.SHADAN().run(self.keyword, self.page, self.size)
            if result:
                self.modular(result)
        elif args.type == "zoomeye":
            result = zoomeye_search.ZOOMEYE().run(self.keyword, self.size)
            if result:
                self.modular(result)
        elif args.type == "quake":
            result = quake_search.QUAKE().run(self.keyword, self.page, self.size)
            if result:
                self.modular(result)
        elif args.type == "hunter":
            result = hunter_search.HUNTER().run(self.keyword, self.page, self.size)
            if result:
                self.modular(result)
        elif args.type == "zone":
            result = zone_search.Zone().run(self.keyword, self.page, self.size)
            if result:
                self.modular(result)
        elif args.type == "github":
            github_search.GitHub().run(self.keyword, self.size, args.gitsort)
        else:
            print('搜索引擎类型输入有误！')

    def modular(self, result):
        """输出"""
        data = process.Process(result, self.keyword, self.args.type)
        data.showScreen()  # 屏幕打印
        if self.args.output:
            data.saveExcel(self.args.output)  # excel保存
        if self.args.db:  # mysql数据库保存
            data.saveDatabase()
        if self.args.finger:  # finger调用
            data.finger(self.args.output)
