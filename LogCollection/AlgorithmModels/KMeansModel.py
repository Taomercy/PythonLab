#!/usr/bin/env python
# -*- coding:utf-8 -*-
from numpy import array
from DataProcessingAndPlot.DataPrepare import DocLogs
from sklearn.cluster import KMeans
from sklearn.externals import joblib
from DataProcessingAndPlot.DataPrepare import DataPCA
from DataProcessingAndPlot.DataPlot import visual_2D_dataset
from LogAnalysis.config import *
from DataProcessingAndPlot.DataPlot import scatter_plot3d
from sklearn.cluster import DBSCAN


def training_by_Kmeans(dirname, job_name=None, scheduler=False, n_clusters=3, feature_d=0, dbscan=False, eps=2, min_samples=3):
    class TableInfo(object):
        def __init__(self, log, raw_label, km_label):
            self.log = log
            self.raw_label = raw_label
            self.km_label = km_label
    print "[job: %s] training by KMeans" % job_name
    context = {}
    plot_path_list = []

    doc = DocLogs(dirname)
    vectors_docs, raw_labels = doc.GetDocDataSet()

    finalData2d, rawMat2d = DataPCA(vectors_docs, 2)
    finalData3d, reconMat3d = DataPCA(vectors_docs, 3)

    if feature_d != 0:
        vectors_docs = array(DataPCA(vectors_docs, feature_d)[0], dtype='float')

    if dbscan:
        kmeans = DBSCAN(eps=eps, min_samples=min_samples).fit(vectors_docs)
        print "choose the DBSCAN"
    else:
        kmeans = KMeans(n_clusters=n_clusters, random_state=0, init='k-means++').fit(vectors_docs)
        print "choose the k-means++"
    km_labels = kmeans.labels_
    joblib.dump(kmeans, get_kmeans_model_path(job_name=job_name))

    if not scheduler:
        log_list = [os.path.basename(log) for log in doc.GetLogList()]

        plot_path = visual_2D_dataset(array(finalData2d), array(raw_labels),
                                      fig_title='Raw Data Labels', fig_name='RawData.png')
        plot_path_list.append(plot_path)

        plot_path = visual_2D_dataset(array(finalData2d), km_labels,
                                      fig_title='Kmeans cluster', fig_name='KmeansCluster.png')
        plot_path_list.append(plot_path)

        plot_path = scatter_plot3d(array(finalData3d, dtype='float'), raw_labels,
                                   fig_title='Raw Data Labels', fig_name='RawData3d.png')
        plot_path_list.append(plot_path)

        plot_path = scatter_plot3d(array(finalData3d, dtype='float'), km_labels,
                                   fig_title='Kmeans cluster', fig_name='KmeansCluster3d.png')
        plot_path_list.append(plot_path)

        context['km_result'] = [TableInfo(log, raw_label, km_label) for log, raw_label, km_label
                                in zip(log_list, raw_labels, km_labels)]
        context['label_th'] = ['log', 'raw labels', 'km labels']
        context['images'] = plot_path_list

    return context

