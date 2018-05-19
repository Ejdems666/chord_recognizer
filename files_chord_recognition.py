import os

import numpy as np

from hmm2 import compute_chord_for_frame

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

for n in range(frame_count):
    frame = data[start:start + framing_rate]
    start = start + framing_rate - hop_size
    chord = compute_chord_for_frame(frame, rate) # here yoo get the chord, so do some nice printing
    # ideally make the printing function in a separate file and just import it here
    print(chord)

print('done')
