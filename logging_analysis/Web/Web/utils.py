#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import os
import tarfile
from zipfile import ZipFile

from ruamel import yaml
from Web.settings import RESULT_DIR
import threading
import re
import pymysql

from Web.settings import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB


def search_dirs(path, pattern):
    result = []
    for p in os.listdir(path):
        if os.path.isdir(os.path.join(path, p)):
            ret = re.match(pattern, p)
            if ret:
                result.append(os.path.join(path, p))
    return result


# Search files in path. Do not drill down to subdirectories
def search_files(path, pattern):
    result = []
    for f in os.listdir(path):
        ret = re.match(pattern, f)
        if ret:
            result.append(os.path.join(path, f))
    return result


# Search files in path. Include subdirectories
def search_files_deeply(path, pattern):
    result = []
    for root, dirs, files in os.walk(path):
        for file in files:
            ret = re.match(pattern, file)
            if ret:
                result.append(os.path.join(root, file))
    return result


def un_zip(source_zip, target_dir):
    myzip = ZipFile(source_zip)
    myfilelist = myzip.namelist()
    for name in myfilelist:
        f_handle = open(os.path.join(target_dir, name), "wb")
        f_handle.write(myzip.read(name))
        f_handle.close()
    myzip.close()
    return target_dir


def un_tar(file_name, target_dir):
    tar = tarfile.open(file_name)
    names = tar.getnames()

    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)

    for name in names:
        tar.extract(name, target_dir)
    tar.close()
    return target_dir


def get_loads(path):
    def get_files(data_path):
        files = []
        dirs = search_dirs(data_path, "^BAT_.*.")
        for d in dirs:
            filename = "_".join(os.path.basename(d).split("_")[0:2])
            data_file = search_files(d, "%s.data" % filename)
            if data_file:
                files.extend(data_file)
        return files

    def get_dataset(filename):
        loads = []
        with open(filename, 'r') as fr:
            context = fr.readlines()
            for line in context:
                string = line.strip().split(",")
                timestamp = datetime.datetime.strptime(string[0], "%Y-%m-%d %H:%M:%S").timestamp()
                load = [int(timestamp * 1000), float(string[1])]
                loads.append(load)
        return loads

    data_path = os.path.join(path, "EXECUTION")
    data_file = get_files(data_path)
    loads_data = {}
    for filename in data_file:
        key = os.path.basename(filename)
        loads = get_dataset(filename)
        loads_data[key] = loads
    return loads_data


def get_load_time(path):
    output_context = []
    logs = search_files(os.path.join(path, "EXECUTION"), "^error.*")
    if not logs:
        output_context.append("Not search the log.")

    error_monitor_log = logs[0]
    fq = open(error_monitor_log, "r")
    file_content = fq.read()
    fq.close()

    matchObj = re.findall(r'Started: (.*) Stopped: (.*) Phase: loadgen', file_content, re.M | re.I)
    if matchObj:
        start = (matchObj[0][0]).rstrip()
        end = (matchObj[-1][1]).rstrip()
        output_context.append("Load phase start from: " + start)
        output_context.append("Load phase end   from: " + end + "\r\n")
        return start, end, output_context
    else:
        output_context.append("Couldn't find load phase timing from the log")
        return None, None, output_context


def get_error_rate(path):
    def get_files(data_path):
        files = []
        dirs = search_dirs(data_path, "^BAT_.*.")
        for d in dirs:
            filename = os.path.basename(d)
            data_file = search_files(d, "%s_total_error_rate.data" % filename)
            if data_file:
                files.extend(data_file)
        return files

    def get_dataset(filename):
        loads = []
        with open(filename, 'r') as fr:
            context = fr.readlines()
            for line in context:
                string = line.strip().split(",")
                timestamp = datetime.datetime.strptime(string[0], "%Y-%m-%d %H:%M:%S").timestamp()
                load = [int(timestamp * 1000), float(string[1])]
                loads.append(load)
        return loads

    data_path = os.path.join(path, "EXECUTION")
    data_file = get_files(data_path)
    loads_data = {}
    for filename in data_file:
        key = os.path.basename(filename)
        loads = get_dataset(filename)
        loads_data[key] = loads
    return loads_data


def read_yaml(filename):
    try:
        data = open(filename).read()
        yaml_reader = yaml.load(data, Loader=yaml.Loader)
    except:
        yaml_reader = {}
    return yaml_reader


def read_log(filename):
    try:
        with open(filename, 'r') as fr:
            context = fr.readlines()
    except Exception as e:
        context = []
    return context


class SingletonType(type):
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with SingletonType._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instance


