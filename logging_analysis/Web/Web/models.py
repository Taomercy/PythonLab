import datetime
import os

from django.db import models

# Create your models here.
from django.db.models import PROTECT

from Web.settings import CASE_DIR, BASE_DIR
from Web.utils import un_tar


class MHWeb(models.Model):
    eriref = models.CharField(primary_key=True, max_length=254)
    heading = models.CharField(max_length=100)
    register_date = models.CharField(max_length=100)
    reporter = models.TextField()
    env_config = models.TextField(blank=True, null=True)

    @staticmethod
    def get_thread():
        return ["ERIREF", "Heading", "Register Date", "Reporter", "Env Config"]

    def __str__(self):
        return self.eriref


class Tar(models.Model):
    filename = models.CharField(primary_key=True, max_length=100)
    abspath = models.CharField(max_length=100)
    uploader = models.CharField(max_length=100)
    upload_time = models.DateTimeField(auto_now=True)
    untar_dir = None

    @staticmethod
    def get_thread():
        return ["Filename", "Uploader", "Upload time"]

    def __str__(self):
        return self.filename

    def get_abspath(self):
        return os.path.join(CASE_DIR, str(self.filename))

    def untar(self):
        now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        dirname = "untar_dir_%s" % now
        untar_dir = os.path.join(BASE_DIR, dirname)
        un_tar(self.get_abspath(), untar_dir)
        case_path = os.path.join(untar_dir, os.listdir(untar_dir)[0])
        self.untar_dir = untar_dir
        return case_path

    def get_untar_dir(self):
        return self.untar_dir


class AppLogType(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    release_version = models.CharField(max_length=50, blank=True, null=True)
    count = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_thread():
        return ["Type name", "Release Version", "Count", "Create Time"]

    def __str__(self):
        return self.name


class UnstabilityProperty(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    free_memory_delta_rate = models.FloatField(default=0.3)
    create_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_thread():
        return ["Name", "Create Time"]

    def __str__(self):
        return self.name
