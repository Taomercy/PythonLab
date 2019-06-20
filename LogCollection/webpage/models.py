# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import os, re, sys
import urllib
from bs4 import BeautifulSoup
from webpage.config import LOG_SAVING_PATH
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
    fetchFrequency = models.IntegerField()
    trainingFrequency = models.IntegerField()
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
    description = models.TextField()


class Log(models.Model):
    name = models.CharField(max_length=32)
    job = models.ForeignKey(Job, primary_key=False, null=True, blank=True, on_delete=models.SET_NULL)
    team = models.ForeignKey(Team, primary_key=False, null=True, blank=True, on_delete=models.SET_NULL)
    codes_number = models.IntegerField()
    istrainingset = models.BooleanField()
    exit_status = models.ForeignKey(ExitStatus, primary_key=False, null=True, blank=True, on_delete=models.SET_NULL)
    error_type = models.ForeignKey(ErrorType, primary_key=False, null=True, blank=True,
                                   on_delete=models.SET_NULL)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name

    def get_log_path(self):
        return os.path.join(self.job.job_dir, self.name)

    class Meta:
        ordering = ('-name',)


class JobUrlModel(object):
    job_url = None
    url = None
    host = None
    html = None
    title = None
    job_name = None
    job_dir = None
    build_num = None
    build_label = None
    stat = None
    parent_job_name = None
    codes_num = None
    console_obj = None

    def __init__(self, url, parent_job_name=""):
        self.job_url = '/'.join(url.split('/')[:-2])

        if url.split('/')[-1] != 'console':
            url += 'console'
        self.url = url
        try:
            job_url_obj = urllib.urlopen(self.url)
            self.html = BeautifulSoup(job_url_obj, 'html.parser')
        except:
            return

        proto, rest = urllib.splittype(url)
        res, rest = urllib.splithost(rest)
        self.host = res

        self.title = self.html.title.string
        self.job_name = self.title.split(' ')[0]
        self.build_label = self.title.split(' ')[1]

        regex = "\d+"
        self.build_num = re.findall(regex, self.title.split(' ')[1])[0]
        self.parent_job_name = parent_job_name

        console_text_url = self.get_console_text_url()
        console_obj = urllib.urlopen(console_text_url)
        code = console_obj.getcode()
        if code != 200:
            print "[%s] error code" % console_text_url, code
            return
        regex = 'Finished:.*'
        try:
            stat = re.findall(regex, console_obj.read())[-1].split(': ')[1]
            self.stat = stat
        except Exception as e:
            print "Error of getting stat [%s]" % e
            return
        if not ExitStatus.objects.filter(name=stat):
            ExitStatus.objects.create(name=stat)

        job = Job.objects.filter(name=self.job_name)
        if not job:
            self.job_dir = os.path.join(LOG_SAVING_PATH, self.job_name)
            if not os.path.exists(self.job_dir):
                os.makedirs(self.job_dir)
            Job.objects.create(name=self.job_name, url=self.job_url, job_dir=self.job_dir, ismonitored=False)
        else:
            if not job[0].url:
                job[0].url = self.job_url
            self.job_dir = job[0].job_dir
            if not job[0].job_dir:
                job[0].job_dir = self.job_dir
            job[0].save()

    def get_url(self):
        return self.url

    def get_host(self):
        return self.host

    def get_html(self):
        return self.html

    def get_title(self):
        return self.title

    def get_job_name(self):
        return self.job_name

    def get_build_num(self):
        return self.build_num

    def get_console_text_url(self):
        console_text_url = self.url.replace('console', 'consoleText')
        return console_text_url

    def get_stat(self):
        return self.stat

    def get_log_name(self):
        log_name = "%s_%s.log" % (self.job_name, self.build_label)
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
                    return None
                fw.writelines(reads)
                self.codes_num = len(reads)
        except:
            return 2
        return 0

    def get_codes_num(self):
        return self.codes_num

    def get_img_from_html(self):
        imgs = self.html.find_all('img')
        return imgs

    def get_links_from_html(self):
        links_list = []
        links = self.html.find_all('a')
        for link in links:
            lk = "https://" + str(self.host) + str(link.get('href'))
            links_list.append(lk)
        return links_list

    def find_sub_job_link(self):
        links_list = self.get_links_from_html()
        sub_job_list = []
        regex = r'job/.*/[0-9]{0,10}/$'
        for link in links_list:
            if re.findall(regex, link):
                if self.job_name in link or 'ExecuteTestSuite' in link:
                    continue
                link_model = JobUrlModel(link)
                if "Error report" in link_model.get_title():
                    continue
                sub_job_list.append(link)
        return sub_job_list

    def save(self, scheduler=False, team_name=None, error_type=None, description=None):
        log_name = self.get_log_name()
        print "start saving [%s]" % log_name
        if Log.objects.filter(name=log_name):
            print "the log has been exist"
            return 1

        if self.save_console_text():
            print "save log fail"
            return 2
        else:
            print "console log saved"

        if scheduler:
            # TODO: Temporarily associate the error type with the exit state
            if not ErrorType.objects.filter(name=self.stat):
                error_type = ErrorType.objects.create(name=self.stat)
            else:
                error_type = ErrorType.objects.get(name=self.stat)
            log = Log.objects.create(name=log_name,
                                     job=Job.objects.get(name=self.job_name),
                                     codes_number=self.get_codes_num(),
                                     istrainingset=False,
                                     exit_status=ExitStatus.objects.get(name=self.stat),
                                     error_type=error_type)
        else:
            if not team_name:
                print "need param team name"
                return 3
            if not error_type:
                print "need param error type"
                return 4
            log = Log.objects.create(name=log_name,
                                     job=Job.objects.get(name=self.job_name),
                                     team=Team.objects.get(name=team_name),
                                     codes_number=self.get_codes_num(),
                                     istrainingset=False,
                                     exit_status=ExitStatus.objects.get(name=self.stat),
                                     error_type=ErrorType.objects.get(name=error_type),
                                     description=description)
        log.save()
        print "[%s] log save success" % self.url
        return 0





