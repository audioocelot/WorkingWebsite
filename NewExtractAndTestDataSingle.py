from __future__ import print_function
from subprocess import call
from numpy import array_equal
import numpy as np
import csv
import os
import sys
from pybrain.tools.xml.networkwriter import NetworkWriter
from pybrain.tools.xml.networkreader import NetworkReader
import json

isEC2Server = False
pathPrefix = ""
if isEC2Server:
    pathPrefix = "/home/ubuntu/"


def GetFeatures(path):
    with open(path,
              'rb') as genreFile:
        genreSamples = csv.reader(genreFile)
        floatSample = []
        sample = next(genreSamples)
        for feature in sample[1:385]:
            floatSample.append(float(feature))
        return np.array(floatSample)

genres = ["classical", "country", "electronic", "hip hop",
          "jazz", "metal", "reggae", "rock"]

MIN = np.load(pathPrefix + "OcelotApp/MIN.npy")
MAX = np.load(pathPrefix + "OcelotApp/MAX.npy")
PTP = np.load(pathPrefix + "OcelotApp/PTP.npy")


open(pathPrefix + "OcelotApp/Temp.csv", 'w').close()
rd = os.system(
    "sudo " + pathPrefix + "openSMILE/inst/bin/SMILExtract "
    + "-C " + pathPrefix + "openSMILE/config/IS09_emotion.conf "
    + "-I " + pathPrefix + "OcelotApp/OcelotApp/uploads/audio/{} ".format(sys.argv[1])
    + "-O " + pathPrefix + "OcelotApp/Temp.csv")

inpt = GetFeatures(pathPrefix + "OcelotApp/Temp.csv")

# CHANGE_PTP = False
# for x in range(len(inpt)):
#    if inpt[x] < MIN[x]:
#        CHANGE_PTP = True
#        MIN[x] = inpt[x]
#    if inpt[x] > MAX[x]:
#        CHANGE_PTP = True
#        MAX[x] = inpt[x]

# if CHANGE_PTP:
#     temp = [MAX[x] - MIN[x] for x in range(len(PTP))]
#     PTP = np.array(temp)
#     np.save("/home/ubuntu/OcelotApp/MIN.npy", MIN)
#     np.save("/home/ubuntu/OcelotApp/MAX.npy", MAX)
#     np.save("/home/ubuntu/OcelotApp/PTP.npy", PTP)

inptNorm = (inpt - MIN) / PTP

net = NetworkReader.readFrom(
    pathPrefix + 'OcelotApp/NN.pybrain.net.384-50.xml'
)

guess = net.activate(inptNorm)
result = np.array(guess)
returnValues = ""
for y, x in zip(result.argsort()[-3:][::-1], range(3)):
    if x == len(result.argsort()[-3:][::-1])-1:
        returnValues += "{}:{}".format(genres[y],
                                       float("{:2.3f}".format(result[y]*100)))
    else:
        returnValues += "{}:{},".format(genres[y],
                                        float("{:2.3f}".format(result[y]*100)))
print(returnValues)
