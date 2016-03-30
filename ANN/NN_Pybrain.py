# Created by Marcello Martins on Feb 23, 2016
# Last modified on Mar 16, 2016
# Audio Ocelots Pybrain implementation of an ANN.

# @file NN_Pybrain.py

from pybrain.structure import RecurrentNetwork, FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer, TanhLayer
from pybrain.structure import FullConnection
from pybrain.datasets import SupervisedDataSet, ClassificationDataSet
from pybrain.utilities import percentError
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import SoftmaxLayer, BiasUnit
from pylab import ion, ioff, figure, draw, contourf, clf, show, hold, plot
from scipy import diag, arange, meshgrid, where
from numpy.random import multivariate_normal
from numpy import array_equal
import pickle

DSSuperRaw = SupervisedDataSet.loadFromFile("Data/DSSuperRaw")
DSClassRaw = ClassificationDataSet.loadFromFile("Data/DSClassRaw")

DSSuperWhiten = SupervisedDataSet.loadFromFile("Data/DSSuperWhiten")
DSClassWhiten = ClassificationDataSet.loadFromFile("Data/DSClassWhiten")

DSSuperNorm = SupervisedDataSet.loadFromFile("Data/DSSuperNorm")
DSClassNorm = ClassificationDataSet.loadFromFile("Data/DSClassNorm")

layers = (14, 14, 8)

net = buildNetwork(*layers, hiddenclass=TanhLayer, bias=True, outputbias=True, outclass=SoftmaxLayer, recurrent=True)

TrainDS, TestDS = DSSuperNorm.splitWithProportion(0.7)

# TrainDS._convertToOneOfMany()
# TestDS._convertToOneOfMany()

t = BackpropTrainer( net, dataset=TrainDS, learningrate = 0.01, momentum = 0.01, verbose=True, weightdecay=0.0)

t.trainEpochs(50)

right, wrong = 0 , 0
for inpt, target in TestDS:
	guess = net.activate(inpt)
	maximum = max(guess)
	for x in range(8):
		if guess[x] == maximum:
			guess[x] = 1
		else:
			guess[x] = 0
	if array_equal(guess,target):
		right+=1
	else:
		wrong+=1

print("{}".format(float(right)/float(right+wrong)))

fileObject = open('NN.pybrain.net', 'w')

pickle.dump(net, fileObject)

fileObject.close()

# fileObject = open('NN.pybrain.net','r')

# net = pickle.load(fileObject)

########## OLD NN CODE ##########################

# n = FeedForwardNetwork()
# inLayer = LinearLayer(14)
# biasLayer1 = BiasUnit()
# biasLayer2 = BiasUnit()
# hiddenLayer1 = SigmoidLayer(65)
# # hiddenLayer2 = SigmoidLayer(30)
# # hiddenLayer3 = SigmoidLayer(30)
# outLayer = SoftmaxLayer(8)

# n.addInputModule(inLayer)
# n.addModule(hiddenLayer1)
# n.addModule(biasLayer1)
# n.addModule(biasLayer2)
# # n.addModule(hiddenLayer2)
# # n.addModule(hiddenLayer3)
# n.addOutputModule(outLayer)

# in_to_hidden = FullConnection(inLayer, hiddenLayer1)
# bias_to_hidden = FullConnection(biasLayer1, hiddenLayer1)
# bias_to_out = FullConnection(biasLayer2, outLayer)
# # hidden_to_hidden = FullConnection(hiddenLayer1, hiddenLayer2)
# # hidden_to_hidden2 = FullConnection(hiddenLayer2, hiddenLayer3)
# hidden_to_out = FullConnection(hiddenLayer1, outLayer)
# n.addConnection(in_to_hidden)
# n.addConnection(bias_to_hidden)
# n.addConnection(bias_to_out)
# # n.addConnection(hidden_to_hidden)
# # n.addConnection(hidden_to_hidden2)
# n.addConnection(hidden_to_out)
# n.sortModules()


