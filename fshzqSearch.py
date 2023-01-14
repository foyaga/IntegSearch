import argparse

from config import query_syntax
from lib import fofa_search
from lib import hunter_search
from lib import quake_search
from lib import shodan_search
from lib import zoomeye_search


class CustomAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, " ".join(values))


def parse_args():
    parser = argparse.ArgumentParser(
        prog="python fshzqSearch.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        exit_on_error=False,
        add_help=False)
    parser.add_argument("-t", "--type", help="搜索引擎类型(fofa|shodan|zoomeye|quake|hunter)")
    parser.add_argument("-k", "--keyword", action=CustomAction, type=str, nargs='+', help="查询语法")
    parser.add_argument("-p", "--page", default=1, type=int, help="查询结果页数(default:1)")
    parser.add_argument("-s", "--size", default=10, type=int, help="查询结果数量(default:10)")
    parser.add_argument("-g", "--finger", action="store_true", default=False, help="是否调用finger进行指纹识别(default:False)")
    parser.add_argument("-f", "--file", help="通过txt文件导入搜索语法")
    parser.add_argument("-o", "--output", action="store_true", default=False, help="结果是否导出excel(default:False)")
    parser.add_argument("-q", "--query", help="查看指定搜索引擎语法")
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='查看程序使用帮助')
    return parser


def banner():
    print(r"""
=====================================================================  
Search keywords in fofa, shodan, hunter, zoomeye, quake
 ______   ______   ___   ___     ______  ______        
/_____/\ /_____/\ /__/\ /__/\   /_____/\/_____/\       
\::::_\/_\::::_\/_\::\ \\  \ \  \:::__\/\:::_ \ \      
 \:\/___/\\:\/___/\\::\/_\ .\ \    /: /  \:\ \ \ \_    
  \:::._\/ \_::._\:\\:: ___::\ \  /::/___ \:\ \ /_ \   
   \:\ \     /____\:\\: \ \\::\ \/_:/____/\\:\_-  \ \  
    \_\/     \_____\/ \__\/ \::\/\_______\/ \___|\_\_/ SEARCH
                                                       
https://github.com/Ifory885/fshzqSearch            by:Ifory
===================================================================== 
    """)

def run(args):
    if args.query:
        query_syntax.query_syntax(args.query)
    else:
        if args.file:
            with open(f"{args.file}", 'r', encoding='utf-8') as f:
                for k in f.readlines():
                    keyword = k.strip()
                    if args.type == "fofa":
                        fofa_search.Fofa().run(keyword, args.page, args.size, args.output, args.finger)
                    elif args.type == "shodan":
                        shodan_search.SHADAN().run(keyword, args.page, args.size, args.output, args.finger)
                    elif args.type == "zoomeye":
                        zoomeye_search.ZOOMEYE().run(keyword, args.page, args.output, args.finger)
                    elif args.type == "quake":
                        quake_search.QUAKE().run(keyword, args.page, args.size, args.output, args.finger)
                    elif args.type == "hunter":
                        hunter_search.HUNTER().run(keyword, args.page, args.size, args.output, args.finger)
                    else:
                        print('搜索引擎类型输入有误！')
        else:
            if args.type == "fofa":
                fofa_search.Fofa().run(args.keyword, args.page, args.size, args.output, args.finger)
            elif args.type == "shodan":
                shodan_search.SHADAN().run(args.keyword, args.page, args.size, args.output, args.finger)
            elif args.type == "zoomeye":
                zoomeye_search.ZOOMEYE().run(args.keyword, args.page, args.output, args.finger)
            elif args.type == "quake":
                quake_search.QUAKE().run(args.keyword, args.page, args.size, args.output, args.finger)
            elif args.type == "hunter":
                hunter_search.HUNTER().run(args.keyword, args.page, args.size, args.output, args.finger)


if __name__ == '__main__':
    banner()
    parser = parse_args()
    args = parser.parse_args()
    if not (vars(args)['type'] or vars(args)['query']):
        parser.parse_args(["-h"])
    run(args)
