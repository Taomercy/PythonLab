#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import url
from LogAnalysis import views

urlpatterns = [
    url(r'^LogAnalysisPage/$', views.LogAnalysisPage, name='LogAnalysisPage'),
    url(r'^TrainingLogByNaiveBayes/$', views.TrainingLogByNaiveBayes, name='TrainingLogByNaiveBayes'),
]