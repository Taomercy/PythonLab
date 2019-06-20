#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.externals import joblib
import log_filter
from LogAnalysis.DataPrepare import get_all_files_in_the_dir
from webpage.models import *
from webpage.config import *
from DataPlot import plot_classifier
from LogAnalysis.models import *


def trainning_log_data_set(dirname, class_from_database=True):
    logLabels = []
    trainingLogList = get_all_files_in_the_dir(dirname)
    m = len(trainingLogList)
    contexts = []
    for i in range(m):
        logStr = ""
        logNameStr = os.path.basename(trainingLogList[i])
        if class_from_database:
            try:
                logClass = Log.objects.get(name=logNameStr).error_type.name
            except Exception as e:
                print "%s gets error ==> [%s]" % (logNameStr, e)
                os.remove(trainingLogList[i])
                continue

        else:
            logClass = logNameStr.split('.')[0].split('_')[-1]
        logLabels.append(str(logClass))
        logContextFilter = log_filter.get_key_log(trainingLogList[i])
        for line in logContextFilter:
            logStr += line
        contexts.append(str(logStr))
    return contexts, logLabels


def test_log_data_set(dirname):
    testLogList = get_all_files_in_the_dir(dirname)
    m = len(testLogList)
    contexts = []
    logNames = []
    for i in range(m):
        logStr = ""
        logNameStr = os.path.basename(testLogList[i])
        logNames.append(logNameStr)
        logContextFilter = log_filter.get_key_log(testLogList[i])
        for line in logContextFilter:
            try:
                logStr += line
            except:
                continue
        contexts.append(logStr)
    return contexts, logNames


def training_by_naive_bayes(train_dirname, job_name=None, scheduler=False):
    print "[job: %s] training by naive bayes starting" % job_name
    context = {}
    logContexts, logLabels = trainning_log_data_set(train_dirname, class_from_database=True)

    X_train, X_test, y_train, y_test = train_test_split(logContexts, logLabels, test_size=0.30)

    vectorizer = CountVectorizer(binary=True, stop_words='english')
    X_train_counts = vectorizer.fit_transform(X_train)
    joblib.dump(vectorizer, get_vectorizer_model_path(job_name=job_name))

    transformer = TfidfTransformer()
    X_train_tfidf = transformer.fit_transform(X_train_counts)
    joblib.dump(transformer, get_tfidf_model_path(job_name=job_name))

    clf = MultinomialNB().fit(X_train_tfidf, y_train)
    joblib.dump(clf, get_native_bayes_model_path(job_name=job_name))

    X_new_counts = vectorizer.transform(X_test)
    X_new_tfidf = transformer.transform(X_new_counts)

    predicted = clf.predict(X_new_tfidf)
    metrics_report = metrics.classification_report(y_test, predicted)
    metrics_score = metrics.accuracy_score(y_test, predicted)

    ScoreStatistic.objects.create(job=Job.objects.get(name=job_name),
                                  model=model_str['naive'],
                                  dataset_num=len(logLabels),
                                  score=metrics_score)

    if not scheduler:
        print "metrics_score:", metrics_score
        print "metrics_report:", metrics_report
        context['predicted'] = predicted
        context['metrics_score'] = metrics_score
        context['metrics_report'] = metrics_report
        return context

    return 0


def predict_by_naive_bayes(test_dirname, job_name=None):
    class PerdictInfo(object):
        def __init__(self, log, predict_label):
            self.log = log
            self.predict_label = predict_label
    context = {}
    try:
        vectorizer = joblib.load(get_vectorizer_model_path(job_name=job_name))
        transformer = joblib.load(get_tfidf_model_path(job_name=job_name))
        clf = joblib.load(get_native_bayes_model_path(job_name=job_name))
    except Exception as e:
        print e
        print "go to training the model"
        return

    test_log, logNames = test_log_data_set(test_dirname)
    X_new_counts = vectorizer.transform(test_log)
    X_new_tfidf = transformer.transform(X_new_counts)

    predicted = clf.predict(X_new_tfidf)

    print "predict result:"
    for logName, label in zip(logNames, predicted):
        print "%s ==> %s" % (logName, label)

    context['predicted'] = [PerdictInfo(log, p_label) for log, p_label in zip(logNames, predicted)]

    return context
