import os
import shutil
import tkinter as tk
from tkinter import ttk,filedialog,messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
from pydub import AudioSegment


#ONLY GRAPH BUTTON WORKS RIGHT NOW

class View(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)

        self.fileNameLabel = None
        self.mainframe = ttk.Frame(self, padding='5 5 5 5 ')  # root is parent of frame
        self.mainframe.grid(row=0, column=0, sticky=("E", "W", "N", "S"))  # placed on first row,col of parent
        # frame can extend itself in all cardinal directions
        self._url_frame = ttk.LabelFrame(self.mainframe, text='File Path', padding='5 5 5 5')  # label frame
        self._url_frame.grid(row=0, column=0, sticky=("E", "W"))  # only expands E W
        self._url_frame.columnconfigure(0, weight=1)
        self._url_frame.rowconfigure(0, weight=1)  # behaves when resizing

        self._load_btn = ttk.Button(self._url_frame, text='Load file', command=self.load_audio)  # create button
        # fetch_url() is callback for button press
        self._load_btn.grid(row=0, column=1, sticky="W", padx=5)

        # Create a Label to display the filename below the button
        self.fileNameLabel = ttk.Label(self._url_frame, text="No file loaded")
        self.fileNameLabel.grid(row=1, column=1, sticky='W', padx=5)

        self._analyze_btn = ttk.Button(self._url_frame, text='Analyze', command=self.plt_graph)  # create button
        # fetch_url() is callback for button press
        self._analyze_btn.grid(row=0, column=2, sticky="W", padx=5)

        self._graph_frame = ttk.Frame(self.mainframe, padding="10")
        self._graph_frame.grid(row=1, column=0, padx=10, pady=1)
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

        self._btn_frame = ttk.Frame(self.mainframe, padding=(0, 10, 0, 0))
        self._btn_frame.grid(row=2, column=0)

        self._data_lbl = ttk.Frame(self._btn_frame, padding="10")
        self._data_lbl.grid(row=0, column=0, sticky="E")

        self.length_box = tk.Text(self._data_lbl, height=1, width=40)
        self.length_box.grid(row=0,column=0)
        self.length_box.insert(tk.END,"File Length = 0s")
        self.frequency_box = tk.Text(self._data_lbl, height=1, width=40)
        self.frequency_box.grid(row=1,column=0,)
        self.frequency_box.insert(tk.END,"Resonance Frequency=___Hz")
        self.difference_box = tk.Text(self._data_lbl, height=1, width=40)
        self.difference_box.grid(row=2,column=0,)
        self.difference_box.insert(tk.END,"Difference=__.__s")


        self._waveform_btn = ttk.Button(self._btn_frame, text='Waveform graph', command=self.plt_graph)  # create button
        self._waveform_btn.grid(row=0, column=1, sticky="W", padx=5)

        self._intensity_btn = ttk.Button(self._btn_frame, text='Intensity Graph', command=self.intensity_graph)  # create button
        self._intensity_btn.grid(row=0, column=2, sticky="W", padx=5)

        self._toggle_btn = ttk.Button(self._btn_frame, text='Cycle RT60 graph', command=self.toggle)  # create button
        self._toggle_btn.grid(row=0, column=3, sticky="W", padx=5)

        self._comb_btn = ttk.Button(self._btn_frame, text='Combined RT60 Graph', command=self.combined)  # create button
        self._comb_btn.grid(row=0, column=6, sticky="W", padx=5)

        self._status_frame = ttk.Frame(self, relief='sunken', padding='2 2 2 2')
        self._status_frame.grid(row=1, column=0, sticky=("E", "W", "S",))
        self._status_msg = tk.StringVar()  # need modified when update status text
        self._status_msg.set('Type a file path to select a file...')
        self._status = ttk.Label(self._status_frame, textvariable=self._status_msg, anchor="w")
        self._status.grid(row=0, column=0, sticky=("E", "W"))

    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller
    def plt_graph(self):
        y, t = self.controller.data()
        freq, Time, Difference = self.controller.analysis()
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
        self.length_box.delete(1.0, tk.END)
        self.frequency_box.delete(1.0, tk.END)
        self.difference_box.delete(1.0, tk.END)
        self.length_box.insert(tk.END,f"File Length = {Time:.2f}s")
        self.frequency_box.insert(tk.END,f"Resonant Frequency = {freq:.2f}Hz")
        self.difference_box.insert(tk.END,f"Difference={Difference[0]:.2f}s")

    def intensity_graph(self):
        for widget in self._graph_frame.winfo_children():
            widget.destroy()
        sample_rate, data = self.controller.rawdata()
        fig, ax = plt.subplots(figsize=(6,3))
        spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        cbar = fig.colorbar(im)
        ax.set_title('Frequency graph')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Frequency (Hz)')
        cbar.set_label('Intensity (dB)')
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self._graph_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=10)

    def low_freq(self):
        for widget in self._graph_frame.winfo_children():
            widget.destroy()
        data_in_db, t = self.controller.frequency_check(0, 1000)
        RT60, index_of_max, index_of_max_less_5, index_of_max_less_25= self.controller.Calculate_RT60(0,1000)
        fig, ax = plt.subplots(figsize=(6,3))
        plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color='y')
        ax.set_title('Low RT60 graph')
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Power (dB)")
        plt.plot(t[index_of_max], data_in_db[index_of_max], 'go')
        plt.plot(t[index_of_max_less_5[0]], data_in_db[index_of_max_less_5[0]], 'bo')
        plt.plot(t[index_of_max_less_25[0]], data_in_db[index_of_max_less_25[0]], 'ro')
        fig.tight_layout()
        ax.grid(True, linestyle='--', color='gray', linewidth=0.5)
        canvas = FigureCanvasTkAgg(fig, master=self._graph_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1,column=0, padx=10, pady=10)

    def mid_freq(self):
        for widget in self._graph_frame.winfo_children():
            widget.destroy()
        data_in_db, t = self.controller.frequency_check(1000,5000)
        RT60, index_of_max, index_of_max_less_5, index_of_max_less_25= self.controller.Calculate_RT60(1000,5000)
        fig, ax = plt.subplots(figsize=(6,3))
        plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color='pink')
        ax.set_title('Mid RT60 graph')
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Power (dB)")
        plt.plot(t[index_of_max], data_in_db[index_of_max], 'go')
        plt.plot(t[index_of_max_less_5[0]], data_in_db[index_of_max_less_5[0]], 'bo')
        plt.plot(t[index_of_max_less_25[0]], data_in_db[index_of_max_less_25[0]], 'ro')
        fig.tight_layout()
        ax.grid(True, linestyle='--', color='gray', linewidth=0.5)
        canvas = FigureCanvasTkAgg(fig, master=self._graph_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1,column=0, padx=10, pady=10)

    def high_freq(self):
        for widget in self._graph_frame.winfo_children():
            widget.destroy()
        data_in_db, t = self.controller.frequency_check(5000,20000)
        RT60, index_of_max, index_of_max_less_5, index_of_max_less_25= self.controller.Calculate_RT60(5000,20000)
        fig, ax = plt.subplots(figsize=(6,3))
        plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color='b')
        ax.set_title('High RT60 graph')
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Power (dB)")
        plt.plot(t[index_of_max], data_in_db[index_of_max], 'go')
        plt.plot(t[index_of_max_less_5[0]], data_in_db[index_of_max_less_5[0]], 'bo')
        plt.plot(t[index_of_max_less_25[0]], data_in_db[index_of_max_less_25[0]], 'ro')
        fig.tight_layout()
        ax.grid(True, linestyle='--', color='gray', linewidth=0.5)
        canvas = FigureCanvasTkAgg(fig, master=self._graph_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1,column=0, padx=10, pady=10)

    def toggle(self):
        global toggle
        if (toggle == 0):
            self.low_freq()
        elif (toggle == 1):
            self.mid_freq()
        elif (toggle == 2):
            self.high_freq()
        toggle = (toggle+1)%3
    def combined(self):
        low_data_in_db, low_t = self.controller.frequency_check(0, 1000)
        low_RT60, low_index_of_max, low_index_of_max_less_5, low_index_of_max_less_25 = self.controller.Calculate_RT60(0, 1000)
        mid_data_in_db, mid_t = self.controller.frequency_check(1000, 5000)
        mid_RT60, mid_index_of_max, mid_index_of_max_less_5, mid_index_of_max_less_25 = self.controller.Calculate_RT60(1000, 5000)
        high_data_in_db, high_t = self.controller.frequency_check(5000, 20000)
        high_RT60, high_index_of_max, high_index_of_max_less_5, high_index_of_max_less_25 = self.controller.Calculate_RT60(5000, 20000)
        for widget in self._graph_frame.winfo_children():
            widget.destroy()
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(low_t, low_data_in_db, linewidth=1, alpha=0.7, color='y', label='low frequency')
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Power (dB)")
        ax.plot(low_t[low_index_of_max], low_data_in_db[low_index_of_max], 'go')
        ax.plot(low_t[low_index_of_max_less_5[0]], low_data_in_db[low_index_of_max_less_5[0]], 'bo')
        ax.plot(low_t[low_index_of_max_less_25[0]], low_data_in_db[low_index_of_max_less_25[0]], 'ro')

        ax.plot(mid_t, mid_data_in_db, linewidth=1, alpha=0.7, color='pink', label='mid frequency')
        ax.plot(mid_t[mid_index_of_max], mid_data_in_db[mid_index_of_max], 'go')
        ax.plot(mid_t[mid_index_of_max_less_5[0]], mid_data_in_db[mid_index_of_max_less_5[0]], 'bo')
        ax.plot(mid_t[mid_index_of_max_less_25[0]], mid_data_in_db[mid_index_of_max_less_25[0]], 'ro')

        ax.plot(high_t, high_data_in_db, linewidth=1, alpha=0.7, color='b', label='high frequency')
        ax.plot(high_t[high_index_of_max], high_data_in_db[high_index_of_max], 'go')
        ax.plot(high_t[high_index_of_max_less_5[0]], high_data_in_db[high_index_of_max_less_5[0]], 'bo')
        ax.plot(high_t[high_index_of_max_less_25[0]], high_data_in_db[high_index_of_max_less_25[0]], 'ro')
        ax.set_title('Combined RT60 graph')
        fig.tight_layout()
        ax.grid(True, linestyle='--', color='gray', linewidth=0.5)
        ax.legend()
        canvas = FigureCanvasTkAgg(fig, master=self._graph_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=10)

    import os

    def load_audio(self):
        """A simple function to load the file and check if conversion is needed."""
        # Check if 'testsound.wav' exists in the project's main directory
        project_dir = os.getcwd()  # Get the current working directory
        test_sound_path = os.path.join(project_dir, 'testsound.wav')

        if os.path.exists(test_sound_path):
            os.remove(test_sound_path)  # Delete the file if it exists

        # Proceed as usual to load the file
        self.filePath = filedialog.askopenfilename(title="Select an audio file")
        if not self.filePath:
            return

        # Update the label to show the loaded filename
        self.fileNameLabel.config(text=f"Loaded: {os.path.basename(self.filePath)}")

        # If the file isn't already a WAV, convert it
        if not self.filePath.lower().endswith('.wav'):
            self.convert_to_wav()  # Convert the file if it's not a WAV
        else:
            # If it's already a WAV, rename it and save to the project folder
            self.rename_wav_file()

    def convert_to_wav(self):
            """Convert the audio file to WAV if necessary."""
            if not self.filePath:
                messagebox.showerror("Error", "No audio file loaded.")
                return

            try:
                newFilename = self.convert_to_wav_helper(self.filePath)
                if newFilename:
                    self.fileNameLabel.config(text=f"Converted to WAV: {os.path.basename(newFilename)}")
                    messagebox.showinfo("Success", f"File converted and saved to {newFilename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to convert file: {str(e)}")

    def rename_wav_file(self):
        """Copy the already WAV file to testsound.wav and save it in the project directory."""
        try:
            # Get the current directory and the new filename
            current_dir = os.path.dirname(os.path.realpath(__file__))
            newFilename = os.path.join(current_dir, "testsound.wav")

            # Copy the file to the new location with the new name
            shutil.copy(self.filePath, newFilename)
            self.filePath = newFilename  # Update the file path to the new file
            self.fileNameLabel.config(text=f"Copied to: {os.path.basename(newFilename)}")
            messagebox.showinfo("Success", f"File copied and saved to {newFilename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy WAV file: {str(e)}")

    @staticmethod
    def convert_to_wav_helper(filename):
            """Changing the file to WAV and saving it as 'testsound.wav' in the current directory."""
            try:
                print(f"Importing {filename}...")

                # Load the audio file using pydub
                audio = AudioSegment.from_file(filename)

                # Get the current directory and append the new file name
                current_dir = os.path.dirname(os.path.realpath(__file__))
                newFilename = os.path.join(current_dir, "testsound.wav")

                print(f"Converting {filename} to {newFilename}...")

                # Export the audio as WAV to the new filename
                audio.export(newFilename, format="wav")
                print(f"Conversion complete: {newFilename}")
                return newFilename
            except Exception as e:
                raise ValueError(f"Could not process the file: {str(e)}")

    def funct3(self):
        print("funct3 test")

    def save(self):
        print("save test")

    def sb(self,msg):
        self._status_msg.set(msg)

    def alert(self,msg):
        messagebox.showinfo(message=msg)

toggle = 0 #do not remove, used to cycle RT60