# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404
from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
import json
import shutil
import threading
from LogCollection.views import Fsche, Tsche
from models import *
from config import *

# Create your views here.
global filter_logs
for job in Job.objects.all():
    old_path = job.job_dir
    if old_path.split('LogSavingPath')[0] != home_path:
        new_path = os.path.join(home_path, 'LogSavingPath', old_path.split('LogSavingPath')[-1][1:])
        try:
            shutil.move(old_path, new_path)
        except Exception as e:
            print e
        job.job_dir = new_path
        job.save()


def homepage(request):
    context = search_all_logs()
    return render(request, 'webpage/LogDisplay.html', context=context)


def search_all_jobs():
    context = {}
    theader = ['Job Name', 'Job_url', 'Ismonitored', 'FetchSizeOfOneTime', 'TimeSetting', 'Description']
    context['theader'] = theader

    return context


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
    context = {}
    logs = Log.objects.all()
    context['logs'] = logs
    context['logs_number'] = len(logs)

    global filter_logs
    filter_logs = logs
    context.update(get_all_select())

    return context


def get_all_select():
    context = {}
    theader = ['Log Name', 'Team', 'ErrorType', 'Exit Status', 'Codes Number', 'Is training set', 'Duration', 'Timestamp', 'Description']
    context['theader'] = theader
    context['Teams'] = Team.objects.all()
    context['ErrorTypes'] = ErrorType.objects.all()
    status = ExitStatus.objects.all()
    for statu in status:
        if not Log.objects.filter(exit_status=statu):
            statu.delete()
    context['Status'] = ExitStatus.objects.all()
    return context


def CleanAll(request):
    for team in Team.objects.all():
        team.delete()
    Team.objects.create(name="Undefine Team", description="Undefine the team")
    Team.objects.create(name="UPG", description="")
    Team.objects.create(name="HSS", description="")

    for log in Log.objects.all():
        log.delete()

    for error in ErrorType.objects.all():
        error.delete()

    ErrorType.objects.create(name="SUCCESS", description="")
    ErrorType.objects.create(name="ABORTED", description="")
    ErrorType.objects.create(name="Undefine Error", description="Undefine the error type")
    ErrorType.objects.create(name="GicCloneError", description="Git clone error")
    ErrorType.objects.create(name="DenpendenciesError", description="Could not resolve dependencies")

    for stat in ExitStatus.objects.all():
        stat.delete()

    try:
        shutil.rmtree(LOG_SAVING_PATH)
        msg = "%s has been deleted" % LOG_SAVING_PATH
    except:
        msg = "something wrong for delete %s" % LOG_SAVING_PATH

    messages.success(request, msg)

    context = search_all_logs()
    return render(request, 'webpage/LogDisplay.html', context=context)


def LogCollection(request):
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

        if ErrorType.objects.filter(name=new_error_type):
            messages.success(request, "the error type is exist")
            return render(request, 'webpage/CreateErrorType.html', context=context)

        ErrorType.objects.create(name=new_error_type, description=description).save()
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

        if Team.objects.filter(name=new_team):
            messages.success(request, "the team is exist")
            return render(request, 'webpage/CreateTeam.html', context=context)

        Team.objects.create(name=new_team, description=description).save()
        messages.success(request, "create new team success!")

    return render(request, 'webpage/CreateTeam.html', context=search_all_teams())


def UploadLogHander(request):
    context = search_all_error_type()
    context.update(search_all_teams())
    if not Job.objects.filter(name="Upload job"):
        Job.objects.create(name="Upload job", ismonitored=False)
    if not ExitStatus.objects.filter(name='Unknown'):
        ExitStatus.objects.create(name='Unknown')

    if request.method == "POST":
        log_file = request.FILES.getlist('logfile', [])
        team = request.POST.get('team', None)
        description = request.POST.get('description', "")
        error_type = request.POST.get('error_type', None)
        save_path = os.path.join(LOG_SAVING_PATH, "Upload job")

        for file in log_file:
            if Log.objects.filter(name=file.name):
                msg = "the log file[%s] has been exist" % file.name
                print msg
                messages.error(request, msg)
                continue

            if not os.path.exists(save_path):
                os.makedirs(save_path)

            log_name = os.path.join(save_path, file.name)
            with open(log_name, 'wb+') as fw:
                # 根据上传的流中的数据一点一点往内存中写
                for c in file.chunks():
                    fw.write(c)
                codes_num = len(fw.read())

            log = Log.objects.create(name=os.path.basename(log_name),
                                     job=Job.objects.get(name="Upload job"),
                                     codes_number=codes_num,
                                     istrainingset=False,
                                     description=description)
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
        build = JobBuild(url)
        if not build.save(scheduler=False, team_name=team, error_type=error_type, description=description):
            messages.success(request, "哈哈哈哈，上传成功啦!")
        else:
            messages.error(request, "哦哟， 失败了呀！")

    context = search_all_logs()
    return render(request, 'webpage/LogDisplay.html', context=context)


