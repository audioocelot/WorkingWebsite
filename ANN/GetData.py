# Created by Marcello Martins on Feb 14, 2016
# Last modified on Feb 15, 2016
# Extract features/data from wav files and save to numpy array for testing

# @file data.py 

import librosa
import os
import numpy as np

# help function to get songs in directory while ignoring system files such as .DS_Store
def listdir_nohidden(path):
	redir = []
	for f in os.listdir(path):
		if not f.startswith('.'):
			redir.append(f)
	return redir

# extract features/data from wav file and return as np.array
def getData(filename):
	print("Gretting data for{}".format(filename))
	y, sr = librosa.load(filename) # load song
	S = np.abs(librosa.stft(y))
	avgEnergy = np.mean(librosa.feature.rmse(y=y))
	tuning = librosa.estimate_tuning(y=y, sr=sr)
	tempo = librosa.beat.estimate_tempo(librosa.onset.onset_strength(y, sr=sr), sr=sr)
	# zeroCrossings = np.sum(librosa.core.zero_crossings(y=y))
	avgChroma = np.mean(librosa.feature.chroma_stft(y=y, sr=sr))
	avgMelSpectro = np.mean(librosa.feature.melspectrogram(y=y, sr=sr))
	avgMFCC = np.mean(librosa.feature.mfcc(y=y, sr=sr))
	avgSpectralContrast = np.mean(librosa.feature.spectral_contrast(S=S, sr=sr))
	raw = [avgEnergy, tuning, tempo, avgChroma, avgMelSpectro, avgMFCC, avgSpectralContrast]
	norm = [float(i)/sum(raw) for i in raw] # normalise numbers between -1 and 1
	return np.array([norm])

# fill array with content to teach NN
def fillLearningData(generes, genreOrder, numRange, data):
	for key, value in generes.iteritems():
		genreOrder = np.append(genreOrder,key)
		for files in value[0:numRange]:
			data = np.vstack([data,getData("../genres/{}/{}".format(key, files))])
	return data, genreOrder

# fill array with content to test NN
def fillTestingData(generes, genreOrder, numRange, data):
	for key, value in generes.iteritems():
		genreOrder = np.append(genreOrder,key)
		for files in value[numRange:]:
			data = np.vstack([data,[getData("../genres/{}/{}".format(key, files))],[answers[0]]])
	return data, genreOrder

# create empty array to hold learningData set and testingDvata set
Data = np.array([]).reshape(0,2)

# create empty array to hold answersData for four generes
answers = [[1,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0],[0,0,1,0,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0],[0,0,0,0,0,1,0,0],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,1]]


# fill data sets with 80 songs for learning and 20 for testing
Data = fillLearningData(generes, learningGenreOrder, 80, learningData)

# save data for permanent storage
np.save("learningGenreOrder.npy", learningGenreOrder)
np.save("testingGenreOrder.npy", testingGenreOrder)
np.save("learningData.npy", learningData)
np.save("answersData.npy", answersData)
np.save("testingData.npy", testingData)

print("data.py Completed")
