# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import os, re, sys
import urllib
from bs4 import BeautifulSoup
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
    error_type = models.TextField()
    description = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.error_type

    class Meta:
        ordering = ('-create_at',)


class LogFile(models.Model):
    log_name = models.CharField(max_length=32)
    team = models.ForeignKey(Team, primary_key=False, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField()
    error_type = models.ForeignKey(ErrorType, primary_key=False, null=True, blank=True, on_delete=models.SET_NULL)
    #uploader = models.CharField()
    upload_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.log_name

    class Meta:
        ordering = ('-upload_time',)


class JobUrlModel(object):
    url = None
    host = None
    html = None
    title = None
    job_name = None
    build_num = None
    stat = None
    parent_job_name = None

    def __init__(self, url, parent_job_name=""):
        if url.split('/')[-1] != 'console':
            url += 'console'
        self.url = url
        try:
            job_url_obj = urllib.urlopen(self.url)
            self.html = BeautifulSoup(job_url_obj, 'html.parser')
        except:
            sys.exit(1)

        proto, rest = urllib.splittype(url)
        res, rest = urllib.splithost(rest)
        self.host = res

        self.title = self.html.title.string
        self.job_name = self.title.split(' ')[0]

        regex = "\d+"
        self.build_num = re.findall(regex, self.title.split(' ')[1])[0]

        self.stat = self.get_stat()
        self.parent_job_name = parent_job_name

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
        console_text_url = self.get_console_text_url()
        console_obj = urllib.urlopen(console_text_url)
        regex = 'Finished:.*'
        stat = re.findall(regex, console_obj.read())[0].split(': ')[1]
        return stat

    def save_console_text(self, path=''):
        console_text_url = self.get_console_text_url()
        console_obj = urllib.urlopen(console_text_url)
        save_filename = "%s_%s_%s.log" % (self.job_name, self.build_num, self.stat)
        if path:
            if not os.path.exists(path):
                os.mkdir(path)
            save_filename = os.path.join(path, save_filename)

        try:
            with open(save_filename, 'w') as fw:
                fw.writelines(console_obj.read())
            print "log save success"
        except:
            print "log save failed"
            return None
        return save_filename

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