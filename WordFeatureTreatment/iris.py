#!usr/bin/env python
#! -*- coding:utf-8 -*-
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn import metrics

def knn_test():
    iris = datasets.load_iris()
    iris_X = iris.data
    iris_Y = iris.target
    X_train, X_test, y_train, y_test = train_test_split(iris_X, iris_Y, test_size=0.3)
    knn = KNeighborsClassifier()
    knn.fit(X_train, y_train)
    print y_test
    print knn.predict(X_test)
    print metrics.classification_report(y_test, knn.predict(X_test))


def chi_square_test():
    iris = datasets.load_iris()
    iris_X = iris.data
    iris_Y = iris.target
    mode = SelectKBest(chi2, k=2)
    new_iris_X = mode.fit_transform(iris_X, iris_Y)
    print new_iris_X
    print mode.scores_
    print mode.pvalues_
    
#knn_test()
chi_square_test()
