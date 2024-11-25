import tkinter as tk
from tkinter import ttk
import librosa
import librosa.display
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from Menu import *
# y is a one-dimensional array, y(t) corresponds to amplitude at t
# sr is the sampling rate
y, sr = librosa.load("test_audio.wav")

def plt_graph(y , sr):
    plt.figure(figsize=(20,10))
    librosa.display.waveshow(y,sr=sr)
    plt.title('Waveform of the Audio')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.grid(True, linestyle = '--', color = 'gray', linewidth = 0.5)
    plt.show()

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

def display_mid_freq():
    frequency = librosa.stft(y)
    mid_freq_range = range(50, 1000)
    mid_freq_data = abs(frequency[mid_freq_range, :])
    # Clear the previous plot
    for widget in _img_frame.winfo_children():
        widget.destroy()
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(3,2))
    # Plot the data
    librosa.display.specshow(mid_freq_data, sr=sr, x_axis='time', y_axis='Amplitude')
    # Set title and labels
    ax.set_title("Graph Plot")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    # Add a legend
    ax.legend("Medium frequency")

    # Embed the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=_img_frame)  # Create canvas
    canvas.draw()
    canvas.get_tk_widget().grid(row=1,column=0,padx=0,pady=0)

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
    high_freq_data = abs(frequency[mid_freq_range,:])
