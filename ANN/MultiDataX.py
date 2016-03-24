# Created by Marcello Martins on Feb 14, 2016
# Last modified on Mar 23, 2016

# @file MultiDataX.py

from __future__ import print_function # Python 2/3 compatibility
import librosa
import os
import numpy as np
from scipy.cluster.vq import whiten
from multiprocessing import Process

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


def extractSongData(data, songList, folderName, prefix, answers, fileName):
	for song in songList:
		try:
			Data = np.vstack([Data, getData("{}{}/{}".format(prefix,folderName,song), answers)])
		except:
			print("ERROR ON SONG {}".format(song))
			pass
	try:
		np.save(fileName, Data)
		print("SAVED {}!".format(fileName))
	except:
		print("ERROR COUNLDN'T SAVE {}".format(fileName))
		pass


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

p10 = Process(target=extractSongData, args=((Data, hiphop[:500], "Hiphop-Samples", prefix, answers[0], "HiphopDataSet1.npy")))
p11 = Process(target=extractSongData, args=((Data, hiphop[500:1000], "Hiphop-Samples", prefix, answers[0], "HiphopDataSet2.npy")))
p12 = Process(target=extractSongData, args=((Data, hiphop[1000:1500], "Hiphop-Samples", prefix, answers[0], "HiphopDataSet3.npy")))
p13 = Process(target=extractSongData, args=((Data, hiphop[1500:2000], "Hiphop-Samples", prefix, answers[0], "HiphopDataSet4.npy")))

p20 = Process(target=extractSongData, args=((Data, jazz[:500], "Jazz-Samples", prefix, answers[1], "JazzDataSet1.npy")))
p21 = Process(target=extractSongData, args=((Data, jazz[500:1000], "Jazz-Samples", prefix, answers[1], "JazzDataSet2.npy")))
p22 = Process(target=extractSongData, args=((Data, jazz[1000:1500], "Jazz-Samples", prefix, answers[1], "JazzDataSet3.npy")))
p23 = Process(target=extractSongData, args=((Data, jazz[1500:2000], "Jazz-Samples", prefix, answers[1], "JazzDataSet4.npy")))

p30 = Process(target=extractSongData, args=((Data, classical[:500], "Classical-Samples", prefix, answers[2], "ClassicalDataSet1.npy")))
p31 = Process(target=extractSongData, args=((Data, classical[500:1000], "Classical-Samples", prefix, answers[2], "ClassicalDataSet2.npy")))
p32 = Process(target=extractSongData, args=((Data, classical[1000:1500], "Classical-Samples", prefix, answers[2], "ClassicalDataSet3.npy")))
p33 = Process(target=extractSongData, args=((Data, classical[1500:2000], "Classical-Samples", prefix, answers[2], "ClassicalDataSet4.npy")))

p40 = Process(target=extractSongData, args=((Data, country[:500], "Country-Samples", prefix, answers[3], "CountryDataSet1.npy")))
p41 = Process(target=extractSongData, args=((Data, country[500:1000], "Country-Samples", prefix, answers[3], "CountryDataSet2.npy")))
p42 = Process(target=extractSongData, args=((Data, country[1000:1500], "Country-Samples", prefix, answers[3], "CountryDataSet3.npy")))
p43 = Process(target=extractSongData, args=((Data, country[1500:2000], "Country-Samples", prefix, answers[3], "CountryDataSet4.npy")))

p50 = Process(target=extractSongData, args=((Data, dance[:500], "Dance-Samples", prefix, answers[4], "DanceDataSet1.npy")))
p51 = Process(target=extractSongData, args=((Data, dance[500:1000], "Dance-Samples", prefix, answers[4], "DanceDataSet2.npy")))
p52 = Process(target=extractSongData, args=((Data, dance[1000:1500], "Dance-Samples", prefix, answers[4], "DanceDataSet3.npy")))
p53 = Process(target=extractSongData, args=((Data, dance[1500:2000], "Dance-Samples", prefix, answers[4], "DanceDataSet4.npy")))

p60 = Process(target=extractSongData, args=((Data, metal[:500], "Metal-Samples", prefix, answers[5], "MetalDataSet1.npy")))
p61 = Process(target=extractSongData, args=((Data, metal[500:1000], "Metal-Samples", prefix, answers[5], "MetalDataSet2.npy")))
p62 = Process(target=extractSongData, args=((Data, metal[1000:1500], "Metal-Samples", prefix, answers[5], "MetalDataSet3.npy")))
p63 = Process(target=extractSongData, args=((Data, metal[1500:2000], "Metal-Samples", prefix, answers[5], "MetalDataSet4.npy")))

p70 = Process(target=extractSongData, args=((Data, reggae[:500], "Reggae-Samples", prefix, answers[6], "ReggaeDataSet1.npy")))
p71 = Process(target=extractSongData, args=((Data, reggae[500:1000], "Reggae-Samples", prefix, answers[6], "ReggaeDataSet2.npy")))
p72 = Process(target=extractSongData, args=((Data, reggae[1000:1500], "Reggae-Samples", prefix, answers[6], "ReggaeDataSet3.npy")))
p73 = Process(target=extractSongData, args=((Data, reggae[1500:2000], "Reggae-Samples", prefix, answers[6], "ReggaeDataSet4.npy")))

p80 = Process(target=extractSongData, args=((Data, rock[:500], "Rock-Samples", prefix, answers[7], "RockDataSet1.npy")))
p81 = Process(target=extractSongData, args=((Data, rock[500:1000], "Rock-Samples", prefix, answers[7], "RockDataSet2.npy")))
p82 = Process(target=extractSongData, args=((Data, rock[1000:1500], "Rock-Samples", prefix, answers[7], "RockDataSet3.npy")))
p83 = Process(target=extractSongData, args=((Data, rock[1500:2000], "Rock-Samples", prefix, answers[7], "RockDataSet4.npy")))

p10.start()
p11.start()
p12.start()
p13.start()
p20.start()
p21.start()
p22.start()
p23.start()
p30.start()
p31.start()
p32.start()
p33.start()
p40.start()
p41.start()
p42.start()
p43.start()
p50.start()
p51.start()
p52.start()
p53.start()
p60.start()
p61.start()
p62.start()
p63.start()
p70.start()
p71.start()
p72.start()
p73.start()
p80.start()
p81.start()
p82.start()
p83.start()

p10.join()
p11.join()
p12.join()
p13.join()
p20.join()
p21.join()
p22.join()
p23.join()
p30.join()
p31.join()
p32.join()
p33.join()
p40.join()
p41.join()
p42.join()
p43.join()
p50.join()
p51.join()
p52.join()
p53.join()
p60.join()
p61.join()
p62.join()
p63.join()
p70.join()
p71.join()
p72.join()
p73.join()
p80.join()
p81.join()
p82.join()
p83.join()