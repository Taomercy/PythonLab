#!/usr/bin/env python
from MysqlObj import *


def show_table(db, tb_name=None):
    if tb_name:
        sql_cmd = "show tables like '{0}'".format(tb_name)
    else:
        sql_cmd = "show tables"
    res = db.fetch_all(sql_cmd)
    return res


def truncate_table(db, tb_name):
    sql_cmd = "truncate table {0}".format(tb_name)
    db.update(sql_cmd)


def drop_table(db, tb_name):
    sql_cmd = "drop table {0}".format(tb_name)
    db.update(sql_cmd)


def create_error_type_tb(db, tb_name):
    sql_cmd = "create table {0} (".format(tb_name)
    sql_cmd += "id int auto_increment Primary key, "
    sql_cmd += "ErrorString text)"
    db.update(sql_cmd)


def collect_error_type(db, tb_name, error):
    table = show_table(db, tb_name)
    if not table:
        create_error_type_tb(db, tb_name)

    datas = data_select(db, tb_name, 'ErrorString', error)
    if not datas:
        k = ['ErrorString']
        v = [error]
        data_insert(db, tb_name, k, v)


def create_job_name_tb(db, tb_name):
    sql_cmd = "create table {0} (".format(tb_name)
    sql_cmd += "id int auto_increment Primary key, "
    sql_cmd += "RecentBuild int not null default 0, "
    sql_cmd += "JobName text)"
    db.update(sql_cmd)


def collect_job_name(db, tb_name, JobName):
    table = show_table(db, tb_name)
    if not table:
        create_job_name_tb(db, tb_name)

    datas = data_select(db, tb_name, 'JobName', JobName)
    if not datas:
        k = ['JobName']
        v = [JobName]
        data_insert(db, tb_name, k, v)


def create_action_type(db, tb_name):
    sql_cmd = "create table {0} (".format(tb_name)
    sql_cmd += "id int auto_increment Primary key, "
    sql_cmd += "ActionString text)"
    db.update(sql_cmd)


def prepare_action_type(db, tb_name, actionList):
    # actionList = ["retrgger", "waittimes", "other"]
    table = show_table(db, tb_name)
    if not table:
        create_action_type(db, tb_name)
    for action in actionList:
        res = data_select(db, tb_name, 'ActionString', action)
        if not res:
            k = ['ActionString']
            v = [action]
            data_insert(db, tb_name, k, v)


def create_action_trigger_res_tb(db, tb_name):
    sql_cmd = "create table {0} (".format(tb_name)
    sql_cmd += "ErrorType int, "
    sql_cmd += "BuildStat int, "
    sql_cmd += "BuildTime int,"
    sql_cmd += "actionID int)"
    db.update(sql_cmd)


def collect_action_trigger_res(db, tb_name, error_type, build_stat, build_time, action_id):
    table = show_table(db, tb_name)
    if not table:
        create_action_trigger_res_tb(db, tb_name)

    k = ['ErrorType', 'BuildStat', 'BuildTime', 'actionID']
    if not build_stat:
        build_time = 99999999
    v = [error_type, build_stat, build_time, action_id]
    data_insert(db, tb_name, k, v)
    print "collect record:", v


def create_error_feature_tb(db, tb_name):
    sql_cmd = "create table {0} (".format(tb_name)
    sql_cmd += "JobId int, "
    sql_cmd += "RecentBuildSuccessRate float, "
    sql_cmd += "BuildTime int, "
    sql_cmd += "ErrorType int)"
    db.update(sql_cmd)


def collect_error_feature(db, tb_name, job_id, recent_success_rate, build_time, error_type):
    table = show_table(db, tb_name)
    if not table:
        create_error_feature_tb(db, tb_name)
    k = ['JobId', 'RecentBuildSuccessRate', 'BuildTime', 'ErrorType']
    v = [job_id, recent_success_rate, build_time, error_type]
    data_insert(db, tb_name, k, v)
