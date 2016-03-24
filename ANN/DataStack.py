# Created by Marcello Martins on Feb 14, 2016
# Last modified on Mar 23, 2016
# Extract features/data from wav files and saves to SupervisedDataSet np array for testing

# @file DataStack.py

import os
import numpy as np

HiphopDataSet1 = np.load("HiphopDataSet1.npy")
HiphopDataSet2 = np.load("HiphopDataSet2.npy")
HiphopDataSet3 = np.load("HiphopDataSet3.npy")
HiphopDataSet4 = np.load("HiphopDataSet4.npy")

JazzDataSet1 = np.load("JazzDataSet1.npy")
JazzDataSet2 = np.load("JazzDataSet2.npy")
JazzDataSet3 = np.load("JazzDataSet3.npy")
JazzDataSet4 = np.load("JazzDataSet4.npy")

ClassicalDataSet1 = np.load("ClassicalDataSet1.npy")
ClassicalDataSet2 = np.load("ClassicalDataSet2.npy")
ClassicalDataSet3 = np.load("ClassicalDataSet3.npy")
ClassicalDataSet4 = np.load("ClassicalDataSet4.npy")

CountryDataSet1 = np.load("CountryDataSet1.npy")
CountryDataSet2 = np.load("CountryDataSet2.npy")
CountryDataSet3 = np.load("CountryDataSet3.npy")
CountryDataSet4 = np.load("CountryDataSet4.npy")

DanceDataSet1 = np.load("DanceDataSet1.npy")
DanceDataSet2 = np.load("DanceDataSet2.npy")
DanceDataSet3 = np.load("DanceDataSet3.npy")
DanceDataSet4 = np.load("DanceDataSet4.npy")

MetalDataSet1 = np.load("MetalDataSet1.npy")
MetalDataSet2 = np.load("MetalDataSet2.npy")
MetalDataSet3 = np.load("MetalDataSet3.npy")
MetalDataSet4 = np.load("MetalDataSet4.npy")

ReggaeDataSet1 = np.load("ReggaeDataSet1.npy")
ReggaeDataSet2 = np.load("ReggaeDataSet2.npy")
ReggaeDataSet3 = np.load("ReggaeDataSet3.npy")
ReggaeDataSet4 = np.load("ReggaeDataSet4.npy")

RockDataSet1 = np.load("RockDataSet1.npy")
RockDataSet2 = np.load("RockDataSet2.npy")
RockDataSet3 = np.load("RockDataSet3.npy")
RockDataSet4 = np.load("RockDataSet4.npy")

DataSets = [HiphopDataSet1,HiphopDataSet2,HiphopDataSet3,HiphopDataSet4,JazzDataSet1,JazzDataSet2,JazzDataSet3,JazzDataSet4,ClassicalDataSet1,ClassicalDataSet2,ClassicalDataSet3,ClassicalDataSet4,CountryDataSet1,CountryDataSet2,CountryDataSet3,CountryDataSet4,DanceDataSet1,DanceDataSet2,DanceDataSet3,DanceDataSet4,MetalDataSet1,MetalDataSet2,MetalDataSet3,MetalDataSet4,ReggaeDataSet1,ReggaeDataSet2,ReggaeDataSet3,ReggaeDataSet4,RockDataSet1,RockDataSet2,RockDataSet3,RockDataSet4]

Data = np.array([]).reshape((0,2))
for DataSet in DataSets:
	Data = np.vstack([Data, DataSet])
np.save("Data/DataSetCompleteRaw.npy", Data)

######### BELOW IS A MESS OF CODE USED TO GET THE DATA WE HAVE TODAY ###############


# wdata = np.array([]).reshape(0,14)
# for data in DataSetCompleteWhitenClass:
# 	wdata = np.vstack([wdata, data[0]])

# wmin = np.argmin(wdata, axis=0)
# wmax = np.argmax(wdata, axis=0)

# dmin = []
# dmax = []

# for i, val in enumerate(wmin):
# 	dmin.append(DataSetCompleteWhitenClass[val][0][i])
# for i, val in enumerate(wmax):
# 	dmax.append(DataSetCompleteWhitenClass[val][0][i])

# for i in range(len(DataSetCompleteWhitenClass)):
# 	for j in range(len(DataSetCompleteWhitenClass[i][0])):
# 		DataSetCompleteWhitenClass[i][0][j] = (DataSetCompleteWhitenClass[i][0][j]-dmin[j])/(dmax[j]-dmin[j])
