#!/usr/bin/env python
# -*- coding: utf-8 -*-
from module.Finger.config.data import Urls


class initoptions:
    def __init__(self, result):
        self.key = ["\"", "“", "”", "\\", "'"]
        Urls.url = []
        self.result = result
        # 查询顺序非常重要不能随便移动位置
        if self.result:
            self.check()

    def check(self):
        for res in self.result:
            url = res[0]
            for key in self.key:
                if key in url:
                    url = url.replace(key, "")
            if not url.startswith('http') and url:
                # 若没有http头默认同时添加上http与https到目标上
                Urls.url.append("http://" + str(url))
                Urls.url.append("https://" + str(url))
            elif url:
                Urls.url.append(url)
