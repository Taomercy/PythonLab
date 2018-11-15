#!/usr/bin/python
#!-*- coding:utf-8 -*-
#计算通过身高、声音和头发判断性别的最优分类决策
#为了计算精确除法
from __future__ import division
from math import log
import operator
import sys
try:
    debug_flag = sys.argv[1]
except:
    debug_flag = 'off'
#print 'debug flag:',debug_flag

def debug_func(tag, data=None):
	if debug_flag == 'on':
		if data != None:
			print '{0}'.format(tag), data
		else:
			print '{0}'.format(tag)

#使字典显示中文
def json_print(data):
	import json
	return json.dumps(data, encoding='UTF-8', ensure_ascii=False)

#创造数据应例
def create_dataset():
	dataset = [['高', '长', '粗', '男'],
				['高', '短', '粗', '男'],
				['矮', '短', '粗', '男'],
				['高', '长', '细', '女'],
				['矮', '短', '细', '女'],
				['高', '短', '粗', '女'],
				['矮', '长', '粗', '女'],
				['矮', '长', '粗', '女']]
	labels = ['身高', '头发', '声音']  #特征
	return dataset, labels
def create_dataset1():
	dataset = [['长', '粗', '男'],
				['短', '粗', '男'],
				['短', '粗', '男'],
				['长', '细', '女'],
				['短', '细', '女'],
				['短', '粗', '女'],
				['长', '粗', '女'],
				['长', '粗', '女']]
	labels = ['头发', '声音']  #特征
	return dataset, labels

#按特征分类数据
def feature_class_dataset(dataset, axis, value):
	resultDataSet = []
	for featureVec in dataset:
		if featureVec[axis] == value:
			reducedFeatureVec = featureVec[:axis]
			reducedFeatureVec.extend(featureVec[axis+1:])
			resultDataSet.append(reducedFeatureVec)
	return resultDataSet

#计算数据的熵
def calculate_entropy(dataset):
	numEntries = len(dataset)
	debug_func('数据总数：', numEntries)
	labelCounts = {}
	for featureVec in dataset:
		currentLabel = featureVec[-1]
		if currentLabel not in labelCounts.keys():
			labelCounts[currentLabel] = 0
		#统计类与类的数量
		labelCounts[currentLabel] += 1
	debug_func('统计情况:', json_print(labelCounts))
	entropy = 0
	for key in labelCounts:
		#计算单个类的熵值
		prob = float(labelCounts[key]/numEntries)
		tag = '{0}[熵]:'.format(key)
		debug_func(tag, prob)
		#累计总熵值
		entropy -= prob*log(prob, 2)
	debug_func('>>>>>>>>>>>>')
	return entropy

#选择最优分类特征
def choose_best_feature(dataset):
	#统计特征数
	numFeatures = len(dataset[0])-1
	debug_func('统特征总数:', numFeatures)
	#计算原始熵
	baseEntropy = calculate_entropy(dataset)
	bestInfoGain = 0
	bestFeature = -1
	for i in range(numFeatures):
		featList = [example[i] for example in dataset]
		debug_func('特征列表:', json_print(featList))
		uniqueVals = list(set(featList))
		debug_func('特征列表去重:', json_print(uniqueVals))
		newEntropy = 0
		for value in uniqueVals:
			subDataSet = feature_class_dataset(dataset, i, value)
			debug_func("剩余特征数据", json_print(subDataSet))
			prob = len(subDataSet)/float(len(dataset))
			#按特征分类后的熵
			newEntropy += prob*calculate_entropy(subDataSet)
		infoGain = baseEntropy-newEntropy
		if infoGain > bestInfoGain:
			bestInfoGain = infoGain
			bestFeature = i
		debug_func('=======================================')
	return bestFeature

#按类别数量排序
def majority_count(classList):
	classCount = {}
	for vote in classList:
		if vote not in classCount.keys():
			classCount[vote] = 0
		classCount[vote] += 1
	sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
	return sortedClassCount[0][0]

#创建决策树
def create_decision_tree(dataset, labels):
	classList = [example[-1] for example in dataset]
	if classList.count(classList[0]) == len(classList):
		return classList[0]
	if len(dataset[0]) == 1:
		return majority_count(classList)
	#选择最优特征
	bestFeat = choose_best_feature(dataset)
	bestFeatLabel = labels[bestFeat]
	#分类结果以字典形式保存
	mytree = {bestFeatLabel:{}}
	#删除最优特征,开始递归
	del(labels[bestFeat])
	featValues = [example[bestFeat] for example in dataset]
	uniqueVals = list(set(featValues))
	for value in uniqueVals:
		subLabels = labels[:]
		mytree[bestFeatLabel][value] = create_decision_tree(\
			feature_class_dataset(dataset, bestFeat, value), subLabels)
	return mytree
	

#理解熵计算过程
def main1():
	dataset, labels = create_dataset()
	entropy = calculate_entropy(dataset)
	print '总熵:',entropy
#理解特征分类过程
def main2():
	dataset, labels = create_dataset()
	bestFeature = choose_best_feature(dataset)
	
def main():
	dataset, labels = create_dataset()
	decision_tree = create_decision_tree(dataset, labels) 
	print '决策树：'
	print json_print(decision_tree)
	

if __name__ == '__main__':
	main()
