#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import url
import views

urlpatterns = [
    url(r'^LogPredictHomePage/$', views.LogPredcitHomePage, name='LogPredcitHomePage'),
    url(r'^PredictDraft/$', views.PredictDraft, name='PredictDraft'),
]
