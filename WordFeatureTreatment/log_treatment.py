#!usr/bin/env python
#! -*- coding:utf-8 -*-
from os import listdir
from numpy import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import log_filter

def trainning_log_data_set(dirname):
    logLabels = []
    trainingLogList = listdir(dirname)
    m = len(trainingLogList)
    contexts = []
    for i in range(m):
        logStr = ""
        logNameStr = trainingLogList[i]
        logClass = logNameStr.split('_')[0]
        logLabels.append(logClass)
        logContextFilter = log_filter.get_key_log(dirname + '/' + logNameStr)
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
        logContextFilter = log_filter.get_key_log(dirname + '/' + logNameStr)
        for line in logContextFilter:
            logStr += line
        contexts.append(logStr)
    return contexts, logNames

def cross_validation():
    logContexts, logLabels = trainning_log_data_set('trainLog')
    X_train, X_test, y_train, y_test = train_test_split(logContexts, logLabels, test_size=0.30)

    vectorizer = CountVectorizer(binary=True, stop_words='english')
    X_train_counts = vectorizer.fit_transform(X_train)

    transformer = TfidfTransformer()
    X_train_tfidf = transformer.fit_transform(X_train_counts)
    
    clf = MultinomialNB().fit(X_train_tfidf, y_train)

    X_new_counts = vectorizer.transform(X_test)
    X_new_tfidf = transformer.transform(X_new_counts)

    predicted = clf.predict(X_new_tfidf)
    print predicted
    res = metrics.classification_report(y_test, predicted)
    print res
    return res

def main():
    logContexts, logLabels = trainning_log_data_set('trainLog')

    vectorizer = CountVectorizer(binary=True, stop_words='english')
    X_train_counts = vectorizer.fit_transform(logContexts)

    transformer = TfidfTransformer()
    X_train_tfidf = transformer.fit_transform(X_train_counts)
    
    clf = MultinomialNB().fit(X_train_tfidf, logLabels)
    
    test_log, logNames = test_log_data_set('testLog')
    X_new_counts = vectorizer.transform(test_log)
    X_new_tfidf = transformer.transform(X_new_counts)

    predicted = clf.predict(X_new_tfidf)

    for logName, label in zip(logNames, predicted):
        print "%s ==> %s" % (logName, label)




if __name__ == '__main__':
    #main()
    cross_validation()
