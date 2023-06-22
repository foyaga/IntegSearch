# -*- coding = utf-8 -*-
# @Time  : 2023/2/6 15:21
# @Author: Ifory
# @File  : cmdline.py
# IntegSearch

import argparse
import time


def banner():
    print(r"""
=====================================================================  
Search keywords in fofa, shodan, hunter, zoomeye, quake, zone、github
 ___       _             ____                      _     
|_ _|_ __ | |_ ___  __ _/ ___|  ___  __ _ _ __ ___| |__  
 | || '_ \| __/ _ \/ _` \___ \ / _ \/ _` | '__/ __| '_ \ 
 | || | | | ||  __/ (_| |___) |  __/ (_| | | | (__| | | |
|___|_| |_|\__\___|\__, |____/ \___|\__,_|_|  \___|_| |_|
                   |___/                                 
                                                         by:Ifory885
===================================================================== 
    """)


class CustomAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, " ".join(values))


def parse_args():
    parser = argparse.ArgumentParser(
        prog="python main.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        exit_on_error=False,
        add_help=False)

    # 基础查询相关参数
    target = parser.add_argument_group('target')
    target.add_argument("-t", "--type",
                        help="搜索引擎类型(fofa|shodan|zoomeye|quake|hunter|zone|github)[注:查看指定搜索引擎语法-t]")
    target.add_argument("-k", "--keyword", action=CustomAction, type=str, nargs='+', help="查询语法")
    target.add_argument("-p", "--page", type=int, help="查询结果页数(default:1)")
    target.add_argument("-s", "--size", type=int, help="查询结果数量(default:10)")
    target.add_argument("-f", "--file", help="通过txt文件导入搜索语法")
    target.add_argument("-gs", "--gitsort", type=str,
                        help="github匹配模式(stars|forks|updated|best match)[default:best match]")

    # 其他功能相关参数
    other = parser.add_argument_group('other')
    other.add_argument("-fi", "--finger", action="store_true", default=False, help="是否调用finger进行指纹识别(default:False)")

    # 结果输出相关参数
    output = parser.add_argument_group('output')
    output.add_argument("-oe", "--output", default=False, nargs='?',
                        const=time.strftime('%Y%m%d%H%M%S', time.localtime()), help="结果是否导出excel(default:False)")
    output.add_argument("-od", "--db", action="store_true", default=False, help="结果是否导入数据库(default:False)")

    help = parser.add_argument_group('help')
    help.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='查看程序使用帮助')
    return parser
