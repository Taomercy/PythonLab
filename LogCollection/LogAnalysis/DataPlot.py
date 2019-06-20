#!/usr/bin/env python
# -*- coding:utf-8 -*-
from DataPrepare import *
from LogAnalysis.models import ScoreStatistic
import platform
sysstr = platform.system()
if sysstr == 'Linux':
    import matplotlib
    matplotlib.use('Agg')
import matplotlib.pyplot as plt
from LogCollection.settings import STATIC_ROOT
from mpl_toolkits.mplot3d import Axes3D


def visual_2D_dataset(dataset_X, dataset_Y, fig_title='The doc2vec labels', fig_name='doc2vec_2d.png'):
    # assert dataset_X.shape[1] == 2, 'only support dataset with 2 features'
    plt.figure()
    classes = list(set(dataset_Y))
    markers = ['.', ',', 'o', 'v', '^', '*', '1', '2', '3', '4', '8', 's', 'p', 'h', 'H', '+', 'x', 'D', 'd']
    colors = ['b', 'c', 'g', 'k', 'm', 'r', 'y']
    for class_id in classes:
        one_class = np.array([feature for (feature, label) in zip(dataset_X, dataset_Y) if label == class_id])
        plt.scatter(one_class[:, 0], one_class[:, 1], marker=np.random.choice(markers, 1)[0],
                    c=np.random.choice(colors, 1)[0], label='class_' + str(class_id), s=15)
    plt.legend()
    plt.title(fig_title)

    plot_path = os.path.join(STATIC_ROOT, 'DataPlot', fig_name)
    plt.savefig(plot_path)
    return fig_name


def plotBestFit(data1, data2):
    fig = plt.figure()
    dataArr1 = np.array(data1)
    dataArr2 = np.array(data2)

    m = np.shape(dataArr1)[0]
    axis_x1 = []
    axis_y1 = []
    axis_x2 = []
    axis_y2 = []
    for i in range(m):
        axis_x1.append(dataArr1[i, 0])
        axis_y1.append(dataArr1[i, 1])
        axis_x2.append(dataArr2[i, 0])
        axis_y2.append(dataArr2[i, 1])
    ax = fig.add_subplot(111)
    ax.scatter(axis_x1, axis_y1, s=15, c='red', marker='*', label='FinalData = (XMat - avgs) * selectVec.T')
    ax.scatter(axis_x2, axis_y2, s=15, c='blue', label='Raw Data = (FinalData * selectVec) + average')
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.title('doc2vec after pca')
    plt.legend()

    fig_name = 'doc2vec_after_pca_plot.png'
    plot_path = os.path.join(STATIC_ROOT, 'DataPlot', fig_name)
    plt.savefig(plot_path)
    print "saving the plot %s" % plot_path
    plt.close()
    return fig_name


def plot_classifier(classifier, dataset_X, dataset_Y):
    from numpy import min, max, meshgrid, arange, c_
    x_min, x_max = min(dataset_X[:, 0]) - 1.0, max(dataset_X[:, 0]) + 1.0
    y_min, y_max = min(dataset_X[:, 1]) - 1.0, max(dataset_X[:, 1]) + 1.0
    step_size = 0.01
    x_values, y_values = meshgrid(arange(x_min, x_max, step_size), arange(y_min, y_max, step_size))
    mesh_output = classifier.predict(c_[x_values.ravel(), y_values.ravel()])
    mesh_output = mesh_output.reshape(x_values.shape)
    plt.figure()
    plt.pcolormesh(x_values, y_values, mesh_output, cmap=plt.cm.gray)
    plt.scatter(dataset_X[:, 0], dataset_X[:, 1], c=dataset_Y, s=80, edgecolors='black', linewidth=1,
                cmap=plt.cm.Paired)
    plt.xlim(x_values.min(), x_values.max())
    plt.ylim(y_values.min(), y_values.max())
    plt.xticks((arange(int(min(dataset_X[:, 0]) - 1), int(max(dataset_X[:, 0]) + 1), 1.0)))
    plt.yticks((arange(int(min(dataset_X[:, 1]) - 1), int(max(dataset_X[:, 1]) + 1), 1.0)))
    fig_name = 'classifier.png'
    plot_path = os.path.join(STATIC_ROOT, 'DataPlot', fig_name)
    plt.savefig(plot_path)
    print "saving the plot %s" % plot_path
    plt.close()
    return fig_name


