import os
from files_chord_recognition import chord_recognition


def chords():
    global accurate, inaccurate, split
    test_dir = os.chdir('test_chords')
    accurate = 0
    inaccurate = 0

    for file in os.listdir(test_dir):
        split = file.split(' ')
        if (split[0] == 'Grand'):
            chord_recognition(chord_callback, file)

    print("The recognizer is " + str(accurate * 100 / (accurate + inaccurate)) + " accurate for the given test cases.")


def chord_callback(chord):
    global accurate, inaccurate
    if (chord == split[-2]):
        accurate += 1
    else:
        inaccurate += 1


chords()
