#！usr/bin/python
#!-*- coding:utf-8 -*-
import numpy as np
from Cluster import Cluster
#定义一个足够抽象的基类，以囊括所有我们关心的算法
class CvDNode(object):
	'''
		初始化结构
		self._x, self._y:记录数据集的变量
		self.base, self.chaos:记录对数的底和当期的不确定性
		self.criterion, self.category:记录该node计算信息增益的方法和所属类别
		self.left_child, self.right_child:针对连续性特征和CART、记录Node的左右子节点
		self.children, self.leafs:记录该Node的所有子节点和所有下属叶节点
		self.sample_weight:记录样本的权重
		self.wc:记录各个维度的特征是否连续的列表(whether continuous的缩写)
		self.tree:记录该Node所属的Tree
		self.feature_dim, self.tar, self.feats:记录该Node划分标准的相关信息。具体而言：
			self.feature_dim:记录作为划分标准的特征所对应的维度j
			self.tar:针对连续型特征和CART，记录二分标准
			self.feats:记录该Node能进行的、作为划分标准的特征的维度
			self.parent, self.is_root:记录该Node的父节点以及是否为根节点
			self.depth, self.prev_feat:记录Node的深度和其父节点的划分标准
			self.is_cart:记录该Node是否使用了CAR算法
			self.is_continuous:记录该Node选择的划分标准对应的特征是否连续
			self.pruned:记录该Node是否已被剪掉，后面实现局部剪枝算法时会用到
	'''
	def __init__(self, tree=None, base=2, chaos=None, depth=0, parent=None, is_root=True, prev_feat="Root"):
		self._x = self._y = None
		self.base, self.chaos = base, chaos
		self.criterion = self.category = None
		self.left_child = self.right_child = None
		self.children, self.leafs = {}, {}
		self.sample_weight = None
		self.wc = None
		self.tree = tree
		#如果传入了Tree的话就进行相应的初始化
		if tree is not None:
			#由于数据处理是由Tree完成的
			#所以各个维度的特征是否是连续型随机变量也是由Tree记录的
			self.wc = tree.whether_continuous
			#这里的nodes变量是Tree中记录所有Node的列表
			tree.nodes.append(self)
		self.feature_dim, self.tar. self.feats = None, None, []
		self.parent, self.is_root = parent, is_root
		self.depth, self.prev_feat = depth, prev_feat
		self.is_cart = self.is_continuous = self.pruned = False

	def __getitem__(self, item):
		if isinstance(item, str):
			return getattr(self, "_"+item)

	#重载__lt__方法，使得Node之间可以比较谁更小，进而方便调试和可视化
	def __lt__(self, other):
		return self.prev_feat < other.prev_feat

	#重载__str__和__repr__方法，同样为了方便调试
	def __str__(self):
		if self.category is None:
			return "CvDNode ({}) ({} -> {})".format(self.depth, self.prev_feat, self.tree.label_dict[self.category])

	__repr__ = __str__

	#定义children属性，注意区分开连续+CART的情况和其余的情况
	#有了该属性后，想要获得所有子节点时就不用分情况讨论了

	@property
	def info(self):
		if self.category is None:
			return "CvDNode ({}) ({} -> {})".format(self.depth, self.prev_feat, self.tree.y_transformer[self.category])

	@property
	def children(self):
		return {"left": self.left_child, "right": self.right_child} if (self.is_cart or self.is_continuous) else self._children

	#递归定义height
	#叶节点高度都定义为1，其余节点的高度定义为最高的子节点高度+1

	@property
	def height(self):
		if self.category is not None:
			return 1
		return 1 + max([_child.height if _child is not None else 0 for _child in self.children.values()])


	#定义info_dict，它记录了该Node的主要信息
	#在更新各个Node的叶节点时，被记录进各个self.leafs属性的就是该字典
	@property
	def info_dict(self):
		return {"chaos": self.chaos, "y": self._y}


	#定义一种停止准则：当特征维度为0或者当Node的数据不确定性小于阈值时停止
	#同时，如果用户指定了巨额树的最大深度，那么当该Node的深度太深时也停止
	#若满足了停止条件，该函数返回True，否则返回False
	def stop1(self, eps):
		if (self._x.shape[1] == 0 or (self.chaos is not None and self.chaos <= eps) or \
			(self.tree.max_depth is not None and self._depth >= self.tree.max_depth)):
			#调用处理停止情况的方法
			self._handle_terminate():
			return True
		return False

	#定义第二种停止准则，当最大信息增益仍然小于阈值时停止
	def stop2(self, max_gain, eps):
		if max_gain <= eps:
			self._handle_terminate()
			return True
		return False

	#利用bincount方法定义根据数据生成该Node所属类别的方法
	def get_category(self):
		return np.argmax(np.bincount(self._y))

	#定义处理性质情况的方法，核心思想就是把Node转化为一个叶节点
	def _handle_terminate(self):
		#首先要生产该Node所属的类别
		self.category = self.get_category()
		#然后一路回溯，更新父节点、父节点的父节点，等等，记录叶节点的属性leafs
		_parent = self.parent
		while _parent is not None:
			_parent.leafs[id(self)] = self.info_dict
			_parent = _parent.parent


	def prune(self):
		#调用相应方法进行计算该Node所属类别
		self.category = self.get_category()
		#记录由于该Node转化为叶节点而被剪去的、下属的叶节点
		_pop_list = [key for key in self.leafs]
		#然后一路回溯，更新各个parent的属性leafs，使用id作为键避免重复
		_parent = self.parent
		while _parent is not None:
			for _k in _pop_list:
				#删去由于拒不剪枝而被剪掉的叶节点
				_parent.leafs.pop(_k)
			_parent.leafs[id(self)] = self.info_dict
			_parent = _parent.parent

		#调用mark_pruned方法将自己所有的子节点、子节点的子节点，等等， 的pruned属性置为True，因为他们被剪掉了
		self.mark_pruned()
		#重置各个属性
		self.feature_dim = None
		self.left_child = self.right_child = None
		self.children = {}
		self.leafs = {}


	def mark_pruned(self):
		self.pruned = True
		#遍历各个子节点
		for _child in self.children.values():
			#如果当前的子节点不是None的话，递归调用mark_pruned方法
			#连续型特征和CART算法由可能导致children中出现None,因为此时children可能由left_child和right_child组成，他们有可能是None
			if _child is not None:
				_child.mark_pruned()

	def fit(self, x, y, sample_weight, feature_bound=None, eps=1e-8):
		self._x, self._y = np.atleast_2d(x), np.array(y)
		self.sample_weight = sample_weight
		#若满足第一种体制准则，则退出函数体
		if self.stop1(eps):
			return

		#用该Node的数据实例化Cluster类以计算各种信息量
		_cluster = Cluster(self._x, self._y, sample_weight, self.base)
		if self.is_root:
			if self.criterion == "gini":
				self.chaos = _cluster.gini()
			else:
				self.chaos = _cluster.ent()

		_max_gain, _chaos_list = 0, []
		_max_feature = _max_tar = None
		#遍历还能选择的特征
		for feat in self.feats:
			#如果适合连续性特征或是CART算法，需要额外计算二分标准的取值集合
			if self.wc[feat]:
				_samples = np.sort(self._x.T[feat])
				_set = (_samples[:-1] + _samples[1:]*0.5)
			if self.is_cart:
				_set = self.tree.feature_sets[feat]

			#然后遍历这些二分标准并调用二类问题相关的计算信息量的方法
			if self.is_cart or self.wc[feat]:
				for tar in _set:
					_tmp_gain, _tmp_chaos_list = _cluster.bin_info_gain(feat, tar, criterion=self.criterion,\
						get_chaos_list=True, continuous=self.wc[feat])
					if _tmp_gain > _max_gain:
						(_max_gain, _chaos_list), _max_feature, _max_tar = (_tmp_gain, _tmp_chaos_list), feat, tar
			#对于脸型特征的ID3和C4.5算法，调用普通的计算信息量的方法
			else:
				_tmp_gain, _tmp_chaos_list = _cluster.info_gain(feat, self.criterion, True, self.tree.feature_sets[feat])
				if _tmp_gain > _max_gain:
					(_max_gain, _chaos_list), _max_feature = (_tmp_gain, _tmp_chaos_list), feat

		#若满足第二种停止准则，则退出函数体
		if self.stop2(_max_gain, eps):
			return
		#更新相关的属性
		self.feature_dim = _max_feature
		if self.is_cart or self.wc[_max_feature]:
			self.tar = _max_tar

			#调用根据划分标准进行生成的方法
			self._gen_children(_chaos_list, feature_bound)
			#如果该Node的左子节点和右子节点都是叶节点且所属类别一样，那么就将他们合并，亦即进行局部剪枝
			if (self.left_child.category is not None and self.left_child.category == self.right_child.category):
				self.prune()
				#调用Tree的相关方法，将被剪掉的该Node的左右子节点从Tree的记录所有Node的列nodes中出去
				self.tree.reduce_nodes()
			else:
				self._gen_children(_chaos_list, feature_bound)

	def _gen_children(_chaos_list, feature_bound):
		feat, tar = self.feature_dim, self.tar
		self.is_continuous = continuous = self.wc[feat]
		features = self._x[...,feat]
		new_feats = self.feats.copy()
		if continuous:
			mask = features < tar
			masks = [mask, ~mask]
		else:
			if self.is_cart:
				mask = features == tar
				masks = [mask, ~mask]
				self.tree.feature_sets[feat].discard(tar)
			else:
				masks = None
		if self.is_cart or continuous:
			feats = [tar, '+'] if not continuous else ["{:6.4}-".format(tar), "{:6.4}+".format(tar)]
			for feat, side, chaos in zip(fests, ["left_child", "right_child"], _chaos_list):
				new_node = self.__class__(self.tree, self.base, chaos=chaos, depth=self._depth+1,\
					parent=self, is_root=False, prev_feat=feat)
				new_node.criterion = self.criterion
				setattr(self, side, new_node)
			for node, feat_mask in zip([self.left_child, self.right_child], masks):
				if self.sample_weight is None:
					local_weights = None
				else:
					local_weights = self.sample_weight[feat_mask]
					local_weights /= np.sum(local_weights)
					tmp_data, tmp_labels = self._x[feat_mask, ...], self._y[feat_mask]
				if len(tmp_labels) == 0:
					continue
				node.fit(tmp_data, tmp_labels, local_weights, feature_bound)
		else:
			new_feats.remove(self.feature_dim)
			for feat, chaos in zip(self.tree.feature_sets[self.feature_dim], _chaos_list):
				feat_mask = features == feat
				tmp_x = self._x[feat_mask, ...]
				if len(tmp_x) == 0:
					continue
				new_node = self.__class__(tree=self.tree, base=self.base, chaos=chaos,\
					depth=self._depth+1, parent=self, is_root=False, prev_feat=feat)
				new_node.feats = new_feats
				self.children[feat] = new_node
				if self.sample_weight is None:
					local_weights = None
				else:
					local_weights = self.sample_weight[feat_mask]
					local_weights /= np.sum(local_weights)
				new_node.fit(tmp_x, self._y[feat_mask], local_weights, feature_bound)

	#Util
	def update_layers(self):
		#根据该Node的深度，在self.layers对应位置的列表中记录自己
		self.tree.layers[self._depth].append(self)
		#遍历所有子节点，完成递归
		for node in sorted(self.children):
			node = self.children[node]
			if node is not None:
				node.update_layers()

	def cost(self, pruned=False):
		if not pruned:
			return sum([leaf["chaos"]*len(leaf["y"]) for leaf in self.leafs.values()])
		return self.chaos*len(self._y)

	def get_threshold(self):
		return (self.cost(pruned=True) - self.cost()) / (len(self.leafs) - 1)

	def cut_tree(self):
		self.tree = None
		for child in self.children.values():
			if child is not None:
				child.cut_tree()

	def feed_tree(self, tree):
		self.tree = tree
		self.tree.nodes.append(self)
		self.wc = tree.whether_continuous
		for child in self.children.values():
			if child is not None:
				child.feed_tree(tree)

	def predict_one(self, x):
		if self.category is not None:
			return self.category
		if self.is_continuous:
			if x[self.feature_dim] < self.tar:
				return self.left_child.predict_one(x)
			return self.right_child.predict_one(x)
		if self.is_cart:
			if x[self.feature_dim] == self.tar:
				return self.left_child.predict_one(x)
			return self.right_child.predict_one(x)
		else:
			try:
				return self.children[x[self.feature_dim]].predict_one(x)
			except KeyError:
				return self.get_category()

	def predict(self, x):
		return np.array([self.predict_one(xx) for xx in x])

	def view(self, indent=4):
		print("==", ""*indent*self._depth, self.info)
		for node in sorted(self.children):
			node = self.children[node]
			if node is not None:
				node.view()

class ID3Node(CvDNode):
	def __init__(self, *args, **kwargs):
		CvDNode.__init__(self, *args, **kwargs)
		self.criterion = "ent"

class C45Node(CvDNode):
	"""docstring for C45Node"""
	def __init__(self, *args, **kwargs):
		CvDNode.__init__(self, *args, **kwargs)
		self.criterion = "ratio"

class CartNode(CvDNode):
	def __init__(self, *args):
		CvDNode.__init__(self, *args, **kwargs)
		self.criterion = "gini"
		self.is_cart = True
		


	
	
	