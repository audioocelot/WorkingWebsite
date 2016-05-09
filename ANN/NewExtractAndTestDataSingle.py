from __future__ import print_function
from subprocess import call
from numpy import array_equal
import numpy as np
import csv
import pickle


def GetFeatures(path):
    with open(path,
              'rb') as genreFile:
        genreSamples = csv.reader(genreFile)
        floatSample = []
        sample = next(genreSamples)
        for feature in sample[1:385]:
            floatSample.append(float(feature))
        return np.array(floatSample)

audioPath = "/home/ubuntu/OcelotApp/uploads/audio/Country11.wav"
tempPath = "/home/ubuntu/OcelotApp/uploads/audio/Temp.csv"
confPath = "/home/ubuntu/openSMILE/config/IS09_emotion.conf"

# audioPath = "Jazz11.wav"
# tempPath = "Temp.csv"
# confPath = "/Users/SimplyMarcello/openSMILE/config/IS09_emotion.conf"

answers = {"Classical": [1, 0, 0, 0, 0, 0, 0, 0],
           "Country": [0, 1, 0, 0, 0, 0, 0, 0],
           "Dance": [0, 0, 1, 0, 0, 0, 0, 0],
           "Hiphop": [0, 0, 0, 1, 0, 0, 0, 0],
           "Jazz": [0, 0, 0, 0, 1, 0, 0, 0],
           "Metal": [0, 0, 0, 0, 0, 1, 0, 0],
           "Reggae": [0, 0, 0, 0, 0, 0, 1, 0],
           "Rock": [0, 0, 0, 0, 0, 0, 0, 1]}

answers2 = ["Classical", "Country", "Dance", "Hiphop",
            "Jazz", "Metal", "Reggae", "Rock"]

MIN = np.load("MIN.npy")
MAX = np.load("MAX.npy")
PTP = np.load("PTP.npy")

open("/home/ubuntu/OcelotApp/uploads/audio/Temp.csv", 'w').close()
call(["/home/ubuntu/openSMILE/SMILExtract", "C", "/home/ubuntu/openSMILE/config/IS09_emotion.conf", "-I", "/home/ubuntu/OcelotApp/uploads/audio/test.wav", "-O", "/home/ubuntu/OcelotApp/uploads/audio/Temp.csv"])

inpt = GetFeatures(tempPath)

CHANGE_PTP = False
for x in range(len(inpt)):
    if inpt[x] < MIN[x]:
        CHANGE_PTP = True
        print("#{}\t{} < {}".format(x, inpt[x], MIN[x]))
        MIN[x] = inpt[x]
        print("CHANGED MIN TO: {}".format(MIN[x]))
    if inpt[x] > MAX[x]:
        CHANGE_PTP = True
        print("{}\t{} > {}".format(x, inpt[x], MAX[x]))
        MAX[x] = inpt[x]
        print("CHANGED MAX TO: {}".format(MAX[x]))

if CHANGE_PTP:
    temp = [MAX[x] - MIN[x] for x in range(len(PTP))]
    PTP = np.array(temp)
    np.save("MIN.npy", MIN)
    np.save("MAX.npy", MAX)
    np.save("PTP.npy", PTP)

inptNorm = (inpt - MIN) / PTP

fileObject = open('NN.pybrain.net.384-50', 'r')

net = pickle.load(fileObject)

guess = net.activate(inptNorm)

AA = np.array(guess)
for y in AA.argsort()[-3:][::-1]:
    print("{}: {:2.2f}%".format(answers2[y], guess[y]*100))
print("")
