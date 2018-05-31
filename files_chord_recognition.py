import os
import tkinter as tk

# added three lines to make compatible with mac
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

import numpy as np

from hmm import compute_chord_for_frame

directory = os.getcwd() + '/test_chords/'
fname = 'Grand Piano - Fazioli - major B middle.wav'

from scipy.io.wavfile import read

(rate, data) = read(directory + fname)

# framing audio
framing_rate = rate
hop_size = 1024
frame_count = int(np.round(len(data) / (framing_rate - hop_size)))
# zero padding to make signal length long enough to have nFrames
data = np.append(data, np.zeros(framing_rate))
start = 0

#Create a window
window = tk.Tk()
window.title("Chords")# Title for the window
window.geometry("500x400") # Window size

for n in range(frame_count):
    frame = data[start:start + framing_rate]
    start = start + framing_rate - hop_size
    chord = compute_chord_for_frame(frame, rate) # here yoo get the chord, so do some nice printing
    # ideally make the printing function in a separate file and just import it here
    # Chords added in the loop
    T = tk.Text(window, height = 5, width = 10)
    T.pack()
    T.insert(tk.END, chord)
    print(chord)

# Start the GUI
window.mainloop()

print('done')
