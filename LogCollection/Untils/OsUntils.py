#!/usr/bin/env python
# -*- coding:utf-8 -*-
from LogAnalysis.models import *


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