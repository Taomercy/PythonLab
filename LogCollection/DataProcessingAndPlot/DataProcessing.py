#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import division
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from Untils.OsUntils import *
from Untils.LogFilter import *
import numpy as np


class DocLogs(object):
    def __init__(self, dirname, processing=True):
        self.dirname = dirname
        self.trainingLogList = get_all_files_in_the_dir(self.dirname)
        self.LogLables = []
        self.model = Doc2Vec()
        self.processing = processing

    def __iter__(self):
        TaggededDocument = TaggedDocument
        trainingLogList = self.trainingLogList
        m = len(trainingLogList)
        for i in range(m):
            logNameStr = trainingLogList[i]
            logStr = self.GetWordList(logNameStr, processing=self.processing)
            document = TaggededDocument(logStr, tags=[i])
            yield document

    def GetWordList(self, filename, processing=True):
        context = []
        if processing:
            lines = get_filter_log(filename).split('\n')
        else:
            lines = get_readlines_log(filename)
        for line in lines:
            lin = line.split(' ')
            lin = [li.strip() for li in lin]
            context.extend(lin)
        return context

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

        logs = DocLogs(self.dirname, processing=self.processing)
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
