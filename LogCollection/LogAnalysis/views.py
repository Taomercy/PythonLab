# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
import json
import threading
from AlgorithmModels.NaiveBayesModel import *
from AlgorithmModels.MLPModel import *
from AlgorithmModels.KMeansModel import *
from AlgorithmModels.SVMModel import *
from DataProcessingAndPlot.DataProcessing import *
from DataProcessingAndPlot.DataPlot import timestamp_duration_plot
from DataProcessingAndPlot.DataPlot import scores_statistic_plot
from Untils.TimeUtils import *

# Create your views here.
global plot_job
global plot_model


def DBInit(request):
    try:
        InitMLModel()
    except Exception as e:
        messages.error(request, e)
        return HttpResponse('{"failed":"success"}', content_type='application/json')
    return HttpResponse('{"status":"success"}', content_type='application/json')


def LogAnalysisPage(request):
    context = get_training_jobs()
    return render(request, 'LogAnalysis/LogAnalysisPage.html', context=context)


def TrainingLogByNaiveBayes(request):
    context = get_training_jobs()
    if request.method == "POST":
        training_job = request.POST.get('training_job', "")
        training_path = Job.objects.get(name=training_job).job_dir
        print "training_path:", training_path
        try:
            context.update(training_by_naive_bayes(training_path, job_name=training_job))
        except Exception as e:
            print e
            messages.error(request, e)
        return render(request, 'LogAnalysis/LogAnalysisPage.html', context=context)
    else:
        messages.info(request, "analysis error")
        return render(request, 'LogAnalysis/LogAnalysisPage.html', context=context)


def TrainingLogByMLP(request):
    context = get_training_jobs()
    if request.method == "POST":
        training_job = request.POST.get('training_job', "")
        training_path = Job.objects.get(name=training_job).job_dir
        print "training_path:", training_path
        try:
            context.update(training_by_MLP(training_path, job_name=training_job, feature_d=0))
        except Exception as e:
            print e
            messages.error(request, e)
        return render(request, 'LogAnalysis/LogAnalysisPage.html', context=context)
    else:
        messages.info(request, "analysis error")
        return render(request, 'LogAnalysis/LogAnalysisPage.html', context=context)


def TrainingLogBySVM(request):
    context = get_training_jobs()
    if request.method == "POST":
        training_job = request.POST.get('training_job', "")
        training_path = Job.objects.get(name=training_job).job_dir
        print "training_path:", training_path
        try:
            context.update(training_by_SVM(training_path, job_name=training_job, feature_d=0))
        except Exception as e:
            print e
            messages.error(request, e)
        return render(request, 'LogAnalysis/LogAnalysisPage.html', context=context)
    else:
        messages.info(request, "analysis error")
        return render(request, 'LogAnalysis/LogAnalysisPage.html', context=context)


def TrainingLogByKMeans(request):
    context = get_training_jobs()
    if request.method == "POST":
        training_job = request.POST.get('training_job', "")
        submodel = request.POST.get('submodel', "")
        eps = int(request.POST.get('eps', 2))
        min_samples = int(request.POST.get('min_samples', 2))
        cluster_k = int(request.POST.get('cluster_k', 3))
        feature_d = request.POST.get('feature_d', 'all')
        dbscan = False
        if submodel == 'dbscan':
            dbscan = True
        if feature_d == 'all':
            feature_d = 0
        else:
            feature_d = int(feature_d)

        training_path = Job.objects.get(name=training_job).job_dir
        print "training_path:", training_path
        try:
            context.update(training_by_Kmeans(training_path, job_name=training_job, n_clusters=cluster_k,
                                              feature_d=feature_d, dbscan=dbscan, eps=eps, min_samples=min_samples))
        except Exception as e:
            print e
            messages.error(request, e)
        return render(request, 'LogAnalysis/LogAnalysisPage.html', context=context)
    else:
        messages.info(request, "analysis error")
        return render(request, 'LogAnalysis/LogAnalysisPage.html', context=context)


def LogPredictPage(request):
    if not os.path.isdir(LOG_PREDICT_PATH):
        os.mkdir(LOG_PREDICT_PATH)
    return render(request, 'LogAnalysis/LogPredictPage.html', context=get_context_of_files(LOG_PREDICT_PATH))


def UploadPredictLog(request):
    class MyThread(threading.Thread):
        def __init__(self, threadID, url):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.url = url

        def run(self):
            # print "Starting thread [%d]" % self.threadID
            print "catching url:", self.url
            build = JobBuild(self.url)
            build.save_console_text(LOG_PREDICT_PATH)

            # print "Exiting thread [%d]" % self.threadID

    if request.method == "POST":
        job_home_url = request.POST.get('job_home_url', None)
        build_num_start = request.POST.get('build_num_start', "")
        build_num_end = request.POST.get('build_num_end', "")
        if build_num_start == "" or build_num_end == "":
            build = JobBuild(job_home_url)
            build.save_console_text(LOG_PREDICT_PATH)
            return render(request, 'LogAnalysis/LogPredictPage.html',
                          context=get_context_of_files(LOG_PREDICT_PATH))

        build_num_vector = [num for num in range(int(build_num_start), int(build_num_end))]
        url_list = [job_home_url+str(build_num)+"/console" for build_num in build_num_vector]

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

    return render(request, 'LogAnalysis/LogPredictPage.html', context=get_context_of_files(LOG_PREDICT_PATH))


