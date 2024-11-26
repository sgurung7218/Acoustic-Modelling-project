import tkinter as tk
from tkinter import ttk
from scipy.io import wavfile
from scipy.signal import stft
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from view import *
# y is a one-dimensional array, y(t) corresponds to amplitude at t
# sr is the sampling rate
sr, y = wavfile.read("test_audio.wav")

def freq_graph():
    D = stft(y)  # STFT of y
    s_db = np.abs(D)
    return s_db, sr

def compute_resonance(y,sr):
    #Computing Short-Time Fourier Transform (STFT)
    D = librosa.stft(y)
    #Convert to magnitude spectrogram (absolute value of STFT)
    magnitude, _ = librosa.magphase(D)
    #Compute average magnitude
    average_magnitude = np.mean(magnitude, axis=1)
    #Compute frequency bins for respective STFT
    frequencies = librosa.fft_frequencies(sr)
    #the maximum magnitude in average magnitude spectrum
    index_of_max_resonance = np.argmax(average_magnitude)
    highest_resonance = frequencies[index_of_max_resonance]
    return highest_resonance

def calculate_mid_freq():
    frequency = librosa.stft(y)
    mid_freq_range = range(50, 1000)
    mid_freq_data = abs(frequency[mid_freq_range, :])
    return mid_freq_data, sr

def compute_LMH(y,sr):
    frequency = librosa.stft(y)
    #finding the dimensions of matrix 'frequency' specifically the no. of rows
    numOfBins = frequency.shape[0]
    #Grouping frequency in ranges
    low_freq_range = range(0,50)
    mid_freq_range = range(50,1000)
    high_freq_range = range (1000,20000)
    #extracting data for each range
    low_freq_data = abs(frequency[low_freq_range,:])
    mid_freq_data = abs(frequency[mid_freq_range,:])
    high_freq_data = abs(frequency[high_freq_range,:])
