# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
# Create your views here.
from models import *
from config import *
from django.contrib import messages
import shutil


def search_all_error_type():
    context = {}
    ErrorTypes = ErrorType.objects.all()
    context['ErrorTypes'] = ErrorTypes
    theader = ['Error Name', 'Description', 'Create at']
    context['theader'] = theader
    return context


def search_all_teams():
    context = {}
    Teams = Team.objects.all()
    context['Teams'] = Teams
    theader = ['Team Name', 'Description', 'Create at']
    context['theader'] = theader
    return context


def search_all_logs():
    logs = LogFile.objects.all()
    theader = ['Log Name', 'Team', 'ErrorType', 'Description', 'Upload Time']
    context = {}
    context['logs'] = logs
    context['theader'] = theader
    return context


def CleanAll(request):
    for team in Team.objects.all():
        team.delete()
    Team.objects.create(name="Undefine Team", description="Undefine the team")

    for log in LogFile.objects.all():
        log.delete()

    for error in ErrorType.objects.all():
        error.delete()
    ErrorType.objects.create(error_type="Undefine Error", description="Undefine the error type")

    try:
        shutil.rmtree(LOG_SAVING_PATH)
        msg = "%s has been deleted" % LOG_SAVING_PATH
    except:
        msg = "something wrong for delete %s" % LOG_SAVING_PATH

    messages.success(request, msg)

    context = search_all_logs()
    return render(request, 'webpage/LogDisplay.html', context=context)


def LogDisplay(request):
    context = search_all_logs()
    return render(request, 'webpage/LogDisplay.html', context=context)


def InfoFillInPage(request):
    context = search_all_error_type()
    context.update(search_all_teams())
    return render(request, 'webpage/InfoFillInPage.html', context=context)


def BatchCollectionLog(request):
    context = search_all_error_type()
    context.update(search_all_teams())
    return render(request, 'webpage/BatchCollectionLog.html', context=context)


def UploadLog(request):
    context = search_all_error_type()
    context.update(search_all_teams())
    return render(request, 'webpage/UploadLog.html', context=context)


def CreateErrorType(request):
    context = search_all_error_type()
    return render(request, 'webpage/CreateErrorType.html', context=context)


def SaveNewErrorType(request):
    context = search_all_error_type()
    if request.method == "POST":
        new_error_type = request.POST.get('new_error_type', None)
        description = request.POST.get('description', "")
        errors = [error.error_type for error in context['ErrorTypes']]
        if new_error_type in errors:
            messages.success(request, "the error type is exist")
            return render(request, 'webpage/CreateErrorType.html', context=context)
        ErrorType.objects.create(error_type=new_error_type, description=description).save()
        messages.success(request, "create new error type success!")

    return render(request, 'webpage/CreateErrorType.html', context=search_all_error_type())


def CreateTeam(request):
    context = search_all_teams()
    return render(request, 'webpage/CreateTeam.html', context=context)


def SaveNewTeam(request):
    context = search_all_teams()
    if request.method == "POST":
        new_team = request.POST.get('new_team', None)
        description = request.POST.get('description', "")
        teams = [team.name for team in context['Teams']]
        if new_team in teams:
            messages.success(request, "the team is exist")
            return render(request, 'webpage/CreateTeam.html', context=context)
        Team.objects.create(name=new_team, description=description).save()
        messages.success(request, "create new team success!")

    return render(request, 'webpage/CreateTeam.html', context=search_all_teams())


def UploadLogHander(request):
    context = search_all_error_type()
    context.update(search_all_teams())
    if request.method == "POST":
        log_file = request.FILES['logfile']
        team = request.POST.get('team', None)
        description = request.POST.get('description', "")
        error_type = request.POST.get('error_type', "")
        save_path = os.path.join(LOG_SAVING_PATH, team)
        print "team_path:", save_path
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        log_name = os.path.join(save_path, log_file.name)
        with open(log_name, 'wb+') as fw:
            # 根据上传的流中的数据一点一点往内存中写
            for c in log_file.chunks():
                fw.write(c)

        log = LogFile.objects.create(log_name=log_file.name,
                                     team=Team.objects.all().get(name=team),
                                     description=description,
                                     error_type=ErrorType.objects.all().get(error_type=error_type))
        log.save()

        messages.success(request, "哈哈哈哈，上传成功啦!")
        return render(request, 'webpage/UploadLog.html', context=context)
    else:
        messages.error(request, "ERROR")
        return render(request, 'webpage/UploadLog.html', context=context)


def get_jenkins_log(request):
    if request.method == "POST":
        url = request.POST.get('log_url', None)
        team = request.POST.get('team', None)
        error_type = request.POST.get('error_type', "")
        description = request.POST.get('description', "")
        job_url = JobUrlModel(url)
        team_path = os.path.join(LOG_SAVING_PATH, team, job_url.get_job_name())
        if not os.path.exists(team_path):
            os.makedirs(team_path)
        log_filename = job_url.save_console_text(team_path)

        log = LogFile.objects.create(log_name=os.path.basename(log_filename),
                                     team=Team.objects.all().get(name=team),
                                     description=description,
                                     error_type=ErrorType.objects.all().get(error_type=error_type))
        log.save()
        messages.success(request, "哈哈哈哈，上传成功啦!")

    context = search_all_logs()
    return render(request, 'webpage/LogDisplay.html', context=context)


def get_jenkins_log_by_build_num_internal(request):
    if request.method == "POST":
        job_home_url = request.POST.get('job_home_url', None)
        team = request.POST.get('team', None)
        error_type = request.POST.get('error_type', "")
        description = request.POST.get('description', "")
        build_num_start = request.POST.get('build_num_start', 0)
        build_num_end = request.POST.get('build_num_end', 1)
        build_num_vector = [num for num in range(int(build_num_start), int(build_num_end))]
        url_list = [job_home_url+str(build_num)+"/console" for build_num in build_num_vector]

        for url in url_list:
            try:
                print "url:", url
                job_url = JobUrlModel(url)
                team_path = os.path.join(LOG_SAVING_PATH, team, job_url.get_job_name())
                if not os.path.exists(team_path):
                    os.makedirs(team_path)
                log_filename = job_url.save_console_text(team_path)
                log = LogFile.objects.create(log_name=os.path.basename(log_filename),
                                             team=Team.objects.all().get(name=team),
                                             description=description,
                                             error_type=ErrorType.objects.all().get(error_type=error_type))
                log.save()
            except Exception as error:
                print "log save error:", error
                continue
        messages.success(request, "哈哈哈哈，上传成功啦!")

    context = search_all_logs()
    return render(request, 'webpage/LogDisplay.html', context=context)
