#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import print_function
import json
import logging
import re
import shutil
import threading
from datetime import datetime
import pymysql
import requests
from ruamel import yaml
from application.server.settings import *
from hwwuex_check.utils.utils import mkdir


class SingletonType(type):
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with SingletonType._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instance


class Configuration(metaclass=SingletonType):
    reader = None

    def __init__(self,):
        self.storage_path = STORAGE_PATH
        self.filename = "config.yaml"
        self.path = CONFIG
        mkdir(self.path)
        self.file = os.path.join(self.path, self.filename)
        if not os.path.exists(self.file):
            mkdir(HANDLE)
            mkdir(CASE_ROOT)
            mkdir(RESULT_ROOT)

            config = {
                "storage_path": self.storage_path,
                "config_root": self.path,
                "handle_root": HANDLE,
                "case_root": CASE_ROOT,
                "result_root": RESULT_ROOT,
                "who": []
            }
            self.write(config)
        self.reader = self.read(self.file)

    @staticmethod
    def read(filename):
        data = open(filename).read()
        reader = yaml.load(data, Loader=yaml.Loader)
        return reader

    def write(self, context):
        with open(self.file, "w", encoding="utf-8") as f:
            yaml.dump(context, f, Dumper=yaml.RoundTripDumper)

    def get_value(self, name, default=None, key=lambda x: x):
        """
        Get properties value.

        Parameters
        ----------
        name: string
            the key name in properties.
        default:
            default return
        key: func -> value
            usually used to convert data types.
        """
        value = key(self.reader.get(name, None))
        return value if value else default

    def add_or_update(self, **kwargs):
        self.reader.update(kwargs)
        self.write(self.reader)

    def remove(self, **kwargs):
        for key in kwargs:
            del self.reader[key]
        self.write(self.reader)

    @property
    def config_root(self):
        return self.reader["config_root"]

    @property
    def handle_root(self):
        return self.reader["handle_root"]

    @property
    def case_root(self):
        return self.reader["case_root"]

    @property
    def result_root(self):
        return self.reader["result_root"]

    @property
    def who(self):
        return self.reader["who"]

    def set_client(self, client):
        who = self.reader["who"]
        who.append(client)
        config = self.reader
        config.update({"who": who})
        self.write(config)

    def remove_client(self, client):
        who = self.reader["who"]
        del who[who.index(client)]
        config = self.reader
        config.update({"who": who})
        self.write(config)


class ServerLogger(metaclass=SingletonType):

    def __init__(self, **kwargs):
        self.path = os.path.join(HOME, "log")
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        self.level = (kwargs["level"] if kwargs.get("level") else "debug")
        self.fmt = (kwargs["format"] if kwargs.get("format") else
                       "%(asctime)s %(levelname)s [%(filename)s %(funcName)s %(lineno)d %(thread)d]: %(message)s")
        self.file = (kwargs["file"] if kwargs.get("file") else None)
        self.console = (kwargs["console"] if kwargs.get("console") else False)

        self.level_relations = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL,
        }
        self.logger = logging.getLogger(__name__)
        self.format = logging.Formatter(self.fmt)
        if not self.level_relations.get(self.level):
            self.level = "debug"
        self.logger.setLevel(self.level_relations[self.level])
        if self.console:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(self.format)
            self.logger.addHandler(stream_handler)
        if self.file:
            file_handler = logging.FileHandler(os.path.join(self.path, self.file), mode='w+')
            file_handler.setFormatter(self.format)
            self.logger.addHandler(file_handler)


class RosettaJson(object):
    url = None
    headers = None
    data = None
    response = None

    def __init__(self, url, token):
        self.url = url
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": 'Token {}'.format(token)
        }
        self.headers = headers
        self.response = requests.get(url=url, headers=headers, timeout=5)
        self.data = json.loads(self.response.content)

    @property
    def text(self):
        return self.response.text

    @property
    def nodes_list(self):
        return self.data["nodes"]

    def nodes_name(self):
        for node in self.nodes_list:
            print(node["infratype"]["node_name"])

    @staticmethod
    def node_networks(node):
        return node["networks"]

    @staticmethod
    def node_vips(networks):
        return networks["vips"]

    def search_key(self, string):
        pattern = re.compile("\"{}\":\"(.*?)\"".format(string))
        res = pattern.search(self.text)
        if res:
            return res.group(1)
        return res

    def search_node_name(self, string):
        pattern = re.compile("\"{}\":\"(.*?)\"".format(string))
        res = pattern.search(self.text)
        if res:
            for name in res.groups():
                if "gtla" in name:
                    return "gtla"
                elif "cudb" in name:
                    return "cudb"
                return None
        return res


