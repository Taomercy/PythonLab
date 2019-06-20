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

    url(r'^LogDelete/$', views.LogDelete, name='LogDelete'),
    url(r'^LogEditPage/$', views.LogEditPage, name='LogEditPage'),
    url(r'^LogEditSubmit/$', views.LogEditSubmit, name='LogEditSubmit'),

    url(r'^ErrorTypeDelete/$', views.ErrorTypeDelete, name='ErrorTypeDelete'),
    url(r'^ErrorTypeEditPage/$', views.ErrorTypeEditPage, name='ErrorTypeEditPage'),
    url(r'^ErrorTypeEditSubmit/$', views.ErrorTypeEditSubmit, name='ErrorTypeEditSubmit'),

    url(r'^LogTextPage/$', views.LogTextPage, name='LogTextPage'),

    url(r'^LogSelect/$', views.LogSelect, name='LogSelect'),
    url(r'^SelectedLogsUpdateErrorTypes/$', views.SelectedLogsUpdateErrorTypes, name='SelectedLogsUpdateErrorTypes'),
    url(r'^SelectedLogsDelete/$', views.SelectedLogsDelete, name='SelectedLogsDelete'),


    url(r'^SchedulerPage/$', views.SchedulerPage, name='SchedulerPage'),
    url(r'^JobEditPage/$', views.JobEditPage, name='JobEditPage'),
    url(r'^JobEditSubmit/$', views.JobEditSubmit, name='JobEditSubmit'),
    url(r'^Joblist/$', views.Joblist, name='Joblist'),
    url(r'^SaveNewJob/$', views.SaveNewJob, name='SaveNewJob'),
    url(r'^AddNewJobPage/$', views.AddNewJobPage, name='AddNewJobPage'),
    url(r'^JobDelete/$', views.JobDelete, name='JobDelete'),
    url(r'^JobsDelete/$', views.JobsDelete, name='JobsDelete'),

    url(r'^CleanAll/$', views.CleanAll, name='CleanAll'),
]