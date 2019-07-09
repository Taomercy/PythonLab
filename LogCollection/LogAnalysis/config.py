#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import time

MODEL_SAVE_PATH = "ModelSave"
if not os.path.exists(MODEL_SAVE_PATH):
    os.mkdir(MODEL_SAVE_PATH)

LOG_PREDICT_PATH = "PredictLog"
if not os.path.exists(LOG_PREDICT_PATH):
    os.mkdir(LOG_PREDICT_PATH)


model_str = {
    "naive": "naive bayes",
    "mlp": "mlp",
    "svm": "svm",
    "km++": "K-means++",
    "DBSCAN": "K-means-DBSCAN",
}


def get_model_path(name, job_name):
    if job_name:
        pkg_name = job_name + '_' + name
        path = os.path.join(MODEL_SAVE_PATH, pkg_name)
    else:
        path = os.path.join(MODEL_SAVE_PATH, name)
    return path


def get_native_bayes_model_path(job_name=None):
    pkg_name = "naive_bayes.pkl"
    return get_model_path(pkg_name, job_name)


def get_vectorizer_model_path(job_name=None):
    pkg_name = "vectorizer_model.m"
    return get_model_path(pkg_name, job_name)


def get_tfidf_model_path(job_name=None):
    pkg_name = "tfidf_model.m"
    return get_model_path(pkg_name, job_name)


def get_mlp_model_path(job_name=None):
    pkg_name = "mlp.pkl"
    return get_model_path(pkg_name, job_name)


def get_svm_model_path(job_name=None):
    pkg_name = "svm.pkl"
    return get_model_path(pkg_name, job_name)


def get_kmeans_model_path(job_name=None):
    pkg_name = "kmeans.pkl"
    return get_model_path(pkg_name, job_name)


