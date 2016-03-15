import librosa
import numpy as np


# extract features/data from wav file and return as np.array
def getData(filename):
    # why this hop_length?
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

    # zeroCrossings = np.sum(librosa.core.zero_crossings(y=y))
    avgMelSpectro = np.mean(librosa.feature.melspectrogram(y=y, sr=sr))

    avgSpectralContrast = np.mean(librosa.feature.spectral_contrast(S=S, sr=sr))

    # raw = np.array([[avgSpectralContrast, avgMelSpectro, np.mean(y_harmonic), np.mean(y_percussive), np.mean(mfcc),
    #                  np.mean(mfcc_delta), np.mean(beat_mfcc_delta), np.mean(chromagram), np.mean(beat_chroma),
    #                  np.mean(beat_features), avgEnergy, tuning]])

    raw = {avgSpectralContrast, avgMelSpectro, np.mean(y_harmonic), np.mean(y_percussive), np.mean(mfcc),
           np.mean(mfcc_delta), np.mean(beat_mfcc_delta), np.mean(chromagram), np.mean(beat_chroma),
           np.mean(beat_features), avgEnergy, tuning}

    norm = [float(i) / sum(raw) for i in raw]  # normalise numbers between -1 and 1

    data = {"avgSpectralContrast": norm[0], "avgMelSpectro": norm[1], "y_harmonic": norm[2], "y_percussive": norm[3],
            "mfcc": norm[4], "mfcc_delta": norm[5], "beat_mfcc_delta": norm[6], "chromagram": norm[7],
            "beat_chroma": norm[8], "beat_features": norm[9], "avgEnergy": norm[10], "tuning": norm[11]}

    return data
