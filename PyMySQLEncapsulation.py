# encoding:utf-8
import pymysql


class PyMySQLEncapsulation:

    def __init__(self, host, user, password, db_name):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.connection = self.get_connection()               # 数据库连接
        self.cursor = self.get_cursor()                       # 操作游标，操作数据库前需要获取操作游标

    def get_connection(self):
        self.connection = pymysql.connect(self.host, self.user, self.password, self.db_name)
        return self.connection

    def get_cursor(self):
        # 获取操作游标
        self.cursor = self.connection.cursor()
        return self.cursor

    def execute(self, sql: str):
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception:
            # 发生错误时回滚
            self.connection.rollback()
            raise Exception(sql)

    def close(self):
        self.connection.close()