def get_jenkins_log_by_build_num_internal(request):
    class MyThread(threading.Thread):
        def __init__(self, threadID, url):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.url = url

        def run(self):
            threadLock = threading.Lock()
            # print "Starting thread [%d]" % self.threadID
            print "fetching log:", self.url
            build = JobBuild(self.url)
            threadLock.acquire()
            build.save(scheduler=True)
            threadLock.release()
            # print "Exiting thread [%d]" % self.threadID

    if request.method == "POST":
        job_home_url = request.POST.get('job_home_url', None)
        description = request.POST.get('description', "")
        build_num_start = request.POST.get('build_num_start', 0)
        build_num_end = request.POST.get('build_num_end', 1)
        build_num_vector = [num for num in range(int(build_num_start), int(build_num_end))]
        url_list = [job_home_url+str(build_num) + '/' for build_num in build_num_vector]

        threads = []
        threadID = 1
        for url in url_list:
            thread = MyThread(threadID, url)
            thread.start()
            threads.append(thread)
            threadID += 1

        for t in threads:
            t.join()
        print "All catching log threads exited!"
        messages.success(request, "哈哈哈哈，上传成功啦!")

    context = search_all_logs()
    return render(request, 'webpage/LogDisplay.html', context=context)


def ErrorTypeDelete(request):
    if request.method == "POST":
        error_type_delete = request.POST.get('error_type_delete', None)
        if error_type_delete is None:
            raise Http404("The error_type_delete is None")

        try:
            error_obj = ErrorType.objects.get(name=error_type_delete)
            logs_for_error = Log.objects.filter(name=error_obj)
            for log in logs_for_error:
                log.error_type = ErrorType.objects.get(name="Undefine Error")
                log.save()
            error_obj.delete()
        except:
            messages.error(request, "delete error!")

        messages.success(request, "delete success!")

    return render(request, 'webpage/CreateErrorType.html', context=search_all_error_type())


def ErrorTypeEditPage(request):
    context = {}
    if request.method == "POST":
        error_type = request.POST.get('error_type_edit', None)
        try:
            error_type = ErrorType.objects.get(name=error_type)
        except:
            error_type = None
        context['edit_error'] = error_type

    return render(request, 'webpage/ErrorTypeEditPage.html', context=context)


def ErrorTypeEditSubmit(request):
    if request.method == "POST":
        error_name = request.POST.get('error_name', None)
        error_name_editing = request.POST.get('error_name_editing', "")
        description_editing = request.POST.get('description_editing', "")

        error = ErrorType.objects.get(name=error_name)
        logs = Log.objects.filter(name=error)

        error.name = error_name_editing
        error.description = description_editing
        error.save()

        new_error = ErrorType.objects.get(name=error_name_editing)
        for log in logs:
            log.error_type = new_error
            log.save()

        print "%s has been update" % error_name
        messages.success(request, "update success!")

    return render(request, 'webpage/CreateErrorType.html', context=search_all_error_type())


def LogDelete(request):
    if request.method == "GET":
        log_name = request.GET.get('log_name', None)
        if log_name is None:
            raise Http404("The log name is None")

        try:
            os.remove(Log.objects.get(name=log_name).get_log_path())
            Log.objects.get(name=log_name).delete()
            print "%s has been deleted" % log_name
        except:
            logs = Log.objects.filter(name=log_name)

            for log in logs:
                try:
                    os.remove(log.get_log_path()())
                except Exception as e:
                    print e
                print "%s has been deleted" % log_name
            logs.delete()

        messages.success(request, "delete success!")

    context = search_all_logs()
    return render(request, 'webpage/LogDisplay.html', context=context)


