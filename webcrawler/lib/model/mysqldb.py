#!/usr/bin/env python 2.7
# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
###############################################################################
"""
对MySQLdb常用函数进行封装的类
注意：使用这个类的前提是正确安装 MySQL-Python模块。
官方网站：http://mysql-python.sourceforge.net/

Authors: Gary(ligang05@baidu.com)
Date:    2015/07/07 17:23:06
"""


import time
import logging
import MySQLdb


import webcrawler.conf.mysqlconf as mysqlconf



class MySQL(object):
    """对MySQLdb常用函数进行封装的类"""

    _errcode = ''     # MySQL错误号码
    _conn = None        # 数据库conn
    _cur = None         # 游标
    _timecount = 0
    _try_count = 0

    def __init__(self, dbname, charset='utf8'):
        """构造器：根据数据库连接参数，创建MySQL连接"""
        error_msg = ''
        try:
            dbconfig = mysqlconf.DB_NAMES[dbname]
            self._conn = MySQLdb.connect(**dbconfig)
        except KeyError as e:
            error_msg = 'Error, cannot find the database, {0}!'.format(dbname)
            logging.error(error_msg)
            raise Exception(error_msg)
        except MySQLdb.Error as e:
            self.log_dberror(e, 'try again!')
            if self._try_count < mysqlconf.TRY_LINK_COUNT:
                time.sleep(mysqlconf.INTERVAL_TIME_SECOND)
                self._try_count += 1
                return self.__init__(dbname)
            else:
                raise Exception(error_msg)

        self._cur = self._conn.cursor()
        self._conn.set_character_set(charset)

    def log_dberror(self, err, msg=''):
        """记录错误日志"""
        log_msg = 'MySQL error,{err_code}: {err_msg}!{msg}'.format(err_code=err.args[0],\
            err_msg=err.args[1], msg=msg)
        logging.error(log_msg)

    def query(self, sql):
        """执行 SELECT 语句"""
        try:
            self._cur.execute("SET NAMES utf8")
            result = self._cur.execute(sql)
        except MySQLdb.Error as e:
            self._error_code = e.args[0]
            self.log_dberror(e)
            result = False
        return result

    def update(self, sql):
        """执行 UPDATE 及 DELETE 语句"""
        try:
            self._cur.execute("SET NAMES utf8")
            result = self._cur.execute(sql)
            self._conn.commit()
        except MySQLdb.Error as e:
            self._error_code = e.args[0]
            self.log_dberror(e)
            result = False
        return result

    def commit(self):
        """数据库commit操作"""
        self._conn.commit()

    def rollback(self):
        """数据库回滚操作"""
        self._conn.rollback()

    def show_tables(self):
        """显示所有表名"""
        self.query('show tables')
        results = self._cur.fetchall()
        return [tb[0] for tb in results]

    def selectdb(self, dbname):
        """选择数据库"""
        try:
            self._conn.select_db(dbname)
        except MySQLdb.Error as e:
            self.log_dberror(e)

    def query_onerow(self, sql):
        """查询单条记录"""
        self.query(sql)
        result = self._cur.fetchone()
        return result

    def query_allrows(self, sql):
        """查询多条记录"""
        self.query(sql)
        result = self._cur.fetchall()
        desc = self._cur.description
        data = []
        for inv in result:
            _data = {}
            for i in range(0, len(inv)):
                # _data[desc[i][0]] = str(inv[i])
                _data[desc[i][0]] = inv[i]
            data.append(_data)
        return data

    def insert(self, table_name, data):
        """
        table_name: 插入的表名
        data: 插入的数据
        需要使用commit函数正式生效
        """
        for key in data:
            if isinstance(data[key], str):
                data[key] = "'" + data[key] + "'"
            else:
                data[key] = str(data[key])
        key   = ','.join(data.keys())
        value = ','.join(data.values())
        real_sql = "INSERT INTO " + table_name + " (" + key + ") VALUES (" + value + ")"
        try:
            return self.query(real_sql)
        except MySQLdb.Error as e:
            self._error_code = e.args[0]
            self.log_dberror(e)
            return False

    def insert_update(self, table_name, data):
        """
        table_name: 插入的表名
        data: 插入的数据
        插入数据，如果已经存在主键则更新
        需要使用commit函数正式生效
        """
        keys = []
        for key in data:
            if isinstance(data[key], str):
                data[key] = "'" + data[key] + "'"
            else:
                data[key] = str(data[key])
            strkey = "`%s` = VALUES(`%s`)" % (key, key)
            keys.append(strkey)

        key   = ','.join(data.keys())
        value = ','.join(data.values())
        update = ','.join(keys)
        # real_sql = "INSERT INTO " + table_name + " (" + key + ") VALUES (" + value + ")"
        real_sql = "INSERT INTO %s ( %s ) VALUES ( %s ) ON DUPLICATE KEY UPDATE %s " % (table_name, key, value, update)
        # print real_sql

        try:
            return self.query(real_sql)
        except MySQLdb.Error as e:
            self._error_code = e.args[0]
            self.log_dberror(e)
            return False

    def getlast_insertid(self):
        """获取最后一条插入id"""
        return self._cur.lastrowid

    def rowcount(self):
        """查询的结果行数"""
        return self._cur.rowcount

    def  close(self):
        """关闭数据库连接"""
        self.__del__()

    def __del__(self): 
        """释放资源,系统GC自动调用"""
        try:
            self._cur.close() 
            self._conn.close() 
        except:
            pass

if __name__ == '__main__':
    '''使用样例'''
    #连接数据库，创建这个类的实例
    db = MySQL('local_test')

    #操作数据库
    sql = "SELECT * FROM `messages` where subject='h234'"
    db.query(sql)

    #获取结果列表
    # result = db.fetch_one_row()
    result = db.query_onerow(sql)
    print result
    print db.show_tables()

    data = {
        'subject': 'hahw44',
        'reply_to': 1234445,
        'text': 'new-text',
    }
    # db.insert('messages', data)
    db.insert_update('messages', data);
    db.commit()
