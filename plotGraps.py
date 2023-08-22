import rasterio as rio
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
import matplotlib.dates as mdates

class getGraphs:
    def __init__(self):
        self.datesFpath = input(r"Date file to plot trend: ")
        self.imageStackFpath = input(r"Image stack to plot the trend: ")
        self.clusterFpath = input(r"Cluster image to select pixels: ")
        with rio.open(clusterFpath) as dst:
            self.clusterImg = dst.read(1)
            self.cMeta = dst.meta
        tempDates = np.loadtxt(dateFpath, dtype='str')
        self.Dates = [datetime.strptime(d, '%Y%m%d').date() for d in tempDates]
        with rio.open(self.imageStackFpath) as dst:
            self.img = dst.read()
            self.imgMeta = dst.meta
    def plotClusterId(self, clusterID, random=1000, ymin=-0.1, ymax=0.7, saveFpath=None, showPlot=False):
        temp = self.imageStackFpath[:,self.clusterImg==clusterID]
        randomIdxs = np.random.choice(range(temp.shape[1]), size = random)
        plt.clf()
        plt.ioff()
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%Y"))
        for i in randomIdxs:
            plt.plot(self.Dates, temp[:,i])
        plt.ylim(ymin, ymax)
        plt.xticks(self.Dates, rotation=70)
        plt.grid(axis='x')
        if saveFpath is not None:
            plt.savefig(saveFpath)
        if showPlot is True:
            plt.show()
        plt.clf()
    def plotAllClusters(self, saveFolder, random=1000, ymin=-0.1, ymax=0.7):
        for i in np.unique(self.clusterImg):
            saveFpath = Path(saveFolder, str(i)+'.jpg')
            self.plotClusterId(clusterID=i, random=random, ymin=ymin, ymax=ymax, saveFpath=saveFpath)