def LogsDelete(request):
    if request.method == "POST":
        logs_name = request.POST.getlist("logs_name")
        for log_name in logs_name:
            if log_name is None:
                raise Http404("The log name is None")
            try:
                os.remove(Log.objects.get(name=log_name).get_log_path())
                Log.objects.get(name=log_name).delete()
            except:
                logs = Log.objects.filter(name=log_name)
                for log in logs:
                    try:
                        os.remove(log.get_log_path()())
                    except Exception as e:
                        print e
                    print "%s has been deleted" % log_name
                logs.delete()
    return HttpResponse('{"status":"success"}', content_type='application/json')

def LogEditPage(request):
    context = {}
    if request.method == "GET":
        log_name = request.GET.get('log_name', None)
        try:
            log = Log.objects.get(name=log_name)
        except:
            log = Log.objects.filter(name=log_name)
        context['edit_log'] = log

    context.update(search_all_teams())
    context.update(search_all_error_type())
    return render(request, 'webpage/LogEditPage.html', context=context)


def LogEditSubmit(request):
    if request.method == "POST":
        log_name = request.POST.get('log_name', None)
        log_name_editing = request.POST.get('log_name_editing', None)
        team_editing = request.POST.get('team_editing', "")
        error_type_editing = request.POST.get('error_type_editing', "")
        description_editing = request.POST.get('description_editing', "")

        log = Log.objects.get(name=log_name)
        log.name = log_name_editing

        log.team = Team.objects.get(name=team_editing)
        log.error_type = ErrorType.objects.get(name=error_type_editing)
        log.description = description_editing
        log.save()

        print "%s has been update" % log_name
        messages.success(request, "update success!")

    context = search_all_logs()
    return render(request, 'webpage/LogDisplay.html', context=context)


def LogTextPage(request):
    context = search_all_logs()
    if request.method == "GET":
        log_name = request.GET.get('log_name', None)
        log_path = Log.objects.get(name=log_name).get_log_path()
        with open(log_path, 'r') as fr:
            log_txt = fr.readlines()
        try:
            context['log_txt'] = [u'%s' % line for line in log_txt]
        except Exception as e:
            messages.error(request, e)
            print "read log error"
            return render(request, 'webpage/LogDisplay.html', context=context)
        return render(request, 'webpage/LogTextPage.html', context=context)

    return render(request, 'webpage/LogDisplay.html', context=context)


def LogSelect(request):
    def tableData(request, dataList):
        if request.method == "POST":
            limit = request.POST.get('limit')  # how many items per page
            offset = request.POST.get('offset')  # how many items in preview pages

            if dataList:
                response_data = {'total': dataList.count(), 'rows': []}
                if not offset:
                    offset = 0
                if not limit:
                    limit = 10
                page = int(int(offset) / int(limit) + 1)
                pageinator = Paginator(dataList, limit)  # 开始做分页
                data = pageinator.page(page)

                for log in data:
                    response_data['rows'].append({
                        "name": log.name,
                        "job": str(log.job),
                        "team": str(log.team),
                        "codes_number": log.codes_number,
                        "istrainingset": log.istrainingset,
                        "exit_status": str(log.exit_status),
                        "error_type": str(log.error_type),
                        "duration": log.duration,
                        "timestamp": log.timestamp,
                        "description": log.description,
                    })
                return HttpResponse(json.dumps(response_data))  # 需要json处理下数据格式
            else:
                return HttpResponse(json.dumps({'total': 0, 'rows': []}))
    logs = []
    context = get_all_select()
    if request.method == "POST":
        log_name_condition = request.POST.get('log_name', None)
        team_condition = request.POST.get('team', None)
        error_type_condition = request.POST.get('error_type', None)
        exit_status_condition = request.POST.get('exit_status', None)
        logs = Log.objects.all()

        if log_name_condition:
            logs = logs.filter(name__contains=log_name_condition)
        if team_condition:
            logs = logs.filter(team=Team.objects.get(name=team_condition))
        if error_type_condition:
            logs = logs.filter(error_type=ErrorType.objects.get(name=error_type_condition))
        if exit_status_condition:
            logs = logs.filter(exit_status=ExitStatus.objects.get(name=exit_status_condition))

        global filter_logs
        filter_logs = logs
        context['logs'] = logs
        context['logs_number'] = len(logs)
    return tableData(request, logs)
    # return render(request, 'webpage/LogDisplay.html', context=context)


