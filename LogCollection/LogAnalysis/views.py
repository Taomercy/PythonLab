# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from os import listdir
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn import metrics
import log_filter
from webpage.models import *
# Create your views here.


def trainning_log_data_set(dirname, class_from_database=True):
    logLabels = []
    trainingLogList = listdir(dirname)
    m = len(trainingLogList)
    contexts = []
    for i in range(m):
        logStr = ""
        logNameStr = trainingLogList[i]
        if class_from_database:
            logClass = LogFile.objects.get(log_name=logNameStr).error_type.error_type
        else:
            logClass = logNameStr.split('.')[0].split('_')[-1]
        logLabels.append(logClass)
        logContextFilter = log_filter.get_key_log(os.path.join(dirname, logNameStr))
        for line in logContextFilter:
            logStr += line
        contexts.append(logStr)
    return contexts, logLabels


def test_log_data_set(dirname):
    testLogList = listdir(dirname)
    m = len(testLogList)
    contexts = []
    logNames = []
    for i in range(m):
        logStr = ""
        logNameStr = testLogList[i]
        logNames.append(logNameStr)
        logContextFilter = log_filter.get_key_log(os.path.join(dirname, logNameStr))
        for line in logContextFilter:
            logStr += line
        contexts.append(logStr)
    return contexts, logNames


def training_by_naive_bayes(train_dirname):
    print "training by naive bayes starting"
    context = {}
    logContexts, logLabels = trainning_log_data_set(train_dirname, class_from_database=False)

    X_train, X_test, y_train, y_test = train_test_split(logContexts, logLabels, test_size=0.30)

    vectorizer = CountVectorizer(binary=True, stop_words='english')
    X_train_counts = vectorizer.fit_transform(X_train)

    transformer = TfidfTransformer()
    X_train_tfidf = transformer.fit_transform(X_train_counts)

    clf = MultinomialNB().fit(X_train_tfidf, y_train)

    X_new_counts = vectorizer.transform(X_test)
    X_new_tfidf = transformer.transform(X_new_counts)

    predicted = clf.predict(X_new_tfidf)
    metrics_report = metrics.classification_report(y_test, predicted)
    metrics_score = metrics.accuracy_score(y_test, predicted)
    context['predicted'] = predicted
    context['metrics_score'] = metrics_score
    context['metrics_report'] = metrics_report
    return context


def predict_by_naive_bayes(train_dirname, test_dirname):
    logContexts, logLabels = trainning_log_data_set(train_dirname, class_from_database=True)

    vectorizer = CountVectorizer(binary=True, stop_words='english')
    X_train_counts = vectorizer.fit_transform(logContexts)

    transformer = TfidfTransformer()
    X_train_tfidf = transformer.fit_transform(X_train_counts)

    clf = MultinomialNB().fit(X_train_tfidf, logLabels)

    test_log, logNames = test_log_data_set(test_dirname)
    X_new_counts = vectorizer.transform(test_log)
    X_new_tfidf = transformer.transform(X_new_counts)

    predicted = clf.predict(X_new_tfidf)

    for logName, label in zip(logNames, predicted):
        print "%s ==> %s" % (logName, label)

    return predicted


def LogAnalysisPage(request):
    return render(request, 'LogAnalysis/LogAnalysisPage.html')


def TrainingLogByNaiveBayes(request):
    if request.method == "POST":
        training_dir = request.POST.get('training_dir', "")
        context = training_by_naive_bayes(training_dir)
    return render(request, 'LogAnalysis/LogAnalysisPage.html', context=context)

