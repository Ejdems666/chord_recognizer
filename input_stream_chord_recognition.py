import numpy as np
import pyaudio
from hmm import compute_chord_for_frame

CHUNK = 16384
FORMAT = pyaudio.paUInt8
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 0.5
THRESHOLD = 130

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=False,
                frames_per_buffer=CHUNK,
                input_device_index=3)

while stream.is_active():
    snippet = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        snippet.append(data)
    data = np.frombuffer(b''.join(snippet), dtype=np.uint8)
    if max(data) > THRESHOLD:
        chord = compute_chord_for_frame(data, RATE)
        # here yoo get the chord, so do some nice printing
        # ideally make the printing function in a separate file and just import it here
        print(chord)
    else:
        print(".")

stream.stop_stream()
stream.close()
p.terminate()
