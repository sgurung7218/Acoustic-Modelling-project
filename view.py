from tkinter import *
from tkinter import ttk,filedialog,messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import librosa
import librosa.display
import os
import sys
#from pydub import AudioSegment

#ONLY GRAPH BUTTON WORKS RIGHT NOW

class View(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)

        self.mainframe = ttk.Frame(self, padding='5 5 5 5 ')  # root is parent of frame
        self.mainframe.grid(row=0, column=0, sticky=("E", "W", "N", "S"))  # placed on first row,col of parent
        # frame can extend itself in all cardinal directions
        self._url_frame = ttk.LabelFrame(self.mainframe, text='File Path', padding='5 5 5 5')  # label frame
        self._url_frame.grid(row=0, column=0, sticky=("E", "W"))  # only expands E W
        self._url_frame.columnconfigure(0, weight=1)
        self._url_frame.rowconfigure(0, weight=1)  # behaves when resizing

        self._load_btn = ttk.Button(self._url_frame, text='Load file', command=self.searchfile)  # create button
        # fetch_url() is callback for button press
        self._load_btn.grid(row=0, column=1, sticky=W, padx=5)

        self._analyze_btn = ttk.Button(self._url_frame, text='Analyze', command=self.plt_graph)  # create button
        # fetch_url() is callback for button press
        self._analyze_btn.grid(row=0, column=2, sticky=W, padx=5)

        self._save_method = StringVar()
        self._save_method.set('img')
        self._img_only_radio = ttk.Radiobutton(self._url_frame, text='File is .wav', variable=self._save_method,
                                               value='img')
        self._img_only_radio.grid(row=1, column=0, padx=5, pady=2, sticky="W")
        self._img_only_radio.configure(state='normal')
        self._json_radio = ttk.Radiobutton(self._url_frame, text='Convert to .wav', variable=self._save_method,
                                           value='json')
        self._json_radio.grid(row=2, column=0, padx=5, pady=2, sticky="W")

        self._graph_frame = ttk.Frame(self.mainframe, padding="10")
        self._graph_frame.grid(row=1, column=0, padx=10, pady=10)
        self._graph_label = ttk.Label(self._graph_frame, text="Data analysis")
        self._graph_label.grid(row=0, column=0)
        # Create an initial empty plot
        fig, ax = plt.subplots(figsize=(6, 3))  # Create a blank figure and axis
        ax.set_title("Default Graph")
        ax.set_xlabel("Time(s)")
        ax.set_ylabel("Amplitude")
        ax.grid(True)
        fig.tight_layout()

        # Embed the initial empty plot into Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self._graph_frame)
        canvas.draw()  # Draw the empty plot
        canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=10)  # Add the canvas to the grid

        self._data_lbl = ttk.Label(self._graph_frame, text="Data")
        self._data_lbl.grid(row=2, column=0, padx=5, pady=5)

        self._btn_frame = ttk.Frame(self.mainframe, padding=(0, 10, 0, 0))
        self._btn_frame.grid(row=2, column=0)

        self._waveform_btn = ttk.Button(self._btn_frame, text='Waveform graph', command=self.plt_graph)  # create button
        # fetch_url() is callback for button press
        self._waveform_btn.grid(row=0, column=0, sticky=W, padx=5)

        self._intensity_btn = ttk.Button(self._btn_frame, text='Intensity Graph', command=self.intensity_graph)  # create button
        # fetch_url() is callback for button press
        self._intensity_btn.grid(row=0, column=1, sticky=W, padx=5)

        self._cycle_btn = ttk.Button(self._btn_frame, text='Cycle Frequency', command=self.funct3)  # create button
        # fetch_url() is callback for button press
        self._cycle_btn.grid(row=0, column=2, sticky=W, padx=5)

        self._comb_btn = ttk.Button(self._btn_frame, text='Combined', command=self.funct3)  # create button
        # fetch_url() is callback for button press
        self._comb_btn.grid(row=0, column=4, sticky=W, padx=5)

        self._quit_btn = ttk.Button(self.mainframe, text='Quit', command=self.quit)  # create button
        # exit program on press
        self._quit_btn.grid(row=2, column=0, sticky=("S","E"), padx=5)

        self._status_frame = ttk.Frame(self, relief='sunken', padding='2 2 2 2')
        self._status_frame.grid(row=1, column=0, sticky=("E", "W", "S",))
        self._status_msg = StringVar()  # need modified when update status text
        self._status_msg.set('Select a file to start...')
        self._status = ttk.Label(self._status_frame, textvariable=self._status_msg, anchor=W)
        self._status.grid(row=0, column=0, sticky=(E, W))

    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller

    def plt_graph(self):
        y, t = self.controller.data()
        for widget in self._graph_frame.winfo_children():
            widget.destroy()
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(t, y, label="Audio Signal")
        ax.set_title('Waveform graph')
        ax.set_xlabel('Time(s)')
        ax.set_ylabel('Amplitude')
        ax.grid(True, linestyle='--', color='gray', linewidth=0.5)
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self._graph_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=10)

    def intensity_graph(self):
        sample_rate, data = self.controller.rawdata()
        fig, ax = plt.subplots(figsize=(6,3))
        spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        cbar = fig.colorbar(im)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Frequency (Hz)')
        cbar.set_label('Intensity (dB)')
        canvas = FigureCanvasTkAgg(fig, master=self._graph_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=10)

    def searchfile(self):
        file = filedialog.askopenfile()
        if file == None:
            self.alert("Select a file")
        else:
            filename = os.path.basename(file.name)
            #filenameparts = os.path.splitext(filename)
            #filetype = filenameparts[1]

            """ #This doesn't work at the moment
            if filetype != ".wav":
                if filetype == ".m4a":
                    wav_filename = f"{filenameparts[0]}.wav"
                    sound = AudioSegment.from_file(filename, format="m4a")
                    filename = sound.export(wav_filename, format="wav")
                else:
                    self.alert("Unsupported file type")
            """

            sr, y = wavfile.read(f"{filename}")
            self.controller.remakemodel(y,sr)






        """
        mid_freq_data, sr = mm.calculate_mid_freq()
        for widget in self._graph_frame.winfo_children():
            widget.destroy()
        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(4, 2))
        # Plot the data
        librosa.display.specshow(mid_freq_data, sr=sr, x_axis='time', y_axis='log')
        # Set title and labels
        ax.set_title("Graph Plot")
        ax.set_xlabel("Amplitude")
        ax.set_ylabel("Time(s)")
        ax.grid(True, linestyle='--', color='gray', linewidth=0.5)
        # Embed the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self._graph_frame)  # Create canvas
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=10)
        """

    def funct3(self):
        print("funct3 test")

    def save(self):
        print("save test")

    def sb(self,msg):
        self._status_msg.set(msg)

    def alert(self,msg):
        messagebox.showinfo(message=msg)

    def quit(self):
        sys.exit()