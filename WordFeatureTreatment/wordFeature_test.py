#!/usr/bin/env python
# -*- coding:utf-8 -*-
from numpy import *
from sklearn.feature_extraction.text import CountVectorizer
import sys

def get_readlines(filename):
    context = []
    with open(filename, 'r') as fr:
        context = [line.strip('\n') for line in fr.readlines()]
    return context

filename = sys.argv[1]
import catch
#context = catch.get_key_log(filename)
#print context
context = ["This is an error",
            "Log error",
            "Computer CI",
            ]
from sklearn.feature_extraction.text import TfidfTransformer
vectorizer = CountVectorizer()
transformer = TfidfTransformer()
tfidf = transformer.fit_transform(vectorizer.fit_transform(context))
print vectorizer.vocabulary_
print tfidf
'''
vectorizer = CountVectorizer(binary=True, stop_words='english')
print vectorizer.fit_transform(context).todense()
print vectorizer.get_feature_names()
print vectorizer.vocabulary_
from sklearn.cross_validation import train_test_split
'''
