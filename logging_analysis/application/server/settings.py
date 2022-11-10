import os
allow_port = [8888, 50007]
STORAGE_PATH = "/hcs"
HOME = os.environ['HOME']
CONFIG = os.path.join(HOME, "config")
HANDLE = os.path.join(HOME, "handle")
CASE_ROOT = os.path.join(STORAGE_PATH, "case")
RESULT_ROOT = os.path.join(STORAGE_PATH, "result")
hwwuex_check = "/root/hwwuex_check"
APPLOG_DB = os.path.join(hwwuex_check, "config", "logging.db")

ROSETTA_URL = "https://rosetta.com/api/environments/121"
ROSETTA_TOKEN = "123"

MYSQL_HOST = "192.168.115.52"
MYSQL_USER = "root"
MYSQL_PASSWORD = "admin123"
MYSQL_DB = "hc_db"

CHECK_RESULT_EXPIRED_DAYS = 30
CHECK_RESULT_MINIMUM_QUANTITY = 3
CASE_EXPIRED_DAYS = 30

untar_limit_time = 60*5
