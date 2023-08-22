import numpy as np
import rasterio as rio
from tslearn import clustering
from pathlib import Path
import matplotlib.pyplot as plt

class kMeansCluster:
    def __init__(self,):
        print("Work in progress")
    def getImage(self, imageFpath):
        with rio.open(imageFpath) as dst:
            self.Image = dst.read()
            self.meta = dst.meta
            self.shape = self.Image.shape
        self.flatImg = self.Image.reshape(self.shape[0],-1).T
    def getElbowCurve(self,clusters=50):
        clusterList = []
        inertiaList = []
        labelList = []
        i = 2
        while i <= n_clusters:
            print(i)
            km_dst = clustering.TimeSeriesKMeans(n_clusters=i, metric="euclidean", 
                n_init=1, n_jobs=5, max_iter=1,max_iter_barycenter=1,).fit(self.flatImg)
            print("K means estimated")
            clusterList.append(i)
            inertiaList.append(km_dst.inertia_)
            labelList.append(km_dst.labels_)
            i+= 1
        plt.plot(clusterList, inertiaList)
        plt.title("Elbow Curve")
        plt.xlabel("Cluster Number")
        plt.ylabel("Inertia")
        plt.show()
        # return clusterList, inertiaList, labelList
    def getKmeansTSL(self, n_clusters=50, ret=True, save=True, savePath=None):
        self.km_tslearn = clustering.TimeSeriesKMeans(
            n_clusters=n_clusters, metric="euclidean", n_init=3, 
            n_jobs=5, max_iter=5,max_iter_barycenter=3,).fit(self.flatImg)
        if ret==True: 
            return self.km_tslearn
    def getKmeansCV(self, n_clusters=50, ret=False, savePath=None):
        shape = self.shape
        tempImg = np.zeros(shape[1], shape[2], shape[3])
        for i in range(shape[0]):
            tempImg[:,:,i] = self.Image[i]
        satz = tempImg.reshape((-1, tempImg.shape[2]))
        satz = np.float32(satz)
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        ret,label,center=cv.kmeans(satz,n_clusters,None,criteria,10,cv.KMEANS_RANDOM_CENTERS)
        label += 1
        labelImg = label.reshape(tempImg.shape[:2])
        self.labelImg_cv = labelImg
        if ret==True:
            return labelImg
        if savePath is not None:
            #TODO: Change the data type of input data according to meta file
            meta = self.meta
            meta.update(count=1)
            if savePath==None:
                print("Please enter the save path")
            with rio.open(savePath, 'w', **meta) as dst:
                dst.write(labelImg)
