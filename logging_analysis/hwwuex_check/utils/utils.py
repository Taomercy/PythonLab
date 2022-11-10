#!/usr/bin/env python
# -*- coding:utf-8 -*-
import functools

import stopit
from datetime import datetime
import logging
import os
import re
import shutil
import tarfile
import sqlite3
import subprocess
from ruamel import yaml
from zipfile import ZipFile


def init_log(log_file, ctime=False, console=False, level="info"):
    logger = logging.getLogger(log_file)
    if ctime:
        formatter = logging.Formatter('%(asctime)s : %(message)s', "%Y-%m-%d %H:%M:%S")
    else:
        formatter = logging.Formatter('%(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w+')
    fileHandler.setFormatter(formatter)
    if level == "debug":
        lev = logging.DEBUG
    elif level == "info":
        lev = logging.INFO
    else:
        lev = level
    logger.addHandler(fileHandler)
    logger.setLevel(lev)
    if console:
        console = logging.StreamHandler()
        logger.addHandler(console)
    return logger


def calculator_execute_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = kwargs.pop("logger", None)
        fw = kwargs.pop("fw", None)
        start_time = datetime.now()
        func_return = func(*args, **kwargs)
        spend = (datetime.now() - start_time).seconds
        info = "Function({}) Execute Time: {} (s)".format(func.__name__, str(spend))
        if logger:
            logger.debug(info)
        elif fw:
            fw.write(info+"\n")
        else:
            print(info)
        return func_return
    return wrapper


def write_yaml(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, Dumper=yaml.RoundTripDumper)


def read_yaml(filename):
    try:
        data = open(filename).read()
        yaml_reader = yaml.load(data, Loader=yaml.Loader)
    except:
        yaml_reader = {}
    return yaml_reader


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


@stopit.threading_timeoutable("timeout", timeout_param="timeout")
def un_tar(file_name, target_dir):
    tar = tarfile.open(file_name)
    names = tar.getnames()

    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)

    for name in names:
        try:
            tar.extract(name, target_dir)
        except Exception as e:
            print(e)
            continue
    tar.close()
    return target_dir


def remove_dir(path):
    shutil.rmtree(path)


def mkdir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def remove_empty_files(path):
    try:
        cwd = os.getcwd()
        os.chdir(path)
        for file_name in os.listdir(path):
            if len(file_name) > 0:
                if os.stat(file_name).st_size == 0:
                    os.remove(file_name)
        os.chdir(cwd)
        return True
    except:
        return False


def time_compare(start, end, current):
    s = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    e = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
    t = datetime.strptime(current, '%Y-%m-%d %H:%M:%S')
    if s < t < e:
        return True
    else:
        return False


# if current time in several days return True
def difference_time_comparison(object_time, days=7):
    object_time_p = datetime.strptime(object_time, "%Y-%m-%d %H:%M:%S")
    today_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today_time_p = datetime.strptime(today_time, "%Y-%m-%d %H:%M:%S")
    delta = (today_time_p-object_time_p).days
    if delta <= days:
        return True
    else:
        return False


def convert_datetime(datestr):
    try:
        ret = re.match(r'(\d+-\d+-\d+T\d+:\d+:\d+\.\d+).*', datestr, re.M | re.I)
        if ret:
            return datetime.strptime(ret.group(1), '%Y-%m-%dT%H:%M:%S.%f')
        ret = re.match(r'(\d+-\d+-\d+T\d+:\d+:\d+).*', datestr, re.M | re.I)
        if ret:
            return datetime.strptime(ret.group(1), '%Y-%m-%dT%H:%M:%S')
        ret = re.match(r'(\d+-\d+-\d+ \d+:\d+:\d+).*', datestr, re.M | re.I)
    except Exception as e:
        return None


def format_interval_stime(time1,time2,time_format):
    date1=datetime.strptime(time1,time_format)
    date2=datetime.strptime(time2,time_format)
    time=str(date2-date1).split(":")
    return "{} min {} secs".format(time[1],time[2])


def get_total_seconds(time):
    total_seconds=-1
    ret=re.findall(r'(\d+)\s*MIN\s*(\d+)\s*SEC',time,re.I)
    if ret:
        mins=ret[0][0]
        seconds=ret[0][1]
        total_seconds=int(mins)*60+int(seconds)
    return total_seconds


def get_time_deviation(time,standard_time):
    sec1=get_total_seconds(time)
    sec2=get_total_seconds(standard_time)
    deviation=float(sec1-sec2)*100/sec2
    return abs(deviation)


def execute_cmd(cmd):
    rep = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    rep.wait()
    if rep.returncode !=0:
        raise Exception (cmd)
    cmd_ret=rep.stdout.read().strip()
    return str(cmd_ret)


def connect_to_db():
    db_profiles = os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0], 
                                                "../","config","logging.db"))
    connection = sqlite3.connect(db_profiles)
    connection.row_factory = sqlite3.Row
    conn = connection.cursor()
    return conn,connection


def disconnect_from_db(connection):
    connection.close()


def query_from_table(sql):
    conn,connection = connect_to_db()
    conn.execute(sql)
    rows = conn.fetchall()
    col_name_list = [tuple[0] for tuple in conn.description]
    disconnect_from_db(connection)
    return rows,col_name_list


# CUD means "Create,update,delete"
def cud_to_db(sql):
    conn, connection = connect_to_db()
    conn.execute(sql)
    connection.commit()
    disconnect_from_db(connection)