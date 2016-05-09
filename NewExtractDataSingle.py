from __future__ import print_function
from subprocess import call
import numpy as np
import csv

# audioPath = "/home/ubuntu/OcelotApp/uploads/audio/Country1.wav"
# tempPath = "/home/ubuntu/OcelotApp/uploads/audio/Temp.csv"
confPath = "/home/ubuntu/openSMILE/config/IS09_emotion.conf"
audioPath = "Country1.wav"
tempPath = "Temp.csv"
MIN = np.load("DataMin.npy")
PTP = np.load("DataPtp.npy")


def GetFeatures(path):
    with open(path,
              'rb') as genreFile:
        genreSamples = csv.reader(genreFile)
        floatSample = []
        sample = next(genreSamples)
        for feature in sample[1:385]:
            floatSample.append(float(feature))
        return np.array(floatSample)

open(tempPath, 'w').close()
call(["SMILExtract", "-C", confPath, "-I", audioPath, "-O", tempPath])

inpt = GetFeatures(audioPath)

inptNorm = (inpt - MIN) / PTP

print(inptNorm)
