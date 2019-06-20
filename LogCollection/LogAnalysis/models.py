# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from webpage.models import *


# Create your models here.
class ScoreStatistic(models.Model):
    job = models.ForeignKey(Job, primary_key=False, null=True, blank=True, on_delete=models.SET_NULL)
    model = models.CharField(max_length=50)
    dataset_num = models.IntegerField(null=False)
    score = models.FloatField()
    training_time = models.DateTimeField(auto_now_add=True, blank=True, null=False)

    class Meta:
        ordering = ('-job', '-model', '-training_time',)

