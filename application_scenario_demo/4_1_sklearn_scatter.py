#!usr/bin/env python
# ! -*- coding:utf-8 -*-
from numpy import *
import matplotlib.pyplot as plt
from sklearn.naive_bayes import GaussianNB


def dataset_from_csv(filename):
    data = loadtxt(filename, delimiter=',')
    dataset = delete(data, -1, 1)
    labels = data[:, -1]
    return dataset, labels


def visual_2D_dataset(dataset_X, dataset_Y):
    assert dataset_X.shape[1] == 2, 'only support dataset with 2 features'
    plt.figure()
    classes = list(set(dataset_Y))
    markers = ['.', ',', 'o', 'v', '^', '*', '1', '2', '3', '4', '8', 's', 'p', 'h', 'H', '+', 'x', 'D', 'd']
    colors = ['b', 'c', 'g', 'k', 'm', 'r', 'y']
    for class_id in classes:
        one_class = array([feature for (feature, label) in zip(dataset_X, dataset_Y) if label == class_id])
        plt.scatter(one_class[:, 0], one_class[:, 1], marker=random.choice(markers, 1)[0],
                    c=random.choice(colors, 1)[0], label='class_' + str(class_id))
    plt.legend()
    plt.show()


def plot_classifier(classifier, dataset_X, dataset_Y):
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
    plt.show()


def test():
    # dataset_X = array([[1,2],[4,5],[2,6], [3,5], [5,7],[0.5, 2.5], [2, 2.3], [8, 5], [5,5], [6,4], [5, 2.2], [4.1, 1.5]])
    # dataset_Y = array([1,2,3,2,3,1,2,3,4,4,5,5])
    dataset_X, dataset_Y = dataset_from_csv('data.csv')
    visual_2D_dataset(dataset_X, dataset_Y)
    gaussianNB = GaussianNB()
    gaussianNB.fit(dataset_X, dataset_Y)
    dataset_predict_y = gaussianNB.predict(dataset_X)
    correct_predicts = (dataset_predict_y == dataset_Y).sum()
    accuracy = 100 * correct_predicts / dataset_Y.shape[0]
    print("correct prediction num:", correct_predicts)
    print("accuracy:", accuracy)
    plot_classifier(gaussianNB, dataset_X, dataset_Y)


test()
