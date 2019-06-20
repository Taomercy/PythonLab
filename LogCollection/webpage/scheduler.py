#!/usr/bin/env python
# -*- coding:utf-8 -*-
from models import *
from apscheduler.schedulers.background import BackgroundScheduler
import logging


def fetch_logs(job):
    job_api = job.get_api_url()
    size = job.fetchSizeOfOneTime
    data = eval(urllib.urlopen(job_api).read())
    builds = data['builds']
    sum = 0
    for build in builds:
        u = build['url']
        print u
        try:
            JobUrlModel(u).save(scheduler=True)
        except Exception as e:
            print e
            continue
        sum += 1
        if sum == size:
            break


class FetchingSchedulerMain():
    scheduler = None

    def __init__(self, now_start=False):
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        jobs = Job.objects.filter(ismonitored=True)
        for job in jobs:
            if now_start:
                self.scheduler.add_job(fetch_logs, args=[job])
            self.scheduler.add_job(fetch_logs, 'interval', seconds=job.fetchFrequency, args=[job])

    def job_scheduler_add(self, job):
        if job.ismonitored:
            self.scheduler.add_job(fetch_logs, 'interval', seconds=job.fetchFrequency, args=[job])
            return 0
        return 1

    def job_scheduler_delete(self, job):
        for task in self.scheduler.get_jobs():
            if task.args[0].name == job.name:
                self.scheduler.remove_job(task.id)
                return 0
        return 1

    def job_scheduler_update(self, job):
        if not self.job_scheduler_check(job):
            self.job_scheduler_delete(job)
            self.job_scheduler_add(job)
        else:
            self.job_scheduler_add(job)

    def job_scheduler_check(self, job):
        for task in self.scheduler.get_jobs():
            if task.args[0].name == job.name:
                return 0
        return 1

    def scheduler_shutdown(self, wait=True):
        self.scheduler.shutdown(wait=wait)

    def get_scheduler(self):
        return self.scheduler