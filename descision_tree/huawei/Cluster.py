#！usr/bin/python
#!-*- coding:utf-8 -*-
import math
import numpy as np

class Cluster(object):
    '''
        初始化结构
        self._x, self._y:记录数据集的变量
        self._counters:类别向量的计数器，记录第i类数据的个数
        self._sample_weightple_weight:记录样本权重的属性
        self._con_chaos_cache, self._ent_cache, self._gini_cache:记录中间结果的属性
        self._base:记录对数的底的属性
    '''
    def __init__(self, x, y, sample_weight=None, base=2):
        #这里我们要求输入的是Numpy向量（矩阵）
        self._x, self._y = x.T, y
        self._sample_weight = sample_weight
        self._con_chaos_cache = self._ent_cache = self._gini_cache = None
        self._base = base
        #利用样本权重对类别向量y进行计数
        if _sample_weight is None:
            self._counters = np.bincount(self._y)
        else:
            self._counters = np.bincount(self._y, weights=_sample_weight*len(_sample_weight))
        
    #定义计算信息熵的函数
    def ent(self, ent=None, eps=1e-12):
        #如果已调用过且调用时没有额外给各类别样本的个数，就直接调用结果
        if self._ent_cache is not None and ent is None:
            return self._ent_cache
        _len = len(self._y)
        #如果调用时没有给各类别样本的个数，就利用结构本身的计数器来获取相应的个数
        if ent is None:
            ent = self._counters
        #使用eps来让算法的数值稳定性更好
        _ent_cache = max(eps, -sum([_c/_len*math.log(_c/_len, self._base) if _c != 0 else 0 for _c in ent]))
        #如果调用时没有给各类别样本的个数，就将计算好的信息熵储存下来
        if ent is None:
            self._ent_cache = _ent_cache
        return _ent_cache

    #定义计算基尼系数的函数和计算信息熵的函数很类似，所以略去解释
    def gini(self, p=None):
        if self._gini_cache is not None and p is None:
            return self._gini_cache
        if p is None:
            p = self._counters
        _gini_cache = 1 - np.sum((p/len(self._y))**2)
        if p is None:
            self._gini_cache = _gini_cache
        return _gini_cache

    #定义计算H(y|A)和Gini(y|A)的函数
    def con_chaos(self, idx, criterion='ent', features=None):
        #根据不用的准则，调用不同的方法
        if criterion == 'ent':
            _method = lambda Cluster:cluster.ent()
        else:
            _method = lambda Cluster:cluster.gini()
        #根据输入获取相应维度的向量
        data = self._x[idx]
        #如果调用时没有给该维度的取值空间features,就调用set方法获得该取值空间
        #由于调用set方法比较耗时，在决策树实现时应努力将features传入
        if features is None:
            features = set(data)
        #获得该维度特征各取值所对应的数据的下标
        #用self._con_chaos_cache记录下相应结果以加速后面定义的相关参数
        tmp_labels = [data == feature for feature in features]
        self._con_chaos_cache = [np.sum(_label) for _label in tmp_labels]
        #利用下标获取相应的类别向量
        label_list = [self._y[label] for label in tmp_labels]
        rs, chaos_list = 0, []
        #遍历各下标和对应的类别向量
        for data_label, tar_label in zip(tmp_labels, label_list):
            #获取相应的数据
            tmp_data = self._x.T[data_label]
            #根据相应数据、类别向量和样本权重计算出不确定性
            if self._sample_weight is None:
                _chaos = _method(Cluster(tmp_data, tar_label, base=self._base))
            else：
                _new_weights = self._sample_weight[data_label]
                _chaos = _method(Cluster(tmp_data, tar_label, _new_weights/np.sum(_new_weights), self._base))
                #依概率加权，同时把各个初始套件不确定性记录下来
                rs += len(tmp_data)/len(data)*_chaos
                chaos_list.append(_chaos)
        return rs, chaos_list

    #定义计算信息增益的函数，参数get_chaos_list用于控制输出
    def info_gain(self, idx, criterion='ent', get_chaos_list=False, features=None):
        #根据不同的准则，获取相应的“条件不确定性”
        if criterion in ("ent", "ratio"):
            _con_chaos, _chaos_list = self.con_chaos(idx, "ent", features)
            _gain = self.ent() - _con_chaos
            if criterion == "ratio":
                _gain /= self.ent(self._con_chaos_cache)
        else:
            _con_chaos, _chaos_list = self.con_chaos(idx, "gini", features)
            _gain = self.gini() - _con_chaos
        return (_gain, _chaos_list) if get_chaos_list else _gain

    #定义计算二类问题条件不确定性的函数
    #参数tar既是二分标准，参数continuous则告诉我们该维度的特征是否连续
    def bin_con_chaos(self, idx, tar, criterion="gini", continuous=False):
        if criterion == "ent":
            _method = lambda Cluster:cluster.ent()
        else:
            _method = lambda Cluster:cluster.gini()
        data = self._x[idx]
        #根据二分标准划分数据，注意要分离散和连续两种情况讨论
        tar = data == tar if not continuous else data < tar
        tmp_labels = [tar, ~tar]
        self._con_chaos_cache = [np.sum(_label) for _label in tmp_labels]
        label_list = [self._y[label] for label in tmp_labels]
        rs, chaos_list = 0, []
        for data_label, tar_label in zip(tmp_labels, label_list):
            tmp_data = self._x.T[data_label]
            if self._sample_weight is None:
                _chaos = _method(Cluster(tmp_data, tar_label, base=self._base))
            else:
                _new_weights = self._sample_weight[data_label]
                _chaos = _method(Cluster(tmp_data, tar_label, _new_weights/np.sum(_new_weights), base=self._base))
                rs += len(tmp_data)/len(data)*_chaos
                chaos_list.append(_chaos)
        return rs, chaos_list

    def bin_info_gain(self, idx, tar, criterion="gini", get_chaos_list=False, continuous=False):
        if criterion in ("ent", "ratio"):
            con_chaos, chaos_list = self.bin_con_chaos(idx, tar, "ent", continuous)
            gain = self.ent() - con_chaos
            if criterion == "ratio":
                #noinspection PyTypeChecker
                gain = gain / self.ent(self._con_chaos_cache)
        elif criterion == "gini":
            con_chaos, chaos_list = self.bin_con_chaos(idx, tar, "ent", continuous)
            gain = self.gini() - con_chaos
        else:
            raise NotlmplementedError("info_gain criterion '{}' not defined".format(criterion))
        return (gain, chaos_list) if get_chaos_list else gain


