#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import logging
import shutil
import time
from apscheduler.schedulers.background import BackgroundScheduler
from application.server.settings import *
from application.server.object import ServerLogger


class SchedulerMain(object):
    scheduler = None

    def __init__(self, level="info"):
        logging.basicConfig()
        logger = logging.getLogger('apscheduler')
        if level == "info":
            logger.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.DEBUG)
        self.scheduler = BackgroundScheduler()

    def job_scheduler_add(self, job):
        pass

    def scheduler_shutdown(self, wait=True):
        self.scheduler.shutdown(wait=wait)

    def get_scheduler(self):
        return self.scheduler


def difference_time_comparison(object_time, days=7):
    object_time_p = datetime.datetime.strptime(object_time, "%Y%m%d%H%M%S")
    today_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    today_time_p = datetime.datetime.strptime(today_time, "%Y%m%d%H%M%S")
    delta = (today_time_p-object_time_p).days
    if delta <= days:
        return True
    else:
        return False


def clean_check_result():
    logger = ServerLogger(file="server.log").logger
    users = os.listdir(RESULT_ROOT)
    for user in users:
        result_path = os.path.join(RESULT_ROOT, user)
        results = os.listdir(result_path)
        if len(results) <= CHECK_RESULT_MINIMUM_QUANTITY:
            logger.info("Results(%s) less than minimum quantity(%s)." % (user, str(CHECK_RESULT_MINIMUM_QUANTITY)))
            continue
        for result in results:
            try:
                timestamp = result
                if not difference_time_comparison(timestamp, days=CHECK_RESULT_EXPIRED_DAYS):
                    logger.info("remove expired result: %s" % result)
                    shutil.rmtree(os.path.join(result_path, result))
            except:
                continue


class CleanCheckResultScheduler(SchedulerMain):
    scheduler = None

    def __init__(self, level="info"):
        super().__init__(level=level)

    def job_scheduler_add(self, job):
        pass

    def scheduler_start(self):
        self.scheduler.start()
        # self.scheduler.add_job(clean_check_result, 'interval', seconds=10)
        self.scheduler.add_job(clean_check_result, 'cron', day_of_week='mon-fri', hour=6)


def clean_case():
    logger = ServerLogger(file="server.log").logger
    cases = os.listdir(CASE_ROOT)
    for case in cases:
        t = os.path.getatime(os.path.join(CASE_ROOT, case))
        timestruct = time.localtime(t)
        timestamp = time.strftime("%Y%m%d%H%M%S", timestruct)
        if not difference_time_comparison(timestamp, days=CASE_EXPIRED_DAYS):
            logger.debug("remove expired case: %s" % os.path.join(CASE_ROOT, case))
            shutil.rmtree(os.path.join(CASE_ROOT, case))


class CleanCaseScheduler(SchedulerMain):
    scheduler = None

    def __init__(self, level="info"):
        super().__init__(level=level)

    def job_scheduler_add(self, job):
        pass

    def scheduler_start(self):
        self.scheduler.start()
        # self.scheduler.add_job(clean_case, 'interval', seconds=10)
        self.scheduler.add_job(clean_case, 'cron', day_of_week='mon-fri', hour=6)
