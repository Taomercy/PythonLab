#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import url
from webpage import views

urlpatterns = [
    url(r'^UploadLog/$', views.UploadLog, name='UploadLog'),
    url(r'^get_jenkins_log/$', views.get_jenkins_log, name='get_jenkins_log'),
    url(r'^UploadLogHander/$', views.UploadLogHander, name='UploadLogHander'),
    url(r'^BatchCollectionLog/$', views.BatchCollectionLog, name='BatchCollectionLog'),
    url(r'^get_jenkins_log_by_build_num_internal/$', views.get_jenkins_log_by_build_num_internal,
        name='get_jenkins_log_by_build_num_internal'),
    url(r'^InfoFillInPage/$', views.InfoFillInPage, name='InfoFillInPage'),
    url(r'^CreateErrorType/$', views.CreateErrorType, name='CreateErrorType'),
    url(r'^SaveNewErrorType/$', views.SaveNewErrorType, name='SaveNewErrorType'),
    url(r'^CreateTeam/$', views.CreateTeam, name='CreateTeam'),
    url(r'^SaveNewTeam/$', views.SaveNewTeam, name='SaveNewTeam'),
    url(r'^CleanAll/$', views.CleanAll, name='CleanAll'),
]