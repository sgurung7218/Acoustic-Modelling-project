import librosa
import matplotlib.pyplot as plt
import numpy as np

# 1. Get the file path to an included audio example
filename = librosa.example('nutcracker')


# y is a one-dimensional array, y(t) corresponds to amplitude at t
# sr is the sampling rate
y, sr = librosa.load(filename)

def plt_graph(y , sr):
    plt.figure(figsize=(20,10))

    librosa.display.waveshow(y,sr=sr)
    plt.title('Waveform of the Audio')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.grid(True, linestyle = '--', color = 'gray', linewidth = 0.5)
    plt.show()

