# Created by Marcello Martins on Feb 14, 2016
# Last modified on Mar 23, 2016
# Extract features/data from wav files and saves to SupervisedDataSet np array for testing

# @file data.py

from __future__ import print_function # Python 2/3 compatibility
import librosa
import os
import numpy as np
from pybrain.datasets import SupervisedDataSet
from scipy.cluster.vq import whiten

prefix = "../" #Please set prefix to where ever your music is located on your local.

# help function to get songs in directory while ignoring system files such as .DS_Store
def listdir_nohidden(path):
	redir = []
	for f in os.listdir(path):
		if not f.startswith('.'):
			if "Icon" not in f:
				redir.append(f)
	return redir

# extract features/data from wav file and return as np.array
def getData(filename, answers):
	print("Gretting data for {}".format(filename))
	hop_length = 256;

	# Load the example clip
	y, sr = librosa.load(filename)

	# Short-time Fourier transform (STFT)
	S = np.abs(librosa.stft(y))

	# Separate harmonics and percussives into two waveforms
	y_harmonic, y_percussive = librosa.effects.hpss(y)

	# Beat track on the percussive signal
	tempo, beat_frames = librosa.beat.beat_track(y=y_percussive, sr=sr)

	# Compute MFCC features from the raw signal
	mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop_length, n_mfcc=13)

	# And the first-order differences (delta features)
	mfcc_delta = librosa.feature.delta(mfcc)

	# Stack and synchronize between beat events
	# This time, we'll use the mean value (default) instead of median
	beat_mfcc_delta = librosa.feature.sync(np.vstack([mfcc, mfcc_delta]), beat_frames)

	# Compute chroma features from the harmonic signal
	chromagram = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr)

	# Aggregate chroma features between beat events
	# We'll use the median value of each feature between beat frames
	beat_chroma = librosa.feature.sync(chromagram, beat_frames, aggregate=np.median)

	# Finally, stack all beat-synchronous features together
	beat_features = np.vstack([beat_chroma, beat_mfcc_delta])

	# Average the energy 
	avgEnergy = np.mean(librosa.feature.rmse(y=y))

	# Estimate tuning
	tuning = librosa.estimate_tuning(y=y, sr=sr)

	zeroCrossings = np.sum(librosa.core.zero_crossings(y=y))

	avgMelSpectro = np.mean(librosa.feature.melspectrogram(y=y, sr=sr))

	avgSpectralContrast = np.mean(librosa.feature.spectral_contrast(S=S, sr=sr))

	raw = [ avgSpectralContrast, avgMelSpectro, np.mean(y_harmonic), np.mean(y_percussive), np.mean(mfcc), np.mean(mfcc_delta), np.mean(beat_mfcc_delta), np.mean(chromagram), np.mean(beat_chroma), np.mean(beat_features), avgEnergy, tuning, zeroCrossings, tempo]
	#norm = [(float(i)-min(raw))/((max(raw)-min(raw))) for i in raw] # normalise numbers between -1 and 1
	return np.array([raw,answers]).reshape((1,2))

# create dataset for NN with 12 inputes and 4 outputs

# DS = SupervisedDataSet(12, 8)
# DS = SupervisedDataSet.loadFromFile("DataSet")
answers = [[1,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0],[0,0,1,0,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0],[0,0,0,0,0,1,0,0],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,1]]

Data = np.array([]).reshape((0,2))

# list of song names on my computer by genre
hiphop = listdir_nohidden("{}Hiphop-Samples".format(prefix))
jazz = listdir_nohidden("{}Jazz-Samples".format(prefix))
classical = listdir_nohidden("{}Classical-Samples".format(prefix))
country = listdir_nohidden("{}Country-Samples".format(prefix))
dance = listdir_nohidden("{}Dance-Samples".format(prefix))
metal = listdir_nohidden("{}Metal-Samples".format(prefix))
reggae = listdir_nohidden("{}Reggae-Samples".format(prefix))
rock = listdir_nohidden("{}Rock-Samples".format(prefix))

for song in hiphop:
	try:
		Data = np.vstack([Data, getData("{}Hiphop-Samples/{}".format(prefix,song), answers[0])])
	except:
		print("ERROR ON SONG {}".format(song))
		pass
for song in jazz:
	try:
		Data = np.vstack([Data, getData("{}Jazz-Samples/{}".format(prefix,song), answers[1])])
	except:
		print("ERROR ON SONG {}".format(song))
		pass
for song in classical:
	try:
		Data = np.vstack([Data, getData("{}Classical-Samples/{}".format(prefix,song), answers[2])])
	except:
		print("ERROR ON SONG {}".format(song))
		pass
for song in country:
	try:
		Data = np.vstack([Data, getData("{}Country-Samples/{}".format(prefix,song), answers[3])])
	except:
		print("ERROR ON SONG {}".format(song))
		pass
for song in dance:
	try:
		Data = np.vstack([Data, getData("{}Dance-Samples/{}".format(prefix,song), answers[4])])
	except:
		print("ERROR ON SONG {}".format(song))
		pass
for song in metal:
	try:
		Data = np.vstack([Data, getData("{}Metal-Samples/{}".format(prefix,song), answers[5])])
	except:
		print("ERROR ON SONG {}".format(song))
		pass
for song in reggae:
	try:
		Data = np.vstack([Data, getData("{}Reggae-Samples/{}".format(prefix,song), answers[6])])
	except:
		print("ERROR ON SONG {}".format(song))
		pass
for song in rock:
	try:
		Data = np.vstack([Data, getData("{}Rock-Samples/{}".format(prefix,song), answers[7])])
	except:
		print("ERROR ON SONG {}".format(song))
		pass

# np.save("CompleteRawDataSet.npy", Data)


# tdata = np.array([]).reshape(0,12)
# for i in range(5):
# 	tdata = np.vstack([tdata, Data[i][0]])
# tdata = whiten(tdata)
# print(tdata)
# print(np.argmin(tdata, axis=0))

#DS.saveToFile("DataSetComplete")