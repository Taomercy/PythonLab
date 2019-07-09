#!/usr/bin/env python
# -*- coding:utf-8 -*-
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import time
from webpage.models import *
from AlgorithmModels.NaiveBayesModel import training_by_naive_bayes
from AlgorithmModels.MLPClassifierModel import training_by_SVM_and_MLP
global scheduler


def training_scheduler(job):
    print time.strftime('{%Y-%m-%d %H:%M:%S}', time.localtime(time.time()))
    print "%s training  start" % job.name
    training_by_naive_bayes(job.job_dir, job_name=job.name, scheduler=True)
    training_by_SVM_and_MLP(job.job_dir, job_name=job.name, scheduler=True)
    print "%s training  end" % job.name


class TrainingSchedulerMain(object):
    scheduler = None

    def __init__(self):
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)
        self.scheduler = BackgroundScheduler()

    def job_scheduler_add(self, job):
        if job.ismonitored:
            self.scheduler.add_job(training_scheduler, 'interval', seconds=job.trainingFrequency, args=[job], jitter=600)
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

    def scheduler_start(self):
        self.scheduler.start()
        jobs = Job.objects.filter(ismonitored=True)
        for job in jobs:
            self.scheduler.add_job(training_scheduler, 'interval', seconds=job.trainingFrequency, args=[job], jitter=600)

    def scheduler_shutdown(self, wait=True):
        self.scheduler.shutdown(wait=wait)

    def get_scheduler(self):
        return self.scheduler