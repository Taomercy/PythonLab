# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import os
import urllib
from config import LOG_SAVING_PATH
# Create your models here.


class Team(models.Model):
    name = models.TextField()
    description = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-create_at',)


class ErrorType(models.Model):
    name = models.TextField()
    description = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-create_at',)


class Job(models.Model):
    name = models.TextField()
    url = models.TextField()
    job_dir = models.TextField()
    ismonitored = models.BooleanField()
    fetchSizeOfOneTime = models.IntegerField(default=1)
    fetchFrequency = models.IntegerField(default=3600)
    trainingFrequency = models.IntegerField(default=3600)
    description = models.TextField()
    # latest_config_modify_time = models.TimeField()

    def __str__(self):
        return self.name

    def get_api_url(self):
        return self.url + '/api/python?pretty=true'

    class Meta:
        ordering = ('-name',)


class ExitStatus(models.Model):
    name = models.TextField()
    color = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name


def InitExitStatus():
    if not ExitStatus.objects.filter(name='SUCCESS'):
        ExitStatus.objects.create(name='SUCCESS', color='#008000')
    if not ExitStatus.objects.filter(name='FAILURE'):
        ExitStatus.objects.create(name='FAILURE', color='#FF0000')
    if not ExitStatus.objects.filter(name='UNSTABLE'):
        ExitStatus.objects.create(name='UNSTABLE', color='#FFFF00')
    if not ExitStatus.objects.filter(name='ABORTED'):
        ExitStatus.objects.create(name='ABORTED', color='#808080')


class Log(models.Model):
    name = models.CharField(max_length=32)
    job = models.ForeignKey(Job, primary_key=False, null=True, blank=True, on_delete=models.SET_NULL)
    team = models.ForeignKey(Team, primary_key=False, null=True, blank=True, on_delete=models.SET_NULL)
    codes_number = models.IntegerField()
    istrainingset = models.BooleanField()
    exit_status = models.ForeignKey(ExitStatus, primary_key=False, null=True, blank=True, on_delete=models.SET_NULL)
    error_type = models.ForeignKey(ErrorType, primary_key=False, null=True, blank=True,
                                   on_delete=models.SET_NULL)
    duration = models.FloatField(default=0.0)
    timestamp = models.IntegerField(default=0)

    description = models.TextField(null=True)

    def __str__(self):
        return self.name

    def get_log_path(self):
        return os.path.join(self.job.job_dir, self.name)

    class Meta:
        ordering = ('-timestamp', )


