# Created by Marcello Martins on Feb 14, 2016
# Last modified on Mar 23, 2016
# Extract features/data from wav files and saves to SupervisedDataSet np array for testing

# @file data.py

import librosa
import numpy as np
from scipy.cluster.vq import whiten


# extract features/data from wav file and return as np.array
def getData(filename):
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

    raw = [avgSpectralContrast, avgMelSpectro, np.mean(y_harmonic), np.mean(y_percussive), np.mean(mfcc),
           np.mean(mfcc_delta), np.mean(beat_mfcc_delta), np.mean(chromagram), np.mean(beat_chroma),
           np.mean(beat_features), avgEnergy, tuning, zeroCrossings, tempo]
    # norm = [(float(i)-min(raw))/((max(raw)-min(raw))) for i in raw] # normalise numbers between -1 and 1
    return np.array([raw])


# Gets the data from whatever files name is passed in the command line,
# Usage Example: Python ExtractDataSingle.py /Path/To/Test.wav
# Just change this filename in the code to however the server gets the file
def extract(filename):
    wDataStack = np.load("ANN/Data/WhitenDataStack.npy")
    data = getData(filename)
    wDataStack = np.vstack([wDataStack, data])
    wDataStack = whiten(wDataStack)
    np.save("ANN/Data/WhitenDataStack.npy", wDataStack)
    wmin = np.argmin(wDataStack, axis=0)
    wmax = np.argmax(wDataStack, axis=0)
    dmin = []
    dmax = []
    for i, val in enumerate(wmin):
        dmin.append(wDataStack[val][i])
    for i, val in enumerate(wmax):
        dmax.append(wDataStack[val][i])
    for j in range(len(wDataStack[-1])):
        wDataStack[-1][j] = (wDataStack[-1][j] - dmin[j]) / (dmax[j] - dmin[j])
    print wDataStack[-1]
    return wDataStack[-1]  # <<-- This is the single normalized feature set to feed into the network.
