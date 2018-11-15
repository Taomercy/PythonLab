#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb


class DataBase:
    username = None
    __password = None
    dbName = None
    dbHost = None
    _db = None
    _cursor = None

    def __init__(self, username, password, db_name, db_host="localhost"):
        self.username = username
        self.__password = password
        self.dbName = db_name
        self.dbHost = db_host
        self._db = MySQLdb.connect(db_host, username, password, db_name, charset='utf8')
        self._cursor = self._db.cursor()

    def fetch_all(self, sql_cmd):
        res = ''
        if(self._db):
            try:
                self._cursor.execute(sql_cmd)
                res = self._cursor.fetchall()
            except Exception, data:
                res = False
                print "query database exception, %s" % data
        return res

    def update(self, sql_cmd):
        flag = False
        if(self._db):
            try:
                self._cursor.execute(sql_cmd)
                self._db.commit()
                flag = True
            except Exception, data:
                self._db.rollback()
                flag = False
                print "update database exception, %s" % data

        return flag

    def close(self):
        if(self._db):
            try:
                if(type(self._cursor)=='object'):
                    self._cursor.close()
                if(type(self._db)=='object'):
                    self._db.close()
            except Exception, data:
                print "close database exception, %s,%s,%s" % (data, type(self._cursor), type(self._db))


def data_select(db, tb_name, columnName=None, inputValue=None, whatSelect='*'):
    '''
        sql_cmd = select {whatSelect} from [ where {columnName}={inputValue} ]
    '''
    if whatSelect == '*':
        sql_cmd = '''select * from {0} '''.format(tb_name)
    else:
        sql_cmd = '''select {0} from {1} '''.format(whatSelect, tb_name)
    if columnName and inputValue is not None:
        sql_cmd += '''where {0}='{1}' '''.format(columnName, inputValue)
    res = db.fetch_all(sql_cmd)
    return res


def data_insert(db, tb_name, keyList, valueList):
    '''
        sql_cmd = insert into {tb_name} (k1, k2, k3, ...) values(v1, v2, v3, ...)
    '''
    sql_cmd = '''insert into {0} ('''.format(tb_name)
    for key in keyList:
        sql_cmd += "{0},".format(key)
    sql_cmd = sql_cmd[:-1]
    
    sql_cmd += ') values('
    for value in valueList:
        if isinstance(value, basestring):
            sql_cmd += "'{0}',".format(value)
        else:
            sql_cmd += "{0},".format(value)
    sql_cmd = sql_cmd[:-1]  
    sql_cmd += ')'
    db.update(sql_cmd)
