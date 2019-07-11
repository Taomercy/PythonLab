#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import url
from LogAnalysis import views

urlpatterns = [
    url(r'^LogAnalysisPage/$', views.LogAnalysisPage, name='LogAnalysisPage'),

    url(r'^TrainingLogByNaiveBayes/$', views.TrainingLogByNaiveBayes, name='TrainingLogByNaiveBayes'),
    url(r'^TrainingLogByMLP/$', views.TrainingLogByMLP, name='TrainingLogByMLP'),
    url(r'^TrainingLogBySVM/$', views.TrainingLogBySVM, name='TrainingLogBySVM'),
    url(r'^TrainingLogByKMeans/$', views.TrainingLogByKMeans, name='TrainingLogByKMeans'),

    url(r'^LogPredictPage/$', views.LogPredictPage, name='LogPredictPage'),
    url(r'^UploadPredictLog/$', views.UploadPredictLog, name='UploadPredictLog'),
    url(r'^PreditLogDelete/$', views.PreditLogDelete, name='PreditLogDelete'),
    url(r'^PredictByMLP/$', views.PredictByMLP, name='PredictByMLP'),
    url(r'^PredictByBayes/$', views.PredictByBayes, name='PredictByBayes'),

    url(r'^BuildingStatisticPage/$', views.BuildingStatisticPage, name='BuildingStatisticPage'),
    url(r'^BuildingStatisticSubmit/$', views.BuildingStatisticSubmit, name='BuildingStatisticSubmit'),

    url(r'^ScoresStatisticPage/$', views.ScoresStatisticPage, name='ScoresStatisticPage'),
    url(r'^ScoresStatisticSubmit/$', views.ScoresStatisticSubmit, name='ScoresStatisticSubmit'),

    url(r'^MLModelsPage/$', views.MLModelsPage, name='MLModelsPage'),
    url(r'^ModelList/$', views.ModelList, name='ModelList'),
    url(r'^AddModelPage/$', views.AddModelPage, name='AddModelPage'),
    url(r'^AddModel/$', views.AddModel, name='AddModel'),
    url(r'^DeleteModel/$', views.DeleteModel, name='DeleteModel'),

    url(r'^DBInit/$', views.DBInit, name='DBInit'),
]
