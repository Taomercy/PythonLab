#！usr/bin/python
#!-*- coding:utf-8 -*-
from __future__ import division
from copy import deepcopy
#导入Node结构以进行封装
import numpy as np
import cv2

def cvd_task(args):
    x, clf, n_cores = args
    return np.array([clf.root.predict_one(xlis) for xlist in x])

#定义一个足够抽象的Tree结构的基类
class CvDBase(object):
    '''
        初始化结构
        self.node:记录所有Node的列表
        self.roots:主要用于CART剪枝的属性（用于存储算法过程中产生的各个决策树）
        self.max_depth:记录决策树最大深度的属性
        self.root, self.feature_sets, self.layers:主要用于ID3和C4.5剪枝的两个属性
        self.prune_alpha:惩罚因子
        self.layers:记录着每一层的Node
        self.whether_continuous:记录着各个维度的特征是否连续的列表
    '''
    def __init__(self, max_depth=None, node=None):
        self.nodes, self.layers, self.roots = [], [], []
        self.max_depth = max_depth
        self.root = node
        self.feature_sets = []
        self.label_dic = {}
        self.prune_alpha = 1
        self.y_transformer = None
        self.whether_continuous = None

    def __str__(self):
        return "CvDTree({})".format(self.root.height)

    __repr__ = __str__
    def feed_data(self, x, continuous_rate=0.2):
        #利用set获取各个维度特征的所有可能取值
        self.feature_sets = [set(dimension) for dimension in x.T]
        data_len, data_dim = x.shape
        #判断是否连续
        self.whether_continuous = np.array([len(feat) >= continuous_rate * data_len for feat in self.feature_sets])
        self.root.feats = [i for i in range(x.shape[1])]
        self.root.feed_tree(self)
        #参数alpha和剪枝有关
        #cv_rate用于控制交叉验证集的大小，train_only则控制程是否进行数据集的切分
    def fit(self, x, y, alpha=None, sample_weight=None, eps=1e-8, cv_rate=0.2, train_only=False):
        #数值化类别变量
        _dic = {c:i for i, c in enumerate(set(y))}
        print(_dic)
        y = np.array([_dic[ylist] for ylist in y])
        self.label_dic = {value:key for key, value in _dic.items()}
        x = np.array(x)
        self.y_transformer, y = np.unique(y, return_inverse=True)
        #根据特征个数定出alpha
        self.prune_alpha = alpha if alpha is not None else x.shape[1]/2
        #如果需要划分数据集的话
        if not train_only and self.root.is_cart:
            #根据cv_rate将数据集随机分成训练集和交叉验证集
            #实现的核心思想是利用下标来进行各种切分
            _train_num = int(len(x)*(1-cv_rate))
            _indices = np.random.permutation(np.arange(len(x)))
            _train_indices = _indices[:_train_num]
            _test_indices = _indices[_train_num:]
            if sample_weight is not None:
                #注意对切分后的样本权重做归一化处理
                _train_weights = sample_weight[_train_indices]
                _test_weights = sample_weight[_test_indices]
                _train_weights /= np.sum(_train_weights)
                _test_weights /= np.sum(_test_weights)
            else:
                _train_weights = _test_weights = None
                x_train, y_train = x[_train_indices], y[_train_indices]
                x_cv, y_cv = x[_test_indices], y[_test_indices]
        else:
            x_train, y_train, _train_weights = x, y, sample_weight
            x_cv = y_cv = _test_weights = None
            self.feed_data(x_train)
            #调用根节点的生成算法
            self.root.fit(x_train, y_train, _train_weights, eps)
            #调用对Node剪枝算法的封装
            self.prune(x_cv, y_cv, _test_weights)

    def reduce_nodes(self):
        for i in range(len(self.nodes)-1, -1, -1):
            if self.nodes[i].pruned:
                self.nodes.pop(i)

    def _update_layers(self):
        #根据整棵决策树的高度，在self.layers里面放相应数量的列表
        self.layers = [[] for i in range(self.root.height)]
        self.root._update_layers()
    
        #ID3、C4.5的剪枝算法
    def _prune(self):
        self._update_layers()
        _tmp_nodes = []
        #更新完决策树每一层的Node之后，从后往前地向_tmp_nodes中加Node
        for node_list in self.layers[::-1]:
            for node in node_list[::-1]:
                if node.category is None:
                    _tmp_nodes.append(node)
                    _old = np.array([node.cost()+self.prune_alpha*len(node.leafs) for node in _tmp_nodes])
                    _new = np.array([node.cost(pruned=True)+self.prune_alpha for node in _tmp_nodes])
                    #使用_mask变量存储_old 和 _new对应位置的大小关系
                    _mask = _old >= _new
                    mask = [_mask, ~_mask]
                    while True:
                        #若只剩根节点就退出循环体
                        if self.root.height == 1:
                            break;
                        p = np.argmax(mask)
                        #如果_new中有比_old中对应损失小的损失，则进行局部剪枝
                           if mask[p]:
                               _tmp_nodes[p].prune()
                               #根据被一估量了的Node，跟_new、_old、_mask对应位置的值
                               for i, node in enumerate(_tmp_nodes):
                                   if node.affected:
                                       old[i] = node.cost()+self.prune_alpha*len(node.leafs)
                                       mask[i] = old[i] >= new[i]
                                       node.affected = False
                               #根据被剪掉的Node，将各个变量对应的位置除去（注意从后往前遍历）
                               for i in range(len(_tmp_nodes), -1, -1):
                                   if _tmp_nodes[i].pruned:
                                       _tmp_nodes.pop(i)
                                       old = np.delete(old, i)
                                       new = np.delete(mask, i)
                                   else:
                                       break
                       self.reduce_nodes()

    def prune(self, x_cv, y_cv, weights):
           if self.root.is_cart:
               if x_cv is not None and y_cv is not None:
                   self._cart_prune()
                   arg = np.argmax([CvDBase.acc(y_cv, tree.predict(x_cv), weights) for tree in self.roots]) #type: int
                   tar_root = self.roots[arg]
                   self.nodes = []
                   tar_root.feed_tree(self)
                   self.root = tar_root
           else:
               self._prune()

           #Util
    def predict_one(self, x):
        return self.y_transformer[self.root.predict_one(x)]

    def predict(self, x, get_raw_results=False, **kwargs):
        return self.y_transformer[self._multi_data(x, cvd_task, kwargs)]

    def view(self):
        self.root.view()

    def visualize(self, radius=24, width=1200, height=800, padding=0.2, plot_num=30, title="CvDTree"):
        self._update_layers()
        units = [len(layer) for layer in self.layers]
        img = np.ones((height, width, 3), np.uint8)*255
        axis0_padding = int(height/(len(self.layers)-1 + 2*padding))*padding + plot_num
        axis0 = np.linspace(axis0_padding, height - axis0_padding, len(self.layers), dtype=np.int)
        axis1_padding = plot_num
        axis1 = [np.linspace(axis1_padding, width - axis1_padding, unit+2, dtype=np.int) for unit in units]
        axis1 = [axis[1:-1] for axis in axis1]
        for i, (y, xs) in enumerate(zip(axis0, axis1)):
            for j, x in enumerate(xs):
                if i == 0:
                    cv2.circle(img, (x, y), radius, (255, 100, 125), 1)
                else:
                    cv2.circle(img, (x, y), radius, (125, 100, 255), 1)
                node = self.layers[i][j]
                if node.feature_dim is not None:
                    text = str(node.feature_dim + 1)
                    color = (0, 0, 255)
                else:
                    text = str(self.y_transformer[node.category])
                    color = (0, 255, 0)
                cv2.putText(img, text, (x-7*len(text)+2, y+3), cv2.LINE_AA, 0.6, color, 1)

        for i, y in enumerate(axis0):
            if i == len(axis0)-1:
                break
            for j, x in enumerate(axis1[i]):
                new_y = axis0[i+1]
                dy = new_y-y-2*radius
                for k, new_x in enumerate(axis1[i+1]):
                    dx = new_x-x
                    length = np.sqrt(dx**2+dy**2)
                    ratio = 0.5-min(0.4, 1.2*24/length)
                    if self.layers[i+10][k] in self.layers[i][j].children.values():
                        cv2.line(img, (x, y+radius), (x+int(dx*ratio), y+radius+int(dy*ratio)), (125, 125, 125), 1)
                        cv2.putText(img, str(self.layers[i+1][k].prev_feat),\
                            (x+int(dx*0.5)-6, y+radius+int(dy*0.5)), cv2.LINE_AA, 0.6, (0, 0, 0), 1)
                        cv2.line(img, (new_x-int(dx*ratio), new_y-radius-int(dy*ratio)), (new_x, new_y-radius), (125, 125, 125), 1)
                        cv2.imshow(title, img)
                        cv2.waitKey(0)
                        return img

class CvDMeta(type):
    def __new__(mcs, *args, **kwargs):
        name, bases, attr = args[:3]_, _node = bases

    def __init__(self, whether_continuous=None, max_depth=None, node=None, **kwargs):
        tmp_node = node if isinstance(node, CvDNode) else _node
        CvDBase.__init__(self, max_depth, tmp_node(**kwargs))
        self._name = name

    attr["__init__"] = __init__
    return type(name, bases, attr)

class ID3Tree(CvDBase, ID3Node, metaclass=CvDMeta):
    pass

class C45Tree(CvDBase, C45Tree, metaclass=CvDMeta):
    pass

class CartTree(CvDBase, CartNode, metaclass=CvDMeta):
    def evaluate(self, x, y):
        print(x)
        rt = self.root.predict(x)
        print('结果：', rt)

    def evaluate2(self, x):
        print('\033[1;32m')
        print('*'*30)
        print(x)
        rt = self.root.predict_one(x)
        print('结果：', rt)
        print('*'*30)
        print('\033[0m')