class JobBuild(object):
    job_url = None
    build_url = None
    host = None
    fullDisplayName = None
    job_name = None
    job_dir = None
    build_num = None
    stat = None
    codes_num = None
    duration = None
    building = None
    timestamp = None
    console_text = None

    @staticmethod
    def get_python_api(url):
        return url + '/api/python?pretty=true'

    @staticmethod
    def check_url_visit_code(url):
        job_url_obj = urllib.urlopen(url)
        code = job_url_obj.getcode()
        if code != 200:
            print "[%s] error code" % url, code
            return code
        else:
            return 0

    def __init__(self, build_url, parent_job_name=""):
        self.job_url = '/'.join(build_url.split('/')[:-2])
        job_api = self.get_python_api(self.job_url)
        if self.check_url_visit_code(self.job_url):
            return
        job_data = eval(urllib.urlopen(job_api).read())
        self.job_name = job_data['name']

        self.build_url = build_url
        if self.check_url_visit_code(self.build_url):
            return

        proto, rest = urllib.splittype(build_url)
        res, rest = urllib.splithost(rest)
        self.host = res

        build_api = self.get_python_api(self.build_url)
        build_data = eval(urllib.urlopen(build_api).read())
        self.fullDisplayName = build_data['fullDisplayName']
        self.build_num = build_data['number']
        self.stat = build_data['result']
        self.duration = build_data['duration']
        self.timestamp = build_data['timestamp']
        self.building = build_data['building']

        InitExitStatus()

        job = Job.objects.filter(name=self.job_name)
        if not job:
            self.job_dir = os.path.join(LOG_SAVING_PATH, self.job_name)
            if not os.path.exists(self.job_dir):
                os.makedirs(self.job_dir)
            Job.objects.create(name=self.job_name, url=self.job_url, job_dir=self.job_dir, ismonitored=False)
        else:
            job = Job.objects.get(name=self.job_name)
            if not job.url:
                job.url = self.job_url
            self.job_dir = job.job_dir
            if not job.job_dir:
                job.job_dir = self.job_dir
            job.save()

        console_text_url = self.get_console_text_url()
        console_obj = urllib.urlopen(console_text_url)
        reads = console_obj.read()
        self.console_text = reads
        self.codes_num = len(reads)

    def get_build_url(self):
        return self.build_url

    def get_host(self):
        return self.host

    def get_full_display_name(self):
        return self.fullDisplayName

    def get_job_name(self):
        return self.job_name

    def get_build_num(self):
        return self.build_num

    def get_duration(self):
        return self.duration

    def get_timestamp(self):
        return self.timestamp

    def get_console_text_url(self):
        console_text_url = self.build_url + 'consoleText'
        return console_text_url

    def get_console_text(self):
        return self.console_text

    def get_codes_num(self):
        return self.codes_num

    def get_stat(self):
        return self.stat

    def get_log_name(self):
        log_name = "%s.log" % self.fullDisplayName.replace(' ', '').replace('#','-')
        return log_name

    def save_console_text(self, path=None):
        console_text_url = self.get_console_text_url()
        console_obj = urllib.urlopen(console_text_url)
        code = console_obj.getcode()
        if code != 200:
            # print "[%s] error code" % console_text_url, code
            return 1
        log_name = self.get_log_name()
        if path:
            if not os.path.exists(path):
                os.mkdir(path)
            log_name = os.path.join(path, log_name.replace('/', '_'))
        else:
            log_name = os.path.join(self.job_dir, log_name.replace('/', '_'))

        try:
            with open(log_name, 'w') as fw:
                reads = console_obj.read()
                if not reads:
                    return 3
                fw.writelines(reads)
        except Exception as e:
            print e
            return 2
        return 0

    def data_supplement(self, log_name):
        log = Log.objects.get(name=log_name)
        log.exit_status = ExitStatus.objects.get(name=self.stat)
        log.duration = self.duration
        log.timestamp = self.timestamp
        log.save()

    def save(self, scheduler=False, team_name=None, error_type=None, description=None):
        log_name = self.get_log_name()
        print "start saving [%s]" % log_name
        if Log.objects.filter(name=log_name):
            print "the log has been exist"
            self.data_supplement(log_name)
            return 1

        if self.building is True:
            print "job is building"
            return 1

        param = {}
        param['name'] = log_name
        param['job'] = Job.objects.get(name=self.job_name)
        param['codes_number'] = self.get_codes_num()
        param['istrainingset'] = True
        param['exit_status'] = ExitStatus.objects.get(name=self.stat)
        param['duration'] = self.duration
        param['timestamp'] = self.timestamp
        param['description'] = description
        if scheduler:
            # TODO: Temporarily associate the error type with the exit state
            if not ErrorType.objects.filter(name=self.stat):
                error_type = ErrorType.objects.create(name=self.stat)
            else:
                error_type = ErrorType.objects.get(name=self.stat)
            param['error_type'] = error_type
        else:
            if not team_name:
                print "need param team name"
                return 3
            if not error_type:
                print "need param error type"
                return 4
            param['team'] = Team.objects.get(name=team_name)
            param['error_type'] = ErrorType.objects.get(name=error_type)

        if not os.path.exists(self.job_dir):
            os.makedirs(self.job_dir)
        if self.save_console_text(path=self.job_dir):
            print "save log fail"
            return 2
        else:
            print "console log saved"

        log = Log.objects.create(**param)
        log.save()
        print "[%s] log save success" % self.build_url

        return 0
