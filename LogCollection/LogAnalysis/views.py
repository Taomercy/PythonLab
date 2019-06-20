# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib import messages
import webpage.config as WebConfig
from NaiveBayesModel import *
from DataPrepare import *
from MLPClassifierModel import *
from KMeansModel import *
import threading
from DataPlot import bar_plot_codes_stat
from DataPlot import scores_statistic_plot
# Create your views here.


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


def TrainingLogBySVMAndMLP(request):
    context = get_training_jobs()
    if request.method == "POST":
        training_job = request.POST.get('training_job', "")
        training_path = Job.objects.get(name=training_job).job_dir
        print "training_path:", training_path
        try:
            context.update(training_by_SVM_and_MLP(training_path, job_name=training_job, feature_d=0))
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
    if not os.path.isdir(WebConfig.LOG_PREDICT_PATH):
        os.mkdir(WebConfig.LOG_PREDICT_PATH)
    return render(request, 'LogAnalysis/LogPredictPage.html', context=get_context_of_files(WebConfig.LOG_PREDICT_PATH))


def UploadPredictLog(request):
    class MyThread(threading.Thread):
        def __init__(self, threadID, url):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.url = url

        def run(self):
            # print "Starting thread [%d]" % self.threadID
            print "catching url:", self.url
            job_url = JobUrlModel(self.url)
            job_url.save_console_text(WebConfig.LOG_PREDICT_PATH)

            # print "Exiting thread [%d]" % self.threadID

    if request.method == "POST":
        job_home_url = request.POST.get('job_home_url', None)
        build_num_start = request.POST.get('build_num_start', "")
        build_num_end = request.POST.get('build_num_end', "")
        if build_num_start == "" or build_num_end == "":
            job_url = JobUrlModel(job_home_url)
            job_url.save_console_text(WebConfig.LOG_PREDICT_PATH)
            return render(request, 'LogAnalysis/LogPredictPage.html',
                          context=get_context_of_files(WebConfig.LOG_PREDICT_PATH))

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

    return render(request, 'LogAnalysis/LogPredictPage.html', context=get_context_of_files(WebConfig.LOG_PREDICT_PATH))


def PreditLogDelete(request):
    if request.method == "POST":
        log_name = request.POST.get('predict_log', None)
        os.remove(log_name)
        print "%s has been deleted" % log_name
        messages.success(request, "delete success!")

    return render(request, 'LogAnalysis/LogPredictPage.html', context=get_context_of_files(WebConfig.LOG_PREDICT_PATH))


def PredictByMLP(request):
    context = predict_by_MLP(WebConfig.LOG_PREDICT_PATH)
    return render(request, 'LogAnalysis/LogPredictPage.html', context=context)


def PredictByBayes(request):
    context = predict_by_naive_bayes(WebConfig.LOG_PREDICT_PATH)
    return render(request, 'LogAnalysis/LogPredictPage.html', context=context)


def PlotCodesNumWithStat(request):
    context = get_training_jobs()
    jobs = Job.objects.all()
    figs = []
    for job in jobs:
        fig = bar_plot_codes_stat(job)
        if fig:
            figs.append(fig)
    context['images'] = figs
    return render(request, 'LogAnalysis/LogAnalysisPage.html', context=context)


def ScoresStatisticPage(request):
    context = get_training_jobs()
    models=WebConfig.model_str
    context['models'] = [models]
    return render(request, 'LogAnalysis/LogScheduleAnalysisPage.html', context=context)


def ScoresStatistic(request):
    context = get_training_jobs()
    models = WebConfig.model_str
    context['models'] = [models]
    if request.method == "POST":
        job_name = request.POST.get('training_job')
        model = request.POST.get('model')
        try:
            fig = scores_statistic_plot(job_name, model)
            context['images'] = [fig]
        except Exception as e:
            print "Exception:", e
            messages.error(request, e)
        return render(request, 'LogAnalysis/LogScheduleAnalysisPage.html', context=context)
    return render(request, 'LogAnalysis/LogScheduleAnalysisPage.html', context=context)
