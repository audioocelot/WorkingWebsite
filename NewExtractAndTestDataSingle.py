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

MIN = np.load("/home/ubuntu/OcelotApp/MIN.npy")
MAX = np.load("/home/ubuntu/OcelotApp/MAX.npy")
PTP = np.load("/home/ubuntu/OcelotApp/PTP.npy")

open("/home/ubuntu/OcelotApp/Temp.csv", 'w').close()
rd = os.system(
    "sudo /home/ubuntu/openSMILE/inst/bin/SMILExtract "
    + "-C /home/ubuntu/openSMILE/config/IS09_emotion.conf "
    + "-I /home/ubuntu/OcelotApp/OcelotApp/uploads/audio/{} ".format(sys.argv[1])
    + "-O /home/ubuntu/OcelotApp/Temp.csv")

inpt = GetFeatures("/home/ubuntu/OcelotApp/Temp.csv")

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
    '/home/ubuntu/OcelotApp/NN.pybrain.net.384-250.xml'
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
