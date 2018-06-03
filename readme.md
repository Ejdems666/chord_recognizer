# Chord recognizer

This project uses template matching to analyze sound and figure out what chord is it.

It is able to distinguish between these chords: 'G','G#','A','A#','B','C','C#','D','D#','E','F','F#','Gm','G#m','Am','A#m','Bm','Cm','C#m','Dm','D#m','Em','Fm','F#m'

# how to run

Run chord_tester.py that tests all of the chords in test_chords folder and prints a percentage of how successful is the chord recognition.

Run files_chord_recognition.py to analyze a specific chord (it opens a GUI window)

Run input_steam_chord_recognition.py if you have an instrument (or smth that can stream sound data into the computer).
You'll see live chord_recognition feed in the opened GUI window


# Setup troubleshoot

If you get error saying that you need to install python as a framework, try the correct awnser here:
https://stackoverflow.com/questions/21784641/installation-issue-with-matplotlib-python