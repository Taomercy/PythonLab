#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import url
from LogAnalysis import views

urlpatterns = [
    url(r'^LogAnalysisPage/$', views.LogAnalysisPage, name='LogAnalysisPage'),
    url(r'^PlotCodesNumWithStat/$', views.PlotCodesNumWithStat, name='PlotCodesNumWithStat'),

    url(r'^TrainingLogByNaiveBayes/$', views.TrainingLogByNaiveBayes, name='TrainingLogByNaiveBayes'),
    url(r'^TrainingLogBySVMAndMLP/$', views.TrainingLogBySVMAndMLP, name='TrainingLogBySVMAndMLP'),
    url(r'^TrainingLogByKMeans/$', views.TrainingLogByKMeans, name='TrainingLogByKMeans'),

    url(r'^LogPredictPage/$', views.LogPredictPage, name='LogPredictPage'),
    url(r'^UploadPredictLog/$', views.UploadPredictLog, name='UploadPredictLog'),
    url(r'^PreditLogDelete/$', views.PreditLogDelete, name='PreditLogDelete'),
    url(r'^PredictByMLP/$', views.PredictByMLP, name='PredictByMLP'),
    url(r'^PredictByBayes/$', views.PredictByBayes, name='PredictByBayes'),

    url(r'^ScoresStatisticPage/$', views.ScoresStatisticPage, name='ScoresStatisticPage'),
    url(r'^ScoresStatistic/$', views.ScoresStatistic, name='ScoresStatistic'),
]
