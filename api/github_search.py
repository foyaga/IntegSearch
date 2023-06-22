# -*- coding = utf-8 -*-
# @Time  : 2023/4/1 19:01
# @Author: Ifory
# @File  : github_search.py
import datetime
import json

import requests
from prettytable import PrettyTable

from config.configfile import config
from module.Finger.config.data import logging


class GitHub(object):
    def __init__(self):
        try:
            self.proxies = json.loads(config['github']['proxies'])
        except Exception as e:
            logging.warning("代理配置异常")
            self.proxies = ''
        self.token = config['github']['token']
        if not self.token:
            logging.error("token配置错误")
            exit(1)
        self.headers = {'Authorization': 'Bearer ' + self.token,
                        "Accept": "application / vnd.github.v3 + json",
                        }


    def run(self, keyword, size, sort):
        if size <= 0:
            logging.error('获取数量错误')
            return False
        total_count = self.get_total_count(keyword)
        if size > total_count:
            size = total_count
        result = []
        items = []
        num = size // 100
        if not num:
            n = 1
        else:
            n = num + 1
            s = 100
        for page in range(n):
            if page == n - 1:
                s = size % 100
                if not s:
                    break
            url = f"https://api.github.com/search/repositories?" \
                  f"q={keyword}&page={page}&per_page={s}&sort={sort}"
            try:
                res = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=10).json()
                items.extend(res['items'])
            except requests.exceptions.ConnectionError:
                logging.error("请求超时,请检查代理或网络")
                exit(0)
            except Exception as e:
                logging.error(f"获取失败{e}")
                exit(0)

        logging.info(f"查询关键词为：{keyword}")
        logging.info(f"查询引擎为：github")
        logging.info(f"查询结果数量：{total_count}")
        logging.info(f"获取数量为：{size}")

        for data in items:
            stargazers_count = data['stargazers_count']
            forks_count = data['forks_count']
            language = data['language']
            pushed_at = datetime.datetime.strptime(data['pushed_at'], '%Y-%m-%dT%H:%M:%SZ')
            clone_url = data['clone_url']
            try:
                description = data['description']
                if len(description) > 50:
                    description = description[:50] + "..."
            except AttributeError:
                description = ""
            result.append((stargazers_count, forks_count, language, pushed_at, clone_url, description))

        self.show(result)

    def get_total_count(self, keyword):
        try:
            url = f"https://api.github.com/search/repositories?q={keyword}&page=1&per_page=1"
            res = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=10).json()
            total_count = res['total_count']
            return total_count
        except requests.exceptions.ConnectionError:
            logging.error("请求超时,请检查代理或网络")
            exit(0)
        except Exception as e:
            logging.error(f"获取失败,请检查token是否正确")
            logging.error(res)
            exit(0)

    def show(self, result):
        table = PrettyTable(['Star', 'Fork', 'language', 'update_time', 'clone_url', 'description'])
        table.align = 'l'
        for res in result:
            table.add_row([res[0], res[1], res[2], res[3], res[4], res[5]])
        print(table)
