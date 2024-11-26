from tkinter import *
from tkinter import ttk,filedialog,messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
import model as mm
import librosa
import librosa.display

#ONLY GRAPH BUTTON WORKS RIGHT NOW

def plt_graph():
    y, sr = mm.freq_graph()
    for widget in _img_frame.winfo_children():
        widget.destroy()
    frequencies = librosa.fft_frequencies(sr=sr)
    fig, ax=plt.subplots(figsize=(5,3))
    ax.plot(y, sr)
    ax.set_title('Waveform of the Audio')
    ax.set_xlabel('Time(s)')
    ax.set_ylabel('Amplitude')
    ax.grid(True, linestyle = '--', color = 'gray', linewidth = 0.5)
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=_img_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1,column=0,padx=10,pady=10)

def funct1():
    print("funct1 test")


def funct2():
    mid_freq_data, sr = mm.calculate_mid_freq()
    for widget in _img_frame.winfo_children():
        widget.destroy()
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(4,2))
    # Plot the data
    librosa.display.specshow(mid_freq_data, sr=sr, x_axis='time', y_axis='log')
    # Set title and labels
    ax.set_title("Graph Plot")
    ax.set_xlabel("Amplitude")
    ax.set_ylabel("Time(s)")
    ax.grid(True, linestyle = '--', color = 'gray', linewidth = 0.5)
    # Embed the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=_img_frame)  # Create canvas
    canvas.draw()
    canvas.get_tk_widget().grid(row=1,column=0,padx=10,pady=10)


def funct3():
    print("funct3 test")


def save():
    print("save test")


def sb(msg):
    _status_msg.set(msg)


def alert(msg):
    messagebox.showinfo(message=msg)


if __name__ == "__main__": # execute logic if run directly
    _root = Tk() # instantiate instance of Tk class
    _root.title('SPIDAM')
    _mainframe = ttk.Frame(_root, padding='5 5 5 5 ') # root is parent of frame
    _mainframe.grid(row=0, column=0, sticky=("E", "W", "N", "S")) # placed on first row,col of parent
    # frame can extend itself in all cardinal directions
    _url_frame = ttk.LabelFrame(_mainframe, text='File Path', padding='5 5 5 5') # label frame
    _url_frame.grid(row=0, column=0, sticky=("E","W")) # only expands E W
    _url_frame.columnconfigure(0, weight=1)
    _url_frame.rowconfigure(0, weight=1) # behaves when resizing

    _url = StringVar()
    _url.set('') # sets initial value of _url
    _url_entry = ttk.Entry(_url_frame, width=40, textvariable=_url) # text box
    _url_entry.grid(row=0, column=0, sticky=("E","W", "S", "N"), padx=5)
    # grid mgr places object at position

    _fetch_btn = ttk.Button(_url_frame, text='Load file', command=funct1) # create button
    # fetch_url() is callback for button press
    _fetch_btn.grid(row=0, column=1, sticky=W, padx=5)

    _fetch_btn = ttk.Button(_url_frame, text='Analyze', command=plt_graph)  # create button
    # fetch_url() is callback for button press
    _fetch_btn.grid(row=0, column=2, sticky=W, padx=5)

    _save_method = StringVar()
    _save_method.set('img')
    _img_only_radio = ttk.Radiobutton(_url_frame, text='File is .wav', variable=_save_method,
        value='img')
    _img_only_radio.grid(row=1, column=0, padx=5, pady=2, sticky="W")
    _img_only_radio.configure(state='normal')
    _json_radio = ttk.Radiobutton(_url_frame, text='Convert to .wav', variable=_save_method,
        value='json')
    _json_radio.grid(row=2, column=0, padx=5, pady=2, sticky="W")

    _img_frame = ttk.Frame(_mainframe, padding="10")
    _img_frame.grid(row=1, column=0, padx=10,pady=10)
    _img_label = ttk.Label(_img_frame, text="Data analysis")
    _img_label.grid(row=0, column=0)
    # Create an initial empty plot
    fig, ax = plt.subplots(figsize=(4, 2))  # Create a blank figure and axis
    ax.set_title("Graphs")
    ax.set_xlabel("Time")
    ax.set_ylabel("Frequency")
    ax.grid(True)
    fig.tight_layout()

    # Embed the initial empty plot into Tkinter
    canvas = FigureCanvasTkAgg(fig, master=_img_frame)
    canvas.draw()  # Draw the empty plot
    canvas.get_tk_widget().grid(row=1, column=0,padx=10,pady=10)  # Add the canvas to the grid

    _choice_lbl = ttk.Label(_img_frame, text="Data")
    _choice_lbl.grid(row=2, column=0, padx=5, pady=5)

    _btn_frame = ttk.Frame(_mainframe, padding=(0, 10, 0, 0))
    _btn_frame.grid(row=1,column=1)

    _low_btn = ttk.Button(_btn_frame, text='Low', command=funct1)  # create button
    # fetch_url() is callback for button press
    _low_btn.grid(row=0, column=0, sticky=W, padx=5)
    # creates fetch title button
    _mid_btn = ttk.Button(_btn_frame, text='Medium', command=funct2)  # create button
    # fetch_url() is callback for button press
    _mid_btn.grid(row=1, column=0, sticky=W, padx=5)

    # creates fetch link button
    _high_link_btn = ttk.Button(_btn_frame, text='High', command=funct3)  # create button
    # fetch_url() is callback for button press
    _high_link_btn.grid(row=2, column=0, sticky=W, padx=5)

    _status_frame = ttk.Frame(_root, relief='sunken', padding='2 2 2 2')
    _status_frame.grid(row=1, column=0, sticky=("E", "W", "S",))
    _status_msg = StringVar()  # need modified when update status text
    _status_msg.set('Type a file path to select a file...')
    _status = ttk.Label(_status_frame, textvariable=_status_msg, anchor=W)
    _status.grid(row=0, column=0, sticky=(E, W))

    _root.mainloop() # listens for events, blocks any code that comes after it