def scatter_plot3d(dataset, labels, fig_title='The doc2vec 3d', fig_name='doc2vec_3d.svg'):
    def TurnLabels2Int(labels):
        label_set = list(set(labels))
        label_num = range(1, len(label_set)+1)
        result = []
        for i in labels:
            index = label_set.index(i)
            result.append(label_num[index])
        return result

    labels = TurnLabels2Int(labels)
    fig = plt.figure()
    coulorA = 15 * np.array(labels, dtype='int')
    ax = plt.subplot(111, projection='3d')
    ax.scatter(dataset[:, 0], dataset[:, 1], dataset[:, 2], coulorA, coulorA, coulorA)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    fig.suptitle(fig_title)

    plot_path = os.path.join(STATIC_ROOT, 'DataPlot', fig_name)
    fig.savefig(plot_path)

    print "saving the plot %s" % plot_path
    plt.close()
    return fig_name


def bar_plot_codes_stat(job):
    logs = Log.objects.filter(job=job)
    if not logs:
        return None
    stat = [stat.id for stat in ExitStatus.objects.all()]

    fig = plt.figure(figsize=(12, 6))

    stat_n = len(stat)
    total_width = 0.8
    width = total_width / stat_n

    for i in range(stat_n):
        cn_tmp = []
        stat_tmp = []
        for log in logs:
            if log.exit_status.id == stat[i]:
                cn_tmp.append(log.codes_number)
                stat_tmp.append(log.exit_status.name)

        plt.scatter(stat_tmp, cn_tmp)
    plt.xlabel('Exit Status')
    plt.ylabel('Codes Number')

    fig.suptitle(job.name)
    fig_name = "codes_num_with_stat_%s.png" % job.name
    plot_path = os.path.join(STATIC_ROOT, 'DataPlot', "codes_num_with_stat_%s.png" % job.name)
    fig.savefig(plot_path)
    print "saving the plot %s" % plot_path
    plt.close()
    return fig_name


def scores_statistic_plot(job_name, model=None, fig_name=None):
    scores = ScoreStatistic.objects.filter(job__name=job_name)
    if not scores:
        raise Exception("Table ScoreStatistic is empty!")
    if model:
        models = [model]
    else:
        models = list(set([score.model for score in scores]))
    fig = plt.figure(figsize=(11, 6))
    title = "[%s] score statistic" % job_name
    fig.suptitle(title)

    ax1 = fig.add_subplot(2, 1, 1)
    ax1.grid(True)
    ax1.set_ylabel("score")

    ax2 = fig.add_subplot(2, 1, 2)
    ax2.grid(True)
    ax2.set_xlabel("training time")
    ax2.set_ylabel("data counts")

    times_a = None
    data_count = None
    for index in range(len(models)):
        model = models[index]
        JScores = scores.filter(model=model).order_by('-training_time')
        j_scores = np.array([score.score for score in JScores])
        times = np.array([score.training_time for score in JScores])
        times_a = times
        ax1.plot(times, j_scores, linewidth=1, linestyle='-', label=model)

        data_count = [score.dataset_num for score in JScores]
    ax2.plot(times_a, data_count, linewidth=1.5, linestyle='-', color='red', label='data count')

    fig.legend(loc='upper left')

    if not fig_name:
        fig_name = "%s_scores_statistic.png" % job_name
    plot_path = os.path.join(STATIC_ROOT, 'DataPlot', fig_name)
    plt.savefig(plot_path)
    return fig_name

