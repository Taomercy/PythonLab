#!/usr/bin/env python
# -*- coding:utf-8 -*-
from common import *
from sklearn.svm import SVC


def training_by_SVM(dirname, job_name=None, scheduler=False, feature_d=0, data_processing=False):
    print "[job: %s] training by SVM" % job_name
    context = {}

    doc = DocLogs(dirname, processing=data_processing)
    vectors_docs, labels = doc.GetDocDataSet()

    finalData2d, rawMat2d = DataPCA(vectors_docs, 2)

    plot_path_list = []
    if not scheduler:
        plot_path = plotBestFit(finalData2d, rawMat2d)
        plot_path_list.append(plot_path)

        plot_path = visual_2D_dataset(array(finalData2d), array(labels),
                                      fig_title='all train data 2d', fig_name='all_train_data2d.png')
        plot_path_list.append(plot_path)

        finalData3d, rawMat3d = DataPCA(vectors_docs, 3)
        plot_path = scatter_plot3d(array(finalData3d, dtype='float'), labels,
                                   fig_title='all train data 3d', fig_name='all_train_data3d.png')
        plot_path_list.append(plot_path)

    if feature_d != 0:
        vectors_docs = array(DataPCA(vectors_docs, feature_d)[0], dtype='float')

    X_train, X_test, y_train, y_test = train_test_split(vectors_docs, labels, test_size=0.30)

    if not scheduler:
        plot_path = visual_2D_dataset(array(X_test), array(y_test),
                                      fig_title='test data', fig_name='test_data.png')
        plot_path_list.append(plot_path)

    print "[job: %s] training by svm ..." % job_name
    svc = SVC(1.0, kernel='rbf', gamma='auto')

    start_time = time.clock()
    svc.fit(X_train, y_train)
    end_time = time.clock()
    duration = end_time - start_time

    joblib.dump(svc, get_svm_model_path(job_name=job_name))

    svm_predicted = svc.predict(X_test)
    svm_metrics_report = metrics.classification_report(y_test, svm_predicted)
    svm_metrics_score = metrics.accuracy_score(y_test, svm_predicted)

    InitMLModel()
    ScoreStatistic.objects.create(job=Job.objects.get(name=job_name),
                                  model=MLModel.objects.get(name='svm'),
                                  dataset_num=len(labels),
                                  score=svm_metrics_score,
                                  duration=duration)

    if not scheduler:
        plot_path = visual_2D_dataset(array(X_test), array(svm_predicted),
                                      fig_title='svm predict result', fig_name='svm_predict.png')
        plot_path_list.append(plot_path)

    if not scheduler:
        context['svm_predicted'] = svm_predicted
        context['svm_metrics_score'] = svm_metrics_score
        context['svm_metrics_report'] = svm_metrics_report
        context['images'] = plot_path_list
        print "plot_path_list:", plot_path_list
    return context