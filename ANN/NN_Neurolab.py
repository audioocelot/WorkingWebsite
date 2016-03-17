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
	print("# right: {}, # wrong: {}".format(right, wrong))

def run():
	# load data from storage
	print("Loading Data from storage...")
	DS = SupervisedDataSet.loadFromFile("DataSetComplete")
	TrainDS, TestDS = DS.splitWithProportion(0.8)


	# create network with 7 inputs, 15 neurons in hidden layer and 4 in output layer
	# define that the range of inputs will be from -1 to 1 and there will be 
	print("Setting up NN...")
	net = nl.net.newff([[-1, 1]]*12, [30, 8])

	# train the NN
	print("Training NN...")
	err = net.train(TrainDS['input'], TrainDS['target'], show=10, epochs=100, goal=0.001)

	# simulate the NN with the testing data
	print("Simulating NN...")
	ary = net.sim(TestDS['input'])

	# Display the miss rate for the testing data
	missRate(ary, TestDS['target'])

	# # save the NN for later use if needed
	# save = raw_input("Would you like to save this NN? ").lower()
	# if save == 'y' or save == 'yes':
	# 	name = raw_input("Please enter file name to save NN: ")
	# else:
	# 	runAgain = raw_input("Run again? ").lower()
	# 	if runAgain == 'y' or runAgain == 'yes':
	# 		run()
	# 	else:
	# 		print("NN.py Completed")

run()