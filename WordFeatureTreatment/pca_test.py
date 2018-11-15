#!usr/bin/env python
#! -*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.datasets.samples_generator import make_blobs
x, y = make_blobs(n_samples=1000, n_features=3, centers=[[3,3,3], [0,0,0], [1,1,1], [2,2,2]], cluster_std=[0.2, 0.1, 0.2, 0.2], random_state=9)
fig = plt.figure()
#ax = Axes3D(fig, rect=[0,0,1,1], elev=30, azim=20)
ax = plt.subplot(111, projection='3d')
plt.scatter(x[:,0], x[:,1], x[:,2], c='b', marker='o')
plt.show()
from sklearn.decomposition import PCA
pca = PCA(n_components=3)
pca.fit(x)
print pca.explained_variance_ratio_
print pca.explained_variance_
pca1 = PCA(n_components=2)
pca1.fit(x)
print pca1.explained_variance_ratio_
print pca1.explained_variance_
x_new = pca1.transform(x)
plt.scatter(x_new[:,0], x_new[:,1], c='b', marker='o')
plt.show()
