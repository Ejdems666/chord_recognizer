import threading

import numpy as np
import pyaudio

from GUI import GUI_text_with_scrollbar, update_text_area
from hmm import compute_chord_for_frame

finish_recognition = False


def chord_recognition():
    CHUNK = 16384
    FORMAT = pyaudio.paUInt8
    CHANNELS = 1
    RATE = 44100
    FRAME_LENGTH = 0.5
    THRESHOLD = 130

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=False,
                    frames_per_buffer=CHUNK,
                    input_device_index=3)

    while stream.is_active() and not finish_recognition:
        snippet = []
        for i in range(0, int(RATE / CHUNK * FRAME_LENGTH)):
            data = stream.read(CHUNK)
            snippet.append(data)
        data = np.frombuffer(b''.join(snippet), dtype=np.uint8)
        if max(data) > THRESHOLD:
            chord = compute_chord_for_frame(data, RATE)
            update_text_area(text_area, chord)
        else:
            update_text_area(text_area, ".")

    stream.stop_stream()
    stream.close()
    p.terminate()


(window, text_area) = GUI_text_with_scrollbar()

chord_recognition_process = threading.Thread(target=chord_recognition)
chord_recognition_process.start()

window.mainloop()
finish_recognition = True
chord_recognition_process.join()

