#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
import os
import re
from datetime import datetime

from application.server.object import Properties, ServerLogger, MysqlDb, Configuration, allow_port
from hwwuex_check.utils.utils import search_files, init_log


class TestCase(object):
    case_full_path = None
    test_case_name = None
    check_type = None
    check_start = None
    result_path = None
    modes = []

    def __init__(self, case_full_path, check_type, modes=None):
        self.case_full_path = case_full_path
        self.test_case_name = os.path.basename(self.case_full_path)
        self.check_type = check_type

        start_time = datetime.now()
        self.check_start = start_time.strftime("%Y-%m-%d %H:%M:%S")
        # prepare result path
        self.result_path = Properties().create_result_path(now=start_time)

        # save properties in result
        info = {"case_name": self.test_case_name, "type": self.check_type}
        Properties().save_data_into_display(**info)

        # modes confirm
        check_standard = {"free_memory_rate": 1.0, "process_difference_tolerance": 0}
        if not modes or "all" in modes:
            modes = ["applog", "ca", "extdb", "fmalarm", "health", "memory", "process", "traffic", "http_connection",
                     "traffic_error"]

        filter_fields = ["TC-CROB-0606", "TC-CROB-0607", "TC-CROB-0608", "TC-CROB-0609", "TC-CROB-0610", "TC-CACC-0214"]
        for field in filter_fields:
            if field in self.test_case_name and "traffic_error" in modes:
                modes.remove("traffic_error")
                break

        # check standard setting
        if self.check_type == "stability":
            pass
        if self.check_type == "accuracy":
            check_standard.update(process_difference_tolerance=10)
        if self.check_type == "robustness":
            check_standard.update(process_difference_tolerance=10)
        if self.check_type == "upgrade":
            modes.append("upgrade")
            check_standard.update(process_difference_tolerance=10)
        self.modes = modes

        # save check standard into result
        Properties().save_data_into_display(update_self=True, **check_standard)

    def get_load_time(self, logger, path):
        logs = search_files(os.path.join(path, "EXECUTION"), "^error.*")
        if not logs:
            logger.info("Not search the log.")
            return None

        error_monitor_log = logs[0]
        fq = open(error_monitor_log, "r")
        file_content = fq.read()
        fq.close()

        matcher = re.findall(r'Started: (.*) Stopped: (.*) Phase: loadgen', file_content, re.M | re.I)
        if matcher:
            start = (matcher[0][0]).rstrip()
            end = (matcher[-1][1]).rstrip()
            return start, end
        else:
            logger.info("Couldn't find load phase timing from the log")
            return None

    def check(self, start=None, end=None):
        logger = ServerLogger(file="server.log").logger
        logger.info("check start")
        logger.info("case full path:% s" % self.case_full_path)
        logger.info("modes: %s" % str(self.modes))

        response = []
        summary = os.path.join(self.result_path, "summary.log")
        summary_log = init_log(summary)

        if not start or not end:
            start, end = self.get_load_time(summary_log, self.case_full_path)
            time_record = {"start": start, "end": end}
            Properties().save_data_into_display(**time_record)
        parameter = {"start": start, "end": end, "summary_log": summary_log}

        summary_log.info("Test Case Name		: " + self.test_case_name)
        summary_log.info("Time Start		: " + start)
        summary_log.info("Time Stop		: " + end)
        summary_log.info("Check Results		: " + self.result_path)
        summary_log.info("-------------")

        start_time = datetime.now()
        for mode in self.modes:
            module_name = "hwwuex_check.models." + mode
            func_name = "check"
            module = __import__(module_name, fromlist=True)
            if hasattr(module, func_name):
                check_func = getattr(module, func_name)
                try:
                    return_code, output_log = check_func(self.case_full_path, self.result_path, **parameter)
                    response.append("[{}]  {}".format(return_code, output_log))
                    record = {mode: return_code}
                    Properties().save_data_into_display(**record)
                except Exception as e:
                    response.append(e)
        spend = (datetime.now() - start_time).seconds
        logger.info("Spend: %s(s)" % str(spend))
        logger.info("Check done")
        summary_log.info("\n")

        # save data into mysql
        server_port = Configuration().get_value(name="port", key=int, default=0)
        if server_port in allow_port:
            mode_string = ",".join(self.modes)
            sql_cmd = """insert into check_record (user_id,case_name,case_type,mode,start,spend) values ("{}","{}","{}","{}","{}",{})""".format(
                Properties().user, self.test_case_name, self.check_type, mode_string, self.check_start, spend)
            logger.debug("sql: %s" % sql_cmd)
            MysqlDb().execute_cmd(sql_cmd)
        else:
            logger.info("It's a test port ({}) not record.".format(server_port))

        logging.shutdown()
        return response
