import tkinter as tk
from tkinter import ttk
from scipy.io import wavfile
from scipy.signal import stft, welch
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
# self.y is a one-dimensional arraself.y, self.y(t) corresponds to amplitude at t
# self.sr is the sampling rate
class Model:
    def __init__(self, y, sr):
        self.y = y
        self.sr = sr

    def load_audio(self, filename):
        # Load audio file using scipy's wavfile
        sr, y = wavfile.read(filename)
        # If stereo (2 channels), convert to mono (average both channels)            if len(y.shape) > 1:
        y = y.mean(axis=1)
        return y, sr

    def waveform_graph(self):
        # If the audio is stereo (2 channels), convert to mono (average both channels)
        if len(self.y.shape) > 1:
            self.y = self.y.mean(axis=1)
        time = np.linspace(0.,self.y.shape[0]/self.sr,self.y.shape[0])
        return self.y, time

    def find_resonance(self):
        freqs , power = welch(self.y, self.sr,nperseg=4096)
        dominant_frequency = freqs[np.argmax(power)]
        return dominant_frequency

    def find_length(self):
        numOfFrames = self.y.shape[0]
        duration = numOfFrames/self.sr
        return duration

    
    def target_freq(self,min, max, freqs):
        for x in freqs:
            if x < max and x > min:
                break
        return x

    def frequency_check(self, min, max):
        if len(self.y.shape) > 1:
            audio_data = self.y[:, 0]
        else:
            audio_data = self.y
        spectrum, freqs, t, im = plt.specgram(audio_data, Fs=self.sr, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        target_frequency = self.target_freq(min, max, freqs)
        index_of_frequency = np.where(freqs == target_frequency)[0][0]
        data_for_frequency = spectrum[index_of_frequency]
        data_in_db_fun = 10 * np.log10(data_for_frequency)
        return data_in_db_fun, t

    def find_nearest_value(self, array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    def Calculate_RT60(self,min,max):
        if len(self.y.shape) > 1:
            audio_data = self.y[:, 0]
        else:
            audio_data = self.y
        spectrum, freqs, t, im = plt.specgram(audio_data, Fs=self.sr, NFFT= 1024, cmap=plt.get_cmap('autumn_r'))
        data_in_db, __ = self.frequency_check(min, max)
        index_of_max = np.argmax(data_in_db)
        value_of_max = data_in_db[index_of_max]
        sliced_array = data_in_db[index_of_max:]
        value_of_max_less_5 = value_of_max - 5
        value_of_max_less_5 = self.find_nearest_value(sliced_array, value_of_max_less_5)
        index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)
        value_of_max_less_25 = value_of_max - 25
        value_of_max_less_25 = self.find_nearest_value(sliced_array, value_of_max_less_25)
        index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
        rt20 = t[index_of_max_less_5[0]] - t[index_of_max_less_25[0]]
        rt60 = 3 * rt20
        return rt60, index_of_max, index_of_max_less_5, index_of_max_less_25

    def find_difference(self):
        low_RT60, _, __, ___ = self.Calculate_RT60(0,1000)
        mid_RT60, _, __, ___ = self.Calculate_RT60( 1000, 5000)
        high_RT60, _, __, ___ = self.Calculate_RT60( 5000, 20000)
        avg_RT60 = (low_RT60 + mid_RT60 + high_RT60) / 3
        difference = avg_RT60 - .5
        return difference