def SelectedLogsUpdateErrorTypes(request):
    context = get_all_select()
    if request.method == "POST":
        error = request.POST.get('error', None)
        global filter_logs
        for log in filter_logs:
            log.error_type = ErrorType.objects.get(name=error)
            log.save()

        context['logs'] = filter_logs
        context['logs_number'] = len(filter_logs)

    return render(request, 'webpage/LogDisplay.html', context=context)


def SelectedLogsDelete(request):
    global filter_logs
    for log in filter_logs:
        try:
            os.remove(Log.objects.get(name=log.name).get_log_path())
            log.delete()
        except:
            log.delete()
            continue
        print "%s has been deleted" % log.name
    messages.success(request, "delete success!")
    context = search_all_logs()
    return render(request, 'webpage/LogDisplay.html', context=context)


def SchedulerPage(request):
    return render(request, 'webpage/Scheduler.html')


def Joblist(request):
    def tableData(request, dataList):
        if request.method == "POST":
            limit = request.POST.get('limit')  # how many items per page
            offset = request.POST.get('offset')  # how many items in total in the DB
            # jobs = Job.objects.all()

            if dataList:
                response_data = {'total': dataList.count(), 'rows': []}
                if not offset:
                    offset = 0
                if not limit:
                    limit = 10
                page = int(int(offset) / int(limit) + 1)
                pageinator = Paginator(dataList, limit)  # 开始做分页
                data = pageinator.page(page)

                for job in data:
                    response_data['rows'].append({
                        "Name": job.name,
                        "Url": job.url,
                        "Log_dir": job.job_dir,
                        "Monitor_status": job.ismonitored,
                        "FetchSizeOfOneTime": job.fetchSizeOfOneTime,
                        "FetchFrequency": job.fetchFrequency,
                        "TrainingFrequency": job.trainingFrequency,
                        "Description": job.description,
                    })
                return HttpResponse(json.dumps(response_data))  # 需要json处理下数据格式
            else:
                return HttpResponse(json.dumps({'total': 0, 'rows': []}))
    jobs = []
    if request.method == "POST":
        name = request.POST.get('job_name')
        status = request.POST.get('monitor_status')
        jobs = Job.objects.all()
        if name:
            jobs = jobs.filter(name__contains=name)
        if status:
            if status.lower() == 'true':
                status = True
            elif status.lower() == 'false':
                status = False
            jobs = jobs.filter(ismonitored=status)
    return tableData(request, jobs)


def AddNewJobPage(request):
    return render(request, 'webpage/JobAddPage.html')


def SaveNewJob(request):
    if request.method == "POST":
        name = request.POST.get('name', None)
        url = request.POST.get('url', None)
        job_dir = request.POST.get('job_dir', None)
        ismonitored = request.POST.get('ismonitored', None)
        ismonitored = True if ismonitored.lower() == 'true' else False
        fetchSizeOfOneTime = request.POST.get('fetchSizeOfOneTime', None)
        fetchFrequency = int(request.POST.get('fetchFrequency', None))
        trainingFrequency = int(request.POST.get('trainingFrequency', None))
        description = request.POST.get('description', "")
        startNow = request.POST.get('startNow', None)
        startNow = True if startNow.lower() == 'true' else False
        jobFetchSizeForStartNow = request.POST.get('jobFetchSizeForStartNow', None)

        if Job.objects.filter(name=name):
            messages.success(request, "the job is exist")
            return render(request, 'webpage/JobAddPage.html')

        job_dir = os.path.join(LOG_SAVING_PATH, name)
        if not os.path.exists(job_dir):
            os.makedirs(job_dir)
        Job.objects.create(name=name, url=url, job_dir=job_dir, ismonitored=ismonitored,
                           fetchSizeOfOneTime=fetchSizeOfOneTime, fetchFrequency=fetchFrequency,
                           trainingFrequency=trainingFrequency, description=description).save()
        messages.success(request, "create new scedule job success!")
        job = Job.objects.get(name=name)
        if startNow:
            job.fetchSizeOfOneTime = jobFetchSizeForStartNow
        Fsche.job_scheduler_add(job, start_now=startNow)
        Tsche.job_scheduler_add(job)
    return render(request, 'webpage/Scheduler.html', context=search_all_error_type())


