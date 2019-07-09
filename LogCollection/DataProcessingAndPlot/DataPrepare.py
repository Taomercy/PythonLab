#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import division
from LogAnalysis.models import *
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import numpy as np


def get_all_files_in_the_dir(dirname):
    files = []
    for parent, dirnames, filenames in os.walk(dirname):
        for filename in filenames:
            files.append(str(os.path.join(parent, filename)))
    return files


def get_all_dirs_in_the_dir(dirname):
    dirs = []
    for parent, dirnames, filenames in os.walk(dirname):
        for dirname in dirnames:
            absdirname = str(os.path.join(parent, dirname))
            try:
                if os.listdir(absdirname):
                    dirs.append(absdirname)
                else:
                    os.rmdir(absdirname)
            except Exception as e:
                print e
                continue
    return dirs


def get_context_of_files(dirname):
    context = {}
    files = get_all_files_in_the_dir(dirname)
    context['files'] = files
    return context


def get_training_jobs():
    context = {}
    context['training_jobs'] = Job.objects.all()
    return context


def get_ml_models():
    context = {}
    context['ml_models'] = MLModel.objects.all()
    return context


def get_plotColor():
    context = {}
    context['plotColor'] = PlotColor.objects.all()
    return context


def get_plotLineStyle():
    context = {}
    context['plotLineStyle'] = PlotLineStyle.objects.all()
    return context


def get_plotMarker():
    context = {}
    context['plotMarker'] = PlotMarker.objects.all()
    return context


class DocLogs(object):
    def __init__(self, dirname):
        self.dirname = dirname
        self.trainingLogList = get_all_files_in_the_dir(self.dirname)
        self.LogLables = []
        self.model = Doc2Vec()

    def __iter__(self, class_from_database=True):
        TaggededDocument = TaggedDocument
        trainingLogList = self.trainingLogList
        m = len(trainingLogList)
        for i in range(m):
            logStr = []
            logNameStr = trainingLogList[i]
            with open(logNameStr, 'r') as cf:
                lines = cf.readlines()
            for line in lines:
                lin = line.split(' ')
                lin = [li.strip() for li in lin]
                logStr.extend(lin)
            document = TaggededDocument(logStr, tags=[i])
            yield document

    def GetDocDataSet(self, doc_size=1000):
        trainingLogList = self.trainingLogList
        logLabels = []
        m = len(trainingLogList)
        for i in range(m):
            logNameStr = os.path.basename(trainingLogList[i])
            try:
                logClass = Log.objects.get(name=logNameStr).error_type.name
                logLabels.append(str(logClass))
            except:
                continue

        logs = DocLogs(self.dirname)
        model = Doc2Vec(logs, dm=1, vector_size=doc_size, workers=4, sample=1e-5)
        model.train(logs, total_examples=model.corpus_count, epochs=model.iter)
        self.model = model
        vectors_docs = model.docvecs.vectors_docs
        return vectors_docs, logLabels

    def GetLogList(self):
        return self.trainingLogList

    def GetDocModel(self):
        return self.model


def DataPCA(XMat, k, debug=False):
    def meanX(dataX):
        return np.mean(dataX, axis=0)

    if debug:
        print "Data Pca processing ================="
        print "average = np.mean(dataX, axis=0)"
    average = meanX(XMat)

    m, n = np.shape(XMat)
    avgs = np.tile(average, (m, 1))
    data_adjust = XMat - avgs
    covX = np.cov(data_adjust.T)
    featValue, featVec = np.linalg.eig(covX)
    index = np.argsort(-featValue)
    if debug:
        print "Xmat shape = [m = %d, n = %d]" % (m, n)
        print "avgs = np.tile(average, (m, 1))"
        print "avgs = ", avgs
        print "avgs.shape = ", avgs.shape
        print "data_adjust = XMat - avgs"
        print "data_adjust = ", data_adjust
        print "data_adjust.shape = ", data_adjust.shape
        print "covX = np.cov(data_adjust.T)"
        print "covX = ", covX
        print "covX.shape = ", covX.shape
        print "featValue, featVec = np.linalg.eig(covX)"
        print "featValue = ", featValue
        print "featVec = ", featVec
        print "index = np.argsort(-featValue)"
    if k > n:
        print "k must lower than feature number"
        return
    else:
        selectVec = np.matrix(featVec.T[index[:k]])
        finalData = data_adjust * selectVec.T
        rawData = (finalData * selectVec) + average
        if debug:
            print "selectVec = np.matrix(featVec.T[index[:k]])"
            print "selectVec = ", selectVec
            print "selectVec.shape = ", selectVec.shape
            print "finalData = data_adjust * selectVec.T"
            print "finalData.shape = ", finalData.shape
            print "rawData = (finalData * selectVec) + average"
            print "rawData.shape = ", rawData.shape

    if debug:
        print "Data Pca end ================="
    return finalData, rawData
