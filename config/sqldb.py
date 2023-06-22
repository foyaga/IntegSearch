import pymysql

from config.configfile import config


class DB:
    def __init__(self):
        self.conn = pymysql.connect(
            host=config['database']['host'],
            port=config['database']['port'],
            user=config['database']['user'],
            passwd=config['database']['password'],
            charset='utf8', )
        self.cur = self.conn.cursor()

    def __del__(self):  # 析构函数，实例删除时触发
        try:
            self.cur.close()
            self.conn.close()
        except AttributeError:
            print("数据库连接失败")
            exit(0)

    # 封装数据库查询操作
    def query(self, sql):
        while True:
            try:
                self.conn.ping(reconnect=True)
                self.cur.execute(sql)
                return self.cur.fetchall()
            except Exception as error:
                print(error)
                exit(0)

    # 封装更改数据库操作
    def exec(self, sql):
        while True:
            try:
                self.conn.ping(reconnect=True)
                self.cur.execute(sql)  # 执行sql
                self.conn.commit()  # 提交更改
                break
            except Exception as error:
                self.conn.rollback()  # 回滚
                print(error)
                exit(0)
