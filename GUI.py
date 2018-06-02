from tkinter import *

def GUI_text_with_scrollbar():
    window = Tk()
    window.title("Chords")  # Title for the window
    window.geometry("250x200")  # Window size
    container = Frame(window, width=80, height=80)
    text_area = Text(window, height=5, width=10, font=("Courier", 44))
    scrollbar = Scrollbar(container)
    scrollbar.pack(side="right", fill="y")
    text_area.pack(side="left", fill="both", expand=True)

    return window, text_area


def update_text_area(text_area, chord):
    text_area.insert(END, chord + "\n")
    text_area.see(END)