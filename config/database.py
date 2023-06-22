from config import sqldb
from module.Finger.config.data import logging


class CHECK_DB:
    def __init__(self):
        self.db = sqldb.DB()
        self.check_db()

    def check_db(self):
        dbs = self.db.query("show databases")  # 检查数据库是否存在
        if ('IntegSearch',) not in dbs:
            self.db.query("create database IntegSearch;")
            logging.info("新建数据库成功!")
            self.db.query("SET @@global.sql_mode= '';")

        self.db.query("use IntegSearch;")

        tables = self.db.query("show tables")  # 检查表是否存在

        if ('fofa',) not in tables:
            self.createdb("fofa")

        if ('shodan',) not in tables:
            self.createdb("shodan")

        if ('hunter',) not in tables:
            self.createdb("hunter")

        if ('zoomeye',) not in tables:
            self.createdb("zoomeye")

        if ('quake',) not in tables:
            self.createdb("quake")

        if ('zone',) not in tables:
            self.createdb("zone")

    def createdb(self, search_type):
        sql = f"""
            CREATE TABLE `{search_type}` (
        `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT 'ID',
        `host` varchar(255) NULL DEFAULT NULL COMMENT 'HOST',
        `ip` varchar(100) NULL DEFAULT NULL COMMENT 'IP',
        `port` varchar(50) NULL DEFAULT NULL COMMENT '端口',
        `protocol` varchar(50) NULL DEFAULT NULL COMMENT '协议',
        `country` varchar(150) NULL DEFAULT NULL COMMENT '国家',
        `domain` varchar(255) NULL DEFAULT NULL COMMENT '域名',
        `title` varchar(255) NULL DEFAULT NULL COMMENT '标题',
        `updateTime` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '更新时间',
        primary key(id)
        )CHARSET=utf8;
        """
        self.db.query(sql)
        logging.info(f"新建{search_type}数据表成功!")
