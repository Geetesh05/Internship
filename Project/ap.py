import pandas as pd
from matplotlib import *
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
from scipy.spatial import ConvexHull
from shapely.geometry import Point, Polygon
import time
import math
from sklearn.neighbors import NearestNeighbors
from matplotlib.path import Path
from matplotlib.patches import Polygon as pol
from sklearn.preprocessing import normalize
from scipy.stats import zscore
from scipy.special import comb
from bottom_up import bottom
from nn import nearest
from best_first import bfs
from greedy import greedy
def process(file1,file2,num,threshold):
    df = pd.read_csv(file1, sep=';')
    # removing null files
    inp = len(df.axes[1])
    main = df.iloc[:, 2:inp - 1].values
    dr = df.iloc[:, inp - 1:].values
    data = pd.read_csv(file2, delimiter="\t")
    a = []
    for i in data["entrez_gene_ids"]:
        a.append(i.split(","))

    f = []
    for i in range(len(a)):
        f.append(pd.DataFrame(a[i], columns=["Entrez gene"]))
    z = []
    set1 = []
    pathways_names = []
    d2 = StandardScaler().fit_transform(main)
    pca = PCA(n_components=2)
    result1 = pca.fit_transform(d2)
    x1 = []
    y1 = []
    for x in range(len(f)):
        h = pd.merge(df.astype(float), f[x].astype(float))
        if len(h) > 2:
            x1.append(np.dot(h.iloc[:, 2:inp - 1].values, np.transpose(pca.components_[0])))
            y1.append(np.dot(h.iloc[:, 2:inp - 1].values, np.transpose(pca.components_[1])))
            pathways_names.append(data["pathway"][x])

    x = np.dot(main, np.transpose(pca.components_[0]))
    y = np.dot(main, np.transpose(pca.components_[1]))

    loading = np.transpose([x, y])
    match = []
    for i in range(len(x1)):
        tem = []
        for j in range(len(x1[i])):
            t = [x1[i][j], y1[i][j]]
            tem.append(t)

        match.append(tem)
    pca_result = np.transpose(match).tolist()
    pca_result1 = loading
    dd = StandardScaler().fit_transform(np.transpose(main))
    f3 = pd.DataFrame(dd)
    x2 = np.dot(f3, np.transpose(loading[:, 0]))
    y2 = np.dot(f3, np.transpose(loading[:, 1]))
    scores = []
    for i in range(len(x2)):
        temp = []
        temp.append(x2[i])
        temp.append(y2[i])
        scores.append(temp)
    if num==1:
        bottom(pca_result,pca_result1,pathways_names,scores)
        print("yes")
    elif num==2:
        print("yes")
        if len(threshold)==0:
            nearest(pca_result,pca_result1,pathways_names,0.1,scores)
        else:
            nearest(pca_result,pca_result1,pathways_names,threshold,scores)

    elif num==3:
        print("yes")
        bfs(pca_result,pca_result1,pathways_names,scores)
    else:
        print("yes")
        if len(threshold)==0:
            greedy(pca_result,pca_result1,pathways_names,0.1,scores)
        else:

            greedy(pca_result, pca_result1, pathways_names, threshold, scores)



