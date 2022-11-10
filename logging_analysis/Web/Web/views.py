#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import functools
import json
import shutil
import subprocess
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from Web.settings import CASE_STORAGE
from Web.models import *
from Web.utils import *
from login.models import User

login_user = None


def session_timeout(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            user_id = request.session['user_id']
        except KeyError as e:
            print(e)
            return render(request, 'login/login.html')
        return func(request, *args, **kwargs)
    return wrapper


@session_timeout
@require_GET
def results_display(request):
    user_id = request.session['user_id']
    user = User.objects.get(user_id=user_id)
    results = get_results()
    return render(request, 'results_display.html', locals())


@session_timeout
@require_GET
def MHWeb_display(request):
    user_id = request.session['user_id']
    user = User.objects.get(user_id=user_id)
    mhs = MHWeb.objects.all()
    thread = MHWeb.get_thread()
    return render(request, 'MHWeb_display.html', locals())


@require_GET
def property_display(request):
    properties = UnstabilityProperty.objects.all()
    thread = UnstabilityProperty.get_thread()
    return render(request, 'properties_display.html', locals())


@require_http_methods(['POST', 'GET'])
def create_property(request):
    if request.method == 'GET':
        return render(request, 'create_property.html', locals())
    else:
        name = request.POST.get("property_name", None)
        free_memory_delta_rate = request.POST.get("free_memory_delta_rate", None)
        UnstabilityProperty.objects.create(name=name, free_memory_delta_rate=free_memory_delta_rate).save()
        properties = UnstabilityProperty.objects.all()
        thread = UnstabilityProperty.get_thread()
        return render(request, 'properties_display.html', locals())


@require_http_methods(['POST', 'GET'])
def modify_property(request):
    if request.method == 'GET':
        name = request.GET.get("property_name", None)
        property = UnstabilityProperty.objects.get(name=name)
        return render(request, 'modify_property.html', locals())
    else:
        name = request.POST.get("property_name", None)
        free_memory_delta_rate = request.POST.get("free_memory_delta_rate", None)
        property = UnstabilityProperty.objects.get(name=name)
        property.name = name
        property.free_memory_delta_rate = free_memory_delta_rate
        property.save()
        properties = UnstabilityProperty.objects.all()
        thread = UnstabilityProperty.get_thread()
        return render(request, 'properties_display.html', locals())


@require_POST
def delete_property(request):
    name = request.POST.get("property_name", None)
    property = UnstabilityProperty.objects.get(name=name)
    property.delete()

    properties = UnstabilityProperty.objects.all()
    thread = UnstabilityProperty.get_thread()
    return render(request, 'properties_display.html', locals())


@session_timeout
@require_http_methods(['POST', 'GET'])
def time_axis(request):
    user_id = request.session['user_id']
    user = User.objects.get(user_id=user_id)
    if request.method == 'GET':
        case_paths = search_files(CASE_STORAGE, "TC-*.*")
        if case_paths:
            cases = [os.path.basename(p) for p in case_paths]
        return render(request, 'time_axis.html', locals())
    else:
        case_path = request.POST.get("case_tar", None)
        start = request.POST.get('start', None)
        end = request.POST.get('end', None)

        case_path = os.path.join(CASE_STORAGE, case_path)

        if not start or not end:
            start, end, load_time_output = get_load_time(case_path)

        print("start:", start)
        print("end:", end)
        # TODO:get load rate
        loads_data = get_loads(case_path)
        # TODO:get error rate
        error_rate_data = get_error_rate(case_path)
        # TODO:get applog
        # TODO:get alarm
        # print("loads_data:", loads_data)
        # print("error_rate_data:", error_rate_data)
        return render(request, 'time_axis.html', locals())


@session_timeout
@require_GET
def app_log_type_display(request):
    user_id = request.session['user_id']
    user = User.objects.get(user_id=user_id)
    applogs = AppLogType.objects.all()
    thread = AppLogType.get_thread()
    return render(request, 'app_log_type_display.html', locals())


@require_POST
def delete_app_type(request):
    applog_type_name = request.POST.get("applog_type_name", None)
    app_type = AppLogType.objects.get(name=applog_type_name)
    app_type.delete()

    applogs = AppLogType.objects.all()
    thread = AppLogType.get_thread()
    return render(request, 'app_log_type_display.html', locals())


@require_http_methods(['POST', 'GET'])
def create_applog_type(request):
    if request.method == 'GET':
        return render(request, 'create_applog_type.html', locals())
    else:
        applog_type_name = request.POST.get("applog_type_name", None)
        release_version = request.POST.get("release_version", None)
        count = request.POST.get("count", None)
        AppLogType.objects.create(name=applog_type_name, release_version=release_version, count=count)
        applogs = AppLogType.objects.all()
        thread = AppLogType.get_thread()
        return render(request, 'app_log_type_display.html', locals())


@require_http_methods(['POST', 'GET'])
def upload_case(request):
    if request.method == 'GET':
        return render(request, 'upload_case_tar.html', locals())
    else:
        upload_tar = request.FILES.get("upload_case_tar", None)
        if not upload_tar:
            return HttpResponse('no files for upload!')

        case_name = "_".join(upload_tar.split(".")[:-1])
        if case_name in os.listdir(CASE_STORAGE):
            warning = "Upload failed: the file had been uploaded."
        else:
            tar_saving_path = os.path.join(CASE_STORAGE, upload_tar)
            with open(tar_saving_path, 'wb+') as fw:
                for c in upload_tar.chunks():
                    fw.write(c)

            case_saving_path = os.path.join(CASE_STORAGE, case_name)
            un_tar(tar_saving_path, CASE_STORAGE)
            shutil.rmtree(tar_saving_path)
            print("Tar Saving Path:", tar_saving_path)
            info = "Upload success."

    case_paths = search_files(CASE_STORAGE, "TC-*.*")
    if case_paths:
        cases = [os.path.basename(p) for p in case_paths]
    return render(request, 'case_display.html', locals())


@require_http_methods(['POST'])
def download_case(request):
    case_name = request.POST.get("case_name", None)
    case_path = os.path.join(CASE_STORAGE, case_name)
    tar_name = case_path + ".gz"
    cmd = "tar -cf {} {}".format(tar_name, case_path)
    (status, output) = subprocess.getstatusoutput(cmd)
    tar_fw = open(tar_name, 'rb')
    response = FileResponse(tar_fw)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachement;filename="{0}"'.format(case_name)
    return response


@require_POST
def delete_case(request):
    case_name = request.POST.get("case_name", None)
    case_name_path = os.path.join(CASE_STORAGE, case_name)
    shutil.rmtree(case_name_path)
    case_paths = search_files(CASE_STORAGE, "TC-*.*")
    if case_paths:
        cases = [os.path.basename(p) for p in case_paths]
    return render(request, 'case_display.html', locals())


@session_timeout
@require_http_methods(['POST', 'GET'])
def case_display(request):
    user_id = request.session['user_id']
    user = User.objects.get(user_id=user_id)
    for i in search_files(CASE_STORAGE, ".*.gz"):
        os.remove(i)
    case_paths = search_files(CASE_STORAGE, "TC-*.*")
    if case_paths:
        cases = [os.path.basename(p) for p in case_paths]
    return render(request, 'case_display.html', locals())


@session_timeout
@require_http_methods(['POST', 'GET'])
def test_case_check(request):
    user_id = request.session['user_id']
    user = User.objects.get(user_id=user_id)
    if request.method == 'GET':
        case_paths = search_files(CASE_STORAGE, "TC-*.*")
        if case_paths:
            cases = [os.path.basename(p) for p in case_paths]

        properties = UnstabilityProperty.objects.all()
        return render(request, 'test_case_check.html', locals())
    else:
        building = True
        case_path = request.POST.get("case_path", None)
        check_type = request.POST.get('type', None)
        start = request.POST.get('start', None)
        end = request.POST.get('end', None)
        modes = request.POST.getlist('mode', None)
        property_name = request.POST.get('property', None)

        cmd = "hcc -c '{0}_check {1} {2}' --user {3}".format(check_type, case_path, ",".join(modes), user_id)
        (status, output) = subprocess.getstatusoutput(cmd)

        pattern = re.compile(r"[0-9]{14}")
        res = re.findall(pattern, output)
        if res:
            timestamp = res[0]
            response = {"user": user_id, "timestamp": timestamp}
        else:
            response = {"user": user_id, "timestamp": None}

        return HttpResponse(json.dumps(response))


@session_timeout
@require_http_methods(['GET'])
def result_details(request):
    user_id = request.session['user_id']
    user = User.objects.get(user_id=user_id)
    if request.method == 'GET':
        result_user = request.GET.get("user", None)
        timestamp = request.GET.get("timestamp", None)
        result_path = os.path.join(RESULT_DIR, result_user, timestamp)
        display = os.path.join(result_path, ".display")

        properties = read_yaml(os.path.join(display, "properties.yaml"))
        start = properties.get("start")
        end = properties.get("end")

        if properties.get("memory"):
            memory_result = properties["memory"]
            memory_pictures = ["result/{}/{}/.display/free_memory.png".format(result_user, timestamp)]
            memory_th = ["MemFree", "Buffers", "Cached", "Shmem", "SReclaimable", "Free memory"]
            memory_tr = ["Instance", "PRE", "POST", "Delta Rate"]
            memory_data = read_yaml(os.path.join(display, "memory.yaml"))

        if properties.get("applog"):
            applog_result = properties["applog"]
            applog_th = ["Message", "Count"]
            applog_data = read_yaml(os.path.join(display, "applog.yaml"))
            applog_log = read_log(os.path.join(result_path, "applog.log"))

        if properties.get("ca"):
            ca_result = properties["ca"]
            ca_log = read_log(os.path.join(result_path, "ca.log"))

        if properties.get("extdb"):
            extdb_result = properties["extdb"]
            extdb_log = read_log(os.path.join(result_path, "extdb.log"))

        if properties.get("fmalarm"):
            fmalarm_result = properties["fmalarm"]
            fmalarm_log = read_log(os.path.join(result_path, "alarm.log"))

        if properties.get("health"):
            health_result = properties["health"]
            health_log = read_log(os.path.join(result_path, "health.log"))

        if properties.get("process"):
            process_result = properties["process"]
            process_data = read_yaml(os.path.join(display, "process.yaml"))
            process_tolerance = properties.get("process_difference_tolerance", 0)
            process_negative_tolerance = -process_tolerance
            if process_data:
                process_datatable = []
                process_th = ["Process Name", "Process Id", "Post", "Pre", "Deviation"]
                for key in (process_data.get("pre").keys() | process_data.get("post").keys()):
                    item = key.split(":")
                    pre_resource = process_data.get("pre").get(key)
                    post_resource = process_data.get("post").get(key)
                    if pre_resource and post_resource:
                        deviation = pre_resource - post_resource
                    else:
                        deviation = None
                    data = {"process_name": item[0], "process_id": item[1],
                            "post": post_resource, "pre": pre_resource, "deviation": deviation}
                    process_datatable.append(data)
            else:
                process_log = read_log(os.path.join(result_path, "process.log"))

        if properties.get("traffic"):
            load_result = properties["traffic"]
            load_data = read_yaml(os.path.join(display, "load.yaml"))
            loads = load_data.get("data")
            load_log = read_log(os.path.join(result_path, "traffic_load.log"))

        if properties.get("http_connection"):
            http_connection_result = properties["http_connection"]
            http_connection_log = read_log(os.path.join(result_path, "httpConnections.log"))

        if properties.get("traffic_error"):
            traffic_error_result = properties["traffic_error"]
            traffic_error_log = read_log(os.path.join(result_path, "traffic_error.log"))

        return render(request, "result_details.html", locals())


@session_timeout
@require_http_methods(['POST'])
def delete_result(request):
    result_path = request.POST.get("result_path", None)
    try:
        shutil.rmtree(result_path)
        response = {"return": "success"}
    except Exception as e:
        print(e)
        response = {"return": "failed"}
    return HttpResponse(json.dumps(response))


def check_app_log(request):
    return render(request, 'app_log.html', locals())


@session_timeout
@require_http_methods(['GET'])
def dashboard(request):
    user_id = request.session['user_id']
    user = User.objects.get(user_id=user_id)
    days = int(request.GET.get("days", 365))
    x_data, record_data = get_records(days)
    total = get_total_records(days)
    users_count = get_records_by_user(days)
    types_count = get_records_by_type(days)
    return render(request, "dashboard.html", locals())

