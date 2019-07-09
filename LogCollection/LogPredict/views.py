# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from webpage.models import JobBuild
from DataProcessingAndPlot.log_filter import *

# Create your views here.


def LogPredcitHomePage(request):
    return render(request, 'LogPredict/LogPredictHomePage.html')


def PredictDraft(request):
    context = {}
    if request.method == "POST":
        build_url = request.POST.get('build_url', "")
        build = JobBuild(build_url)
        context['job_name'] = build.get_job_name()
        context['codes_num'] = build.get_codes_num()
        context['duration'] = build.get_duration()
        context['timestamp'] = build.get_timestamp()
        context['exit_status'] = build.get_stat()
        console = build.get_console_text()
        try:
            context['error_context'] = log_filter(console)
        except Exception as e:
            print e
        return render(request, 'LogPredict/LogPredictHomePage.html', context=context)
    return render(request, 'LogPredict/LogPredictHomePage.html')
