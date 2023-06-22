from config import grammar
from lib import cmdline
from lib.search import Search

if __name__ == '__main__':
    cmdline.banner()
    parser = cmdline.parse_args()
    args = parser.parse_args()
    if not any(vars(args).values()):
        parser.parse_args(["-h"])
    if args.type and not args.keyword and not args.file:
        grammar.grammar(args.type)
    else:
        if args.file:
            with open(f"{args.file}", 'r', encoding='utf-8') as f:
                for k in f.readlines():
                    keyword = k.strip()
                    search = Search(args, keyword)
        else:
            search = Search(args)
