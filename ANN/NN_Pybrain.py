# Created by Marcello Martins on Feb 23, 2016
# Last modified on Mar 16, 2016
# Audio Ocelots Pybrain implementation of an ANN.

# @file NN_Pybrain.py

from pybrain.structure import RecurrentNetwork, FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer, TanhLayer
from pybrain.structure import FullConnection
from pybrain.datasets import SupervisedDataSet 
from pybrain.datasets import ClassificationDataSet
from pybrain.utilities import percentError
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import SoftmaxLayer
from pylab import ion, ioff, figure, draw, contourf, clf, show, hold, plot
from scipy import diag, arange, meshgrid, where
from numpy.random import multivariate_normal
from numpy import array_equal

DS = SupervisedDataSet.loadFromFile("DataSetComplete")

n = FeedForwardNetwork()
inLayer = LinearLayer(12)
hiddenLayer1 = SigmoidLayer(30)
hiddenLayer2 = SigmoidLayer(30)
outLayer = LinearLayer(8)
n.addInputModule(inLayer)
n.addModule(hiddenLayer1)
n.addModule(hiddenLayer2)
n.addOutputModule(outLayer)

in_to_hidden = FullConnection(inLayer, hiddenLayer1)
hidden_to_hidden = FullConnection(hiddenLayer1, hiddenLayer2)
hidden_to_out = FullConnection(hiddenLayer2, outLayer)
n.addConnection(in_to_hidden)
n.addConnection(hidden_to_hidden)
n.addConnection(hidden_to_out)
n.sortModules()

TrainDS, TestDS = DS.splitWithProportion(0.9)
fnn = buildNetwork( TrainDS.indim, 30, 30, TrainDS.outdim, outclass=SoftmaxLayer, bias=True, recurrent=True )
t = BackpropTrainer( fnn, dataset=TrainDS, learningrate = 0.0001, momentum = 0.99, verbose=True, weightdecay=0.01)

for epoch in range(0,15):
	t.train()

right, wrong = 0 , 0
for inpt, target in TestDS:
	guess = fnn.activate(inpt)
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
print("# right: {}, # wrong: {}".format(right, wrong))

# trnresult = percentError( trainer.testOnClassData(), TrainDS['target'] )
# tstresult = percentError( trainer.testOnClassData( dataset=TestDS ), TestDS['target'] )
# print "epoch: %4d" % trainer.totalepochs, \
# "train error: %5.2f%%" % trnresult, \
# "test error: %5.2f%%" % tstresult


