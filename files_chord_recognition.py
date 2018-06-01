import os
import tkinter as tk
import tkinter.scrolledtext

# added three lines to make compatible with mac
import matplotlib

matplotlib.use("TkAgg")
import numpy as np
from hmm import compute_chord_for_frame
from scipy.io.wavfile import read
import threading


def chord_recognition():
    directory = os.getcwd() + '/test_chords/'
    fname = 'output.wav'

    (rate, data) = read(directory + fname)
    # framing audio
    framing_rate = rate
    hop_size = 1024
    frame_count = int(np.round(len(data) / (framing_rate - hop_size)))
    # zero padding to make signal length long enough to have nFrames
    data = np.append(data, np.zeros(framing_rate))
    start = 0

    for n in range(frame_count):
        frame = data[start:start + framing_rate]
        start = start + framing_rate - hop_size
        chord = compute_chord_for_frame(frame, rate)  # here yoo get the chord, so do some nice printing
        # ideally make the printing function in a separate file and just import it here
        # Chords added in the loop

        textArea.insert(tk.END, chord+"\n")
        textArea.see(tk.END)




# Create a window
window = tk.Tk()
window.title("Chords")  # Title for the window
window.geometry("250x200")  # Window size


container = tk.Frame(window, width=80, height=80)
textArea = tk.Text(window, height=5, width=10)
scrollbar = tk.Scrollbar(container)
scrollbar.pack(side="right", fill="y")
textArea.pack(side="left", fill="both", expand=True)

Process = threading.Thread(target=chord_recognition)
Process.start()

window.mainloop()