def PreditLogDelete(request):
    if request.method == "POST":
        log_name = request.POST.get('predict_log', None)
        os.remove(log_name)
        print "%s has been deleted" % log_name
        messages.success(request, "delete success!")

    return render(request, 'LogAnalysis/LogPredictPage.html', context=get_context_of_files(LOG_PREDICT_PATH))


def PredictByMLP(request):
    context = predict_by_MLP(LOG_PREDICT_PATH)
    return render(request, 'LogAnalysis/LogPredictPage.html', context=context)


def PredictByBayes(request):
    context = predict_by_naive_bayes(LOG_PREDICT_PATH)
    return render(request, 'LogAnalysis/LogPredictPage.html', context=context)


def BuildingStatisticPage(request):
    context = get_training_jobs()
    return render(request, 'LogAnalysis/BuildingStatisticPage.html', context=context)


def BuildingStatisticSubmit(request):
    context = get_training_jobs()
    global plot_job
    time_start = None

    if request.method == "POST":
        plot_job = request.POST.get('training_job', None)
        time_start = get_timestampdelta("OneMonth")

    if request.method == "GET":
        time = request.GET.get("time")
        time_start = get_timestampdelta(time)

    job = Job.objects.get(name=plot_job)
    try:
        fig = timestamp_duration_plot(job, time_start=time_start)
        context['images'] = [fig]
    except Exception as e:
        print "Exception:", e
        messages.error(request, e)
    return render(request, 'LogAnalysis/BuildingStatisticPage.html', context=context)


def ScoresStatisticPage(request):
    context = get_training_jobs()
    models = model_str
    context['models'] = [models]
    return render(request, 'LogAnalysis/ScoresStatisticPage.html', context=context)


def ScoresStatisticSubmit(request):
    context = get_training_jobs()
    models = model_str
    context['models'] = [models]
    global plot_job
    global plot_model
    time_start = None

    if request.method == "POST":
        plot_job = request.POST.get('training_job')
        plot_model = request.POST.get('model')
        time_start = get_timedelta("OneMonth")

    if request.method == "GET":
        time = request.GET.get("time")
        time_start = get_timedelta(time)

    try:
        fig = scores_statistic_plot(plot_job, time_start=time_start, model=plot_model)
        context['images'] = [fig]
    except Exception as e:
        print "Exception:", e
        messages.error(request, e)
    return render(request, 'LogAnalysis/ScoresStatisticPage.html', context=context)


def MLModelsPage(request):
    return render(request, 'LogAnalysis/MLModels.html')


def ModelList(request):
    def tableData(request, dataList):
        if request.method == "POST":
            print(request.POST)
            limit = request.POST.get('limit')  # how many items per page
            offset = request.POST.get('offset')  # how many items in total in the DB

            if dataList:
                response_data = {'total': dataList.count(), 'rows': []}
                if not offset:
                    offset = 0
                if not limit:
                    limit = 10
                page = int(int(offset) / int(limit) + 1)
                pageinator = Paginator(dataList, limit)  # 开始做分页
                data = pageinator.page(page)

                for model in data:
                    response_data['rows'].append({
                        "Name": model.name,
                        "Color": str(model.plot_color),
                        "LineStyle": str(model.line_style),
                        "Marker": str(model.marker),
                    })
                return HttpResponse(json.dumps(response_data))  # 需要json处理下数据格式
            else:
                return HttpResponse(json.dumps({'total': 0, 'rows': []}))
    models = []
    if request.method == "POST":
        models = MLModel.objects.all()
    return tableData(request, models)


def AddModelPage(request):
    context = get_plotColor()
    context.update(get_plotLineStyle())
    context.update(get_plotMarker())
    context.update(get_ml_models())
    return render(request, 'LogAnalysis/AddModelPage.html', context=context)


def AddModel(request):
    context = get_plotColor()
    context.update(get_plotLineStyle())
    context.update(get_plotMarker())
    context.update(get_ml_models())
    if request.method == 'POST':
        name = request.POST.get('name')
        model = MLModel.objects.filter(name=name)
        if model:
            messages.error(request, "The model is exist!")
            return render(request, 'LogAnalysis/AddModelPage.html', context=context)

        color_id = request.POST.get('color')
        lineStyle_id = request.POST.get('lineStyle')
        marker_id = request.POST.get('marker')

        param = {}
        if color_id:
            param['plot_color_id'] = int(color_id)
        if lineStyle_id:
            param['line_style_id'] = int(lineStyle_id)
        if marker_id:
            param['marker_id'] = int(marker_id)
        MLModel.objects.create(name=name, **param).save()
    return render(request, 'LogAnalysis/MLModels.html')


def DeleteModel(request):
    if request.method == "POST":
        model_name = request.POST.get('model_name', None)
        try:
            model = MLModel.objects.get(name=model_name)
            model.delete()
        except Exception as e:
            print e
            messages.error(request, e)
            return render(request, 'LogAnalysis/MLModels.html')
        messages.success(request, "delete success!")
    return render(request, 'LogAnalysis/MLModels.html')
