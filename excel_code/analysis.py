#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import print_function
import os
import platform
import sys

import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
sysstr = platform.system()
if sysstr == 'Linux':
    import matplotlib
    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import xlrd
xl_name = "log_info.xls"
data_sheet_name = "log_info"
label_sheet_name = "log_label"


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

    plot_path = os.path.join(fig_name)
    plt.savefig(plot_path)
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

    plot_path = os.path.join(fig_name)
    fig.savefig(plot_path)
    plt.show()
    plt.close()
    return fig_name


def get_data_set_from_excel():
    wb = xlrd.open_workbook(xl_name)
    dsh = wb.sheet_by_name(data_sheet_name)
    nrows = dsh.nrows
    lsh = wb.sheet_by_name(label_sheet_name)

    x_trains = []
    x_labels = []
    y_tests = []
    y_name = []

    for i in range(1, nrows):
        train_stat = lsh.row_values(i)[2]
        if train_stat == 1:
            label = lsh.row_values(i)[1]
            data = dsh.row_values(i)
            del(data[0])
            x_trains.append(data)
            x_labels.append(label)
        else:
            data = dsh.row_values(i)
            y_name.append(data[0])
            del(data[0])
            y_tests.append(data)
    return x_trains, x_labels, y_tests, y_name


def get_label_set():
    wb = xlrd.open_workbook(xl_name)
    sh = wb.sheet_by_name(label_sheet_name)
    nrows = sh.nrows
    return sh.col_values(1, 1, nrows)


if __name__ == '__main__':
    x_trains, x_labels, y_tests, y_name = get_data_set_from_excel()
    print(x_trains, x_labels, y_tests, y_name)

    mlp = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 5), random_state=1)
    mlp.fit(x_trains, x_labels)

    pre_res = mlp.predict(y_tests)

    print("===============================")
    for f, res in zip(y_name, pre_res):
        print(f, res)

    pca = PCA(n_components=2)
    finalData2d = pca.fit_transform(x_trains)
    visual_2D_dataset(dataset_X=finalData2d, dataset_Y=x_labels, fig_name="res.png")

    pca = PCA(n_components=3)
    finalData3d = pca.fit_transform(x_trains)
    scatter_plot3d(dataset=finalData3d, labels=x_labels, fig_name="ttt.png")



