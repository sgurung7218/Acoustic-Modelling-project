import librosa
import matplotlib.pyplot as plt
import numpy as np

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

def compute_frequency(y,sr):
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


