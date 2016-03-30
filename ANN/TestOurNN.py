from __future__ import print_function # Python 2/3 compatibility
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


DSSuperNorm = SupervisedDataSet.loadFromFile("Data/DSSuperNorm")

fileObject = open('NN.pybrain.net','r')

net = pickle.load(fileObject)

TrainDS, TestDS = DSSuperNorm.splitWithProportion(0.99)

for inpt, target in TestDS:
	sum = 0
	guess = net.activate(inpt)
	print("Hiphop\t  Jazz\t\tClassical\t\tCountry\t\tDance\t\tMetal\t\tReggae\t\tRock")
	for x in guess:
		sum += x
		print("{0:.6f}".format(x), end=' ')
	print("-> {}".format(target))
	print("'\n")
