import tkinter as tk
from tkinter import ttk
from scipy.io import wavfile
from scipy.signal import stft
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
# self.y is a one-dimensional arraself.y, self.y(t) corresponds to amplitude at t
# self.sr is the sampling rate
class Model:
    def __init__(self, y, sr):
        self.y = y
        self.sr = sr
    def waveform_graph(self):
        # If the audio is stereo (2 channels), convert to mono (average both channels)
        if len(self.y.shape) > 1:
            self.y = self.y.mean(axis=1)
        time = np.linspace(0.,self.y.shape[0]/self.sr,self.y.shape[0])
        return self.y, time
    
    def compute_resonance(self):
        #Computing Short-Time Fourier Transform (STFT)
        D = librosa.stft(self.y)
        #Convert to magnitude spectrogram (absolute value of STFT)
        magnitude, _ = librosa.magphase(D)
        #Compute average magnitude
        average_magnitude = np.mean(magnitude, axis=1)
        #Compute frequencself.y bins for respective STFT
        frequencies = librosa.fft_frequencies(self.sr)
        #the maximum magnitude in average magnitude spectrum
        index_of_max_resonance = np.argmax(average_magnitude)
        highest_resonance = frequencies[index_of_max_resonance]
        return highest_resonance
    
    def calculate_mid_freq(self):
        frequencself.y = librosa.stft(self.y)
        mid_freq_range = range(50, 1000)
        mid_freq_data = abs(frequencself.y[mid_freq_range, :])
        return mid_freq_data, self.sr
    
    def compute_LMH(self):
        frequencself.y = librosa.stft(self.y)
        #finding the dimensions of matrix 'frequencself.y' specificallself.y the no. of rows
        numOfBins = frequencself.y.shape[0]
        #Grouping frequencself.y in ranges
        low_freq_range = range(0,50)
        mid_freq_range = range(50,1000)
        high_freq_range = range (1000,20000)
        #extracting data for each range
        low_freq_data = abs(frequencself.y[low_freq_range,:])
        mid_freq_data = abs(frequencself.y[mid_freq_range,:])
        high_freq_data = abs(frequencself.y[high_freq_range,:])
