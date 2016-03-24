# Created by Marcello Martins on Feb 14, 2016
# Last modified on Mar 23, 2016
# Extract features/data from wav files and saves to SupervisedDataSet np array for testing

# @file data.py

from __future__ import print_function # Python 2/3 compatibility
import librosa
import os
import numpy as np
from pybrain.datasets import SupervisedDataSet, ClassificationDataSet
from scipy.cluster.vq import whiten
from multiprocessing import Process
import math
from numpy import array_equal


answer = [[1,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0],[0,0,1,0,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0],[0,0,0,0,0,1,0,0],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,1]]

DSSuperRaw = SupervisedDataSet(14, 8)
DSClassRaw = ClassificationDataSet(14, 1)

DSSuperWhiten = SupervisedDataSet(14, 8)
DSClassWhiten = ClassificationDataSet(14, 1)

DSSuperNorm = SupervisedDataSet(14, 8)
DSClassNorm = ClassificationDataSet(14, 1)

# DS = SupervisedDataSet.loadFromFile("DataSet")

DataSetCompleteRaw = np.load("Data/DataSetCompleteRaw.npy")
DataSetCompleteRawClass = np.load("Data/DataSetCompleteRawClass.npy")
DataSetCompleteWhiten = np.load("Data/DataSetCompleteWhiten.npy")
DataSetCompleteWhitenClass = np.load("Data/DataSetCompleteWhitenClass.npy")
DataSetCompleteNorm = np.load("Data/DataSetCompleteNorm.npy")
DataSetCompleteNormClass = np.load("Data/DataSetCompleteNormClass.npy")

for data in DataSetCompleteRaw:
	DSSuperRaw.appendLinked(data[0],data[1])
for data in DataSetCompleteRawClass:
	DSClassRaw.addSample(data[0],data[1])
for data in DataSetCompleteWhiten:
	DSSuperWhiten.appendLinked(data[0],data[1])
for data in DataSetCompleteWhitenClass:
	DSClassWhiten.addSample(data[0],data[1])
for data in DataSetCompleteNorm:
	DSSuperNorm.appendLinked(data[0],data[1])
for data in DataSetCompleteNormClass:
	DSClassNorm.addSample(data[0],data[1])

DSSuperRaw.saveToFile("Data/DSSuperRaw")
DSClassRaw.saveToFile("Data/DSClassRaw")
DSSuperWhiten.saveToFile("Data/DSSuperWhiten")
DSClassWhiten.saveToFile("Data/DSClassWhiten")
DSSuperNorm.saveToFile("Data/DSSuperNorm")
DSClassNorm.saveToFile("Data/DSClassNorm")


# np.save("Data/DataSetCompleteWhiten.npy", DataSetCompleteRaw)
# print(np.argmin(tdata, axis=0))

# np.save("Data/DataSetCompleteWhitenClass.npy", DataSetCompleteWhiten)

# #DS.saveToFile("DataSetComplete")