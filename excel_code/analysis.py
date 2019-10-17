#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import platform

import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
sysstr = platform.system()
if sysstr == 'Linux':
    import matplotlib
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

train_dir = "C:\\Users\\ZIWWUEX\\Desktop\\code\\log_train"
pre_dir = "C:\\Users\\ZIWWUEX\\Desktop\\code\\log_predict"


def get_data(filename):
    statistic = {}
    with open(filename) as fr:
        context = fr.readlines()

    for line in context:
        if "---" in line:
            error, num = line.strip().split(" --- ")
            statistic[error] = int(num)
    return statistic


def get_dataset(d_name):
    dset = []
    files = os.listdir(d_name)
    for f in files:
        data = get_data(os.path.join(d_name, f))
        dset.append(data.values())
    return np.array(dset)


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


import xlrd
xl_name = "log_info.xls"
data_sheet_name = "log_info"
label_sheet_name = "log_label"


def get_data_set():
    wb = xlrd.open_workbook(xl_name)
    sh = wb.sheet_by_name(data_sheet_name)
    nrows = sh.nrows

    dataset = []
    for i in range(1, nrows):
        data = sh.row_values(i)
        del(data[0])
        dataset.append(data)
    return dataset


def get_label_set():
    wb = xlrd.open_workbook(xl_name)
    sh = wb.sheet_by_name(label_sheet_name)
    nrows = sh.nrows
    return sh.col_values(1, 1, nrows)


train_X = get_data_set()
labels = get_label_set()

mlp = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 5), random_state=1)
mlp.fit(train_X, labels)

pre_X = get_dataset(pre_dir)

print(mlp.predict(pre_X))

# pca = PCA(n_components=2)
# finalData2d = pca.fit_transform(train_X)
# visual_2D_dataset(dataset_X=finalData2d, dataset_Y=labels, fig_name="tt.png")
#
# pca = PCA(n_components=3)
# finalData3d = pca.fit_transform(train_X)
# scatter_plot3d(dataset=finalData3d, labels=labels, fig_name="ttt.png")