def JobDelete(request):
    context = search_all_jobs()
    jobs = Job.objects.all()
    context['jobs'] = jobs
    if request.method == "POST":
        job_name = request.POST.get('job_name', None)
        try:
            job = Job.objects.get(name=job_name)
            Tsche.job_scheduler_delete(job)
            Fsche.job_scheduler_delete(job)
            job.delete()
        except Exception as e:
            print e
            messages.error(request, e)
            return render(request, 'webpage/Scheduler.html', context=context)

        messages.success(request, "delete success!")
    return render(request, 'webpage/Scheduler.html', context=context)


def JobsDelete(request):
    context = search_all_jobs()
    jobs = Job.objects.all()
    context['jobs'] = jobs
    if request.method == "POST":
        # jobs_name = json.loads(request.body.decode("utf8"))
        jobs_name = request.POST.getlist("jobs_name")
        for job_name in jobs_name:
            try:
                job = Job.objects.get(name=job_name)
                Tsche.job_scheduler_delete(job)
                Fsche.job_scheduler_delete(job)
                job.delete()
            except Exception as e:
                print e
                messages.error(request, e)
                return HttpResponse('{"status":"failed"}', content_type='application/json')
        messages.success(request, "delete success!")
    return HttpResponse('{"status":"success"}', content_type='application/json')


def JobEditPage(request):
    context = {}
    if request.method == "POST":
        job_name = request.POST.get('job_name', None)
        try:
            job = Job.objects.get(name=job_name)
        except:
            job = Job.objects.filter(name=job_name)
        context['edit_job'] = job

    return render(request, 'webpage/JobEditPage.html', context=context)


def JobEditSubmit(request):
    context = search_all_jobs()

    if request.method == "POST":
        job_name = request.POST.get('job_name', None)
        ismonitored = request.POST.get('ismonitored', None)
        fetchSizeOfOneTime = request.POST.get('fetchSizeOfOneTime', None)
        url = request.POST.get('url', None)
        job_dir = request.POST.get('job_dir', None)
        trainingFrequency = int(request.POST.get('trainingFrequency', None))
        fetchFrequency = int(request.POST.get('fetchFrequency', None))
        description = request.POST.get('description', None)

        job = Job.objects.get(name=job_name)
        job.ismonitored = True if ismonitored.lower() == 'true' else False
        job.fetchSizeOfOneTime = int(fetchSizeOfOneTime)
        job.url = url
        job.job_dir = job_dir
        job.trainingFrequency = trainingFrequency
        job.fetchFrequency = fetchFrequency
        job.description = description
        try:
            job.save()
        except Exception as e:
            print e
            messages.error(request, e)
            return render(request, 'webpage/JobEditPage.html')

        Fsche.job_scheduler_update(job)
        Tsche.job_scheduler_update(job)

    jobs = Job.objects.all()
    context['jobs'] = jobs

    return render(request, 'webpage/Scheduler.html', context=context)


def schedulerStart(request):
    try:
        Fsche.scheduler_start()
        Tsche.scheduler_start()
    except Exception as e:
        messages.error(request, e)
        return HttpResponse('{"status":"failed"}', content_type='application/json')
    return HttpResponse('{"status":"success"}', content_type='application/json')


def schedulerStop(request):
    try:
        Fsche.scheduler_shutdown(wait=False)
        Tsche.scheduler_shutdown(wait=False)
    except Exception as e:
        messages.error(request, e)
        return HttpResponse('{"status":"failed"}', content_type='application/json')
    return HttpResponse('{"status":"success"}', content_type='application/json')
