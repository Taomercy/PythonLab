from settings import APPLOG_DB, untar_limit_time

from application.server.object import Properties, ServerLogger, MysqlDb
from hwwuex_check.utils.utils import *

global LOAD_START
global LOAD_END
global output_fw
global return_code


@calculator_execute_time
def check(path, output, **kwargs):
    logger = ServerLogger().logger
    properties = Properties()
    LOAD_START = kwargs.get("start")
    LOAD_END = kwargs.get("end")
    global return_code
    return_code = "SUCCESS"
    output_log = os.path.join(output, "applog.log")

    logger = kwargs["summary_log"]
    logger.info("Check Applog		: " + return_code)

    return return_code, output_log