class Properties(object):
    """
    A properties class.

    Provides or saves client information.
    Each client connection corresponds to a properties file which will be saved in handle root path.
    The file is named with the thread number, so different connections have independent parameter space.
    """
    filename = None
    yaml_reader = None

    def __init__(self, user=None, port=None, filename="properties.yaml"):
        self.thread_id = str(threading.current_thread().ident)
        if not user or not port:
            # search the properties file
            self.path = None
            for root, dirs, files in os.walk(Configuration().handle_root):
                for d in dirs:
                    if self.thread_id in d:
                        self.path = os.path.join(root, d)
        else:
            self.path = os.path.join(Configuration().handle_root, "%s-%s-%s" % (user, port, self.thread_id))

        self.file = os.path.join(self.path, filename)

        # if properties file does not exist, create new one
        if not os.path.exists(self.file):
            os.makedirs(self.path)
            # properties initial
            properties = {
                "user": user,
                "port": port,
                "workspace": self.path,
                "result_root": Configuration().result_root,
                "rosetta_url": ROSETTA_URL,
                "rosetta_token": ROSETTA_TOKEN
            }
            # try to get data from rosetta and save into properties
            try:
                rosetta = RosettaJson(properties["rosetta_url"], properties["rosetta_token"])
                rosetta_data = {
                    "oam_vip": rosetta.search_key("oam_vip"),
                    "sc1": rosetta.search_key("sc1"),
                    "sc2": rosetta.search_key("sc2"),
                    "node_name": rosetta.search_key("node_name"),
                }
                properties.update(rosetta_data)
            except Exception as e:
                logger = ServerLogger(file="server.log").logger
                logger.error(e)

            self.write(properties, self.file)

        self.yaml_reader = self.read(self.file)

    def __str__(self):
        return "properties_%s" % self.thread_id

    @staticmethod
    def write(data, filename):
        with open(filename, "w", encoding="utf-8") as f:
            yaml.dump(data, f, Dumper=yaml.RoundTripDumper)

    @staticmethod
    def read(filename):
        data = open(filename).read()
        yaml_reader = yaml.load(data, Loader=yaml.Loader)
        return yaml_reader

    def get_value(self, name, default=None, key=lambda x: x):
        """
        Get properties value.

        Parameters
        ----------
        name: string
            the key name in properties.
        default:
            default return
        key: func -> value
            usually used to convert data types.
        """
        value = key(self.yaml_reader.get(name, None))
        return value if value else default

    def add_or_update(self, **kwargs):
        self.yaml_reader.update(kwargs)
        self.write(self.yaml_reader, self.file)
        if "rosetta_url" in kwargs.keys() or "rosetta_token" in kwargs.keys():
            self.refresh_rosetta()

    def delete(self, keys):
        for key in keys:
            del self.yaml_reader[key]
        self.write(self.yaml_reader, self.file)

    @property
    def workspace(self):
        return self.path

    @property
    def reader(self):
        return self.yaml_reader

    @property
    def user(self):
        return self.yaml_reader.get("user")

    @property
    def port(self):
        return self.yaml_reader.get("port")

    @property
    def result_root(self):
        return self.yaml_reader.get("result_root")

    @property
    def result_path(self):
        return self.yaml_reader.get("result_path")

    @property
    def name(self):
        return self.yaml_reader.get("name")

    def refresh_rosetta(self):
        reader = self.read(self.file)
        rosetta = RosettaJson(reader["rosetta_url"], reader["rosetta_token"])
        rosetta_data = {
            "oam_vip": rosetta.search_key("oam_vip"),
            "sc1": rosetta.search_key("sc1"),
            "sc2": rosetta.search_key("sc2"),
            "node_name": rosetta.search_key("node_name"),
        }
        reader.update(rosetta_data)
        self.write(reader, self.file)

    def set_user(self, name):
        self.add_or_update(user=name)

    def save(self, filename=None):
        target_path = Configuration().path
        if not filename:
            filename = "properties-{}-{}.yaml".format(self.user, self.port)
        file = os.path.join(target_path, filename)
        shutil.copy(self.file, file)

    def copy(self, copy_file):
        target_path = Configuration().path
        target_file = os.path.join(target_path, copy_file)
        reader = self.read(target_file)
        consistent_data = {
            "user": self.user,
            "port": self.port,
            "result_root": self.result_root,
            "workspace": self.workspace
        }
        reader.update(consistent_data)
        self.write(reader, self.file)

    @property
    def display_path(self):
        return os.path.join(self.result_path, ".display")

    @staticmethod
    def create_display_path(display_path):
        if not os.path.exists(display_path):
            os.makedirs(display_path)
        return display_path

    def create_result_path(self, now=None):
        if not now:
            now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        result_path = os.path.join(self.result_root, self.user, timestamp)
        self.add_or_update(result_path=result_path)
        if not os.path.exists(self.result_path):
            os.makedirs(self.result_path)
        self.create_display_path(self.display_path)
        return self.result_path

    def save_data_into_display(self, update_self=False, **kwargs):
        """
        Save properties into display path.

        Display path:
            This directory is used to save all parameters and
            data that need to be displayed on the web page.

        Parameters
        ----------
        update_self: True, False, default: False
            True: Update the properties file form handle workspace.
            False: Only save kwargs into result/.display not handle workspace.
                    It means that the new kwargs cannot get value by cls.
        kwargs:
            The parameters tuple that need to be saved or updated.
        """
        file = os.path.join(self.display_path, "properties.yaml")
        if update_self:
            self.add_or_update(**kwargs)
        if os.path.exists(file):
            reader = self.read(file)
        else:
            reader = self.yaml_reader
        if kwargs:
            reader.update(**kwargs)
        self.write(reader, file)


class MysqlDb(object):

    def __init__(self):
        self.connect = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB,
                                       connect_timeout=3600)
        self.cursor = self.connect.cursor()

    def execute_cmd(self, cmd):
        try:
            self.cursor.execute(cmd)
            self.connect.commit()
        except Exception as e:
            print(e)
            self.connect.rollback()

    def fetchall(self, cmd):
        self.cursor.execute(cmd)
        data = self.cursor.fetchall()
        return data

    def close(self):
        self.cursor.close()
        self.connect.close()
