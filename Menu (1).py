from tkinter import *
from tkinter import ttk,filedialog,messagebox

from Sine import make_sine

#ONLY GRAPH BUTTON WORKS RIGHT NOW

def funct1():
    print("funct1 test")


def funct2():
    print("funct2 test")


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
    _root.title('Sound Graph App')
    _mainframe = ttk.Frame(_root, padding='5 5 5 5 ') # root is parent of frame
    _mainframe.grid(row=0, column=0, sticky=("E", "W", "N", "S")) # placed on first row,col of parent
    # frame can extend itself in all cardinal directions
    _url_frame = ttk.LabelFrame(
        _mainframe, text='File Path', padding='5 5 5 5') # label frame
    _url_frame.grid(row=0, column=0, sticky=("E","W")) # only expands E W
    _url_frame.columnconfigure(0, weight=1)
    _url_frame.rowconfigure(0, weight=1) # behaves when resizing

    _url = StringVar()
    _url.set('') # sets initial value of _url
    _url_entry = ttk.Entry(
        _url_frame, width=40, textvariable=_url) # text box
    _url_entry.grid(row=0, column=0, sticky=(E, W, S, N), padx=5)
    # grid mgr places object at position
    _fetch_btn = ttk.Button(
        _url_frame, text='Low', command=funct1) # create button
    # fetch_url() is callback for button press
    _fetch_btn.grid(row=0, column=1, sticky=W, padx=5)

    # creates fetch title button
    _fetch_title_btn = ttk.Button(
        _url_frame, text='Medium', command=funct2)  # create button
    # fetch_url() is callback for button press
    _fetch_title_btn.grid(row=1, column=1, sticky=W, padx=5)

    # creates fetch link button
    _fetch_link_btn = ttk.Button(
        _url_frame, text='High', command=funct3)  # create button
    # fetch_url() is callback for button press
    _fetch_link_btn.grid(row=2, column=1, sticky=W, padx=5)

    # img_frame contains Lisbox and Radio Frame
    _img_frame = ttk.LabelFrame(
        _mainframe, text='Content', padding='9 0 0 0')
    _img_frame.grid(row=1, column=0, sticky=(N, S, E, W))

    # Set _img_frame as parent of Listbox and _images is variable tied to
    _images = StringVar()
    _img_listbox = Listbox(
        _img_frame, listvariable=_images, height=6, width=25)
    _img_listbox.grid(row=0, column=0, sticky=(E, W), pady=5)
    #Scrollbar can move vertical
    _scrollbar = ttk.Scrollbar(
        _img_frame, orient=VERTICAL, command=_img_listbox.yview)
    _scrollbar.grid(row=0, column=1, sticky=(S, N), pady=6)
    _img_listbox.configure(yscrollcommand=_scrollbar.set)

    #Listbox occupies (0,0) on _img_frame.
    # Scrollbar occupies (0,1) so _radio_frame goes to (0,2)
    _radio_frame = ttk.Frame(_img_frame)
    _radio_frame.grid(row=0, column=2, sticky=(N, S, W, E))

    # place label and padding
    # radio buttons are children of _radio_frame
    _choice_lbl = ttk.Label(
        _radio_frame, text="Choose to convert file")
    _choice_lbl.grid(row=0, column=0, padx=5, pady=5)
    _save_method = StringVar()
    _save_method.set('img')
    # Radiobutton connected to _save_method variable
    # Know which button is selected by checking value
    _img_only_radio = ttk.Radiobutton(
        _radio_frame, text='File is .wav', variable=_save_method,
        value='img')
    _img_only_radio.grid(row=1, column=0,padx=5, pady=2, sticky="W")
    _img_only_radio.configure(state='normal')
    _json_radio = ttk.Radiobutton(
        _radio_frame, text='Convert to .wav', variable=_save_method,
        value='json')
    _json_radio.grid(row=2, column=0, padx=5, pady=2, sticky="W")

    # save command saves images to be listed in Listbox after parsing
    _scrape_btn = ttk.Button(
        _mainframe, text='Graph', command=make_sine)
    _scrape_btn.grid(row=2, column=0, sticky=E, pady=5)

    _status_frame = ttk.Frame(
        _root, relief='sunken', padding='2 2 2 2')
    _status_frame.grid(row=1, column=0, sticky=("E", "W", "S"))
    _status_msg = StringVar() # need modified when update status text
    _status_msg.set('Type a file path to select a file...')
    _status= ttk.Label(
        _status_frame, textvariable=_status_msg, anchor=W)
    _status.grid(row=0, column=0, sticky=(E, W))

    _root.mainloop() # listens for events, blocks any code that comes after it