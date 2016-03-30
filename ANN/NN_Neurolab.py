# Created by Marcello Martins on Feb 14, 2016
# Last modified on Mar 16, 2016
# Create NN and teach it with data collected from @file data.py

# @file NN_Neurolab.py
import itertools
import numpy as np
import neurolab as nl
from pybrain.datasets import SupervisedDataSet 

# function to quickly display the errors for testingData
def missRate(ary, target):
	right, wrong = 0 , 0
	for guess, answer in itertools.izip(ary,target):
		maximum = max(guess)
		for x in range(8):
			if guess[x] == maximum:
				guess[x] = 1
			else:
				guess[x] = 0
		if np.array_equal(guess,answer):
			right+=1
		else:
			wrong+=1
	print("--------------------RESULTS--------------------")
	print("\t# right: {}, # wrong: {}".format(right, wrong))
	print("\tError rate: {}".format(float(right)/(float(right)+float(wrong))))
	print("----------------------END----------------------")


def run(layers, show, epochs):
	# load data from storage
	print("Loading Data from storage...")
	DS = SupervisedDataSet.loadFromFile("Data/DSSuperNorm")
	TrainDS, TestDS = DS.splitWithProportion(0.7)

	for _, target in TrainDS:
		for x in range(8):
			if target[x] == 1:
				target[x] = .9
			else:
				target[x] = .1

	for _, target in TestDS:
		for x in range(8):
			if target[x] == 1:
				target[x] = .9
			else:
				target[x] = .1

	# create network with 7 inputs, 15 neurons in hidden layer and 4 in output layer
	# define that the range of inputs will be from -1 to 1 and there will be 
	print("Setting up NN...")
	net = nl.net.newff(nl.tool.minmax(TestDS['input']), layers)

	net.layers[-1].transf = nl.trans.SoftMax()


	# train the NN
	print("Training NN...")
	err = net.train(TestDS['input'], TestDS['target'], show=show, epochs=epochs, goal=0.000000000001)


	ary = net.sim(TrainDS['input'])


	# Display the miss rate for the testing data
	return missRate(ary, TrainDS['target'])

	# save the NN for later use if needed

	# save = raw_input("Would you like to save this NN? ").lower()
	# if save == 'y' or save == 'yes':
	# 	name = raw_input("Please enter file name to save NN: ")
	# else:
	# 	runAgain = raw_input("Run again? ").lower()
	# 	if runAgain == 'y' or runAgain == 'yes':
	# 		run()
	# 	else:
	# 		print("NN.py Completed")

run([11, 8], 5, 25)
# bestrate = 0
# for x in range(10)
# 	net, rate = run([60, 8], 25, 500)
# 	if rate > bestrate:
# 		bestrate = rate
# 		print("new best rate is: {}".format(rate))
# 		net.save('best.net')