class MysqlDb(object):

    def __init__(self):
        self.connect = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB,
                                       connect_timeout=3600)

    def execute_cmd(self, cmd):
        cursor = self.connect.cursor()
        try:
            cursor.execute(cmd)
            self.connect.commit()
        except Exception as e:
            print(e)
            self.connect.rollback()

    def fetchall(self, cmd):
        cursor = self.connect.cursor()
        cursor.execute(cmd)
        data = cursor.fetchall()
        return data

    def close(self):
        cursor = self.connect.cursor()
        cursor.close()
        self.connect.close()


def get_records(days=365):
    def complete_default(x_axis, y_data, default=0):
        for x in x_axis:
            for check_type in y_data.keys():
                search = False
                points = y_data.get(check_type)
                if x in y_data[check_type].keys():
                    search = True
                if not search:
                    points.update({x: default})

    mysql = MysqlDb()
    sql = "select case_type, start from check_record where datediff(now(), start)<={}".format(days)
    result = mysql.fetchall(sql)
    x_data = []
    y_data = {}
    if int(days) <= 365:
        month_index = datetime.datetime.now().month
        month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        x_data = month_list[month_index:] + month_list[:month_index]

        for d in result:
            check_type = d[0]
            timestamp = d[1]
            month = timestamp.date().month-1
            x_axis = month_list[month]
            if check_type not in y_data.keys():
                y_data[check_type] = {}
            if x_axis not in x_data:
                y_data[check_type].update({x_axis: 0})

            search = False
            if x_axis in y_data[check_type].keys():
                y_data[check_type][x_axis] += 1
                search = True

            if not search:
                y_data[check_type].update({x_axis: 1})

        # complete default=0
        complete_default(month_list, y_data, default=0)

        # sort x data
        for check_type in y_data.keys():
            y_data[check_type] = dict(sorted(y_data[check_type].items(), key=lambda data: x_data.index(data[0])))
    else:
        sql = "select date_format(start, '%Y-%m') as DateTime from check_record where datediff(now(), start)<={} group by date_format(start, '%Y-%m')".format(days)
        x_data = [d[0] for d in mysql.fetchall(sql)]

        sql = "select distinct case_type from check_record where datediff(now(), start)<={}".format(days)
        case_type = [d[0] for d in mysql.fetchall(sql)]

        for t in case_type:
            y_data[t] = {}
            sql = "select date_format(start, '%Y-%m') as DateTime, count(1) as countNumber from check_record where datediff(now(), start)<={} and case_type='{}' group by date_format(start, '%Y-%m')".format(days, t)
            result = mysql.fetchall(sql)
            for d in result:
                y_data[t].update({d[0]: d[1]})

        # complete default=0
        complete_default(x_data, y_data, default=0)

        # sort x data
        x_data = sorted(x_data, key=lambda data: datetime.datetime.strptime(data, '%Y-%m').timestamp())
        for check_type in y_data.keys():
            y_data[check_type] = dict(sorted(y_data[check_type].items(), key=lambda data: datetime.datetime.strptime(data[0], '%Y-%m').timestamp()))

    return x_data, y_data


def get_total_records(days=365):
    mysql = MysqlDb()
    sql = "select count(user_id) from check_record where datediff(now(), start)<={}".format(days)
    result = mysql.fetchall(sql)
    return result[0][0]


def get_records_by_user(days=365):
    mysql = MysqlDb()
    sql = "select distinct user_id from check_record where datediff(now(), start)<={}".format(days)
    result = mysql.fetchall(sql)
    users = [d[0] for d in result]
    data = {}
    for user in users:
        sql = """select count(user_id) from check_record where datediff(now(), start)<={} and user_id="{}";""".format(days, user)
        result = mysql.fetchall(sql)
        count = result[0][0]
        data[user] = count
    return data


def get_records_by_type(days=365):
    mysql = MysqlDb()
    sql = "select distinct case_type from check_record where datediff(now(), start)<={}".format(days)
    result = mysql.fetchall(sql)
    types = [d[0] for d in result]
    data = {}
    for t in types:
        sql = """select count(case_type) from check_record where datediff(now(), start)<={} and case_type="{}";""".format(days, t)
        result = mysql.fetchall(sql)
        count = result[0][0]
        data[t] = count
    return data


def get_results():
    owners = os.listdir(RESULT_DIR)
    results = []
    for name in owners:
        p = os.path.join(RESULT_DIR, name)
        dirs = os.listdir(p)

        for d in dirs:
            info_file = os.path.join(p, d, ".display", "properties.yaml")
            try:
                yaml_reader = yaml.load(open(info_file).read(), Loader=yaml.Loader)
            except:
                continue
            yaml_reader["timestamp"] = d
            yaml_reader["time"] = datetime.datetime.strptime(d, "%Y%m%d%H%M%S")
            results.append(yaml_reader)

    # TODO: get result path
    return results
