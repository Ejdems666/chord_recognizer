from tkinter import *

# root = Tk()
# theLabel = Label(root, text="This is too easy")
# theLabel.pack()
# root.mainloop()

'''import tkinter as tk

#Create a window
window = tk.Tk()
window.title("Harro")# Let us give a title to our window
window.geometry("500x400") #Window size

# Let us add our members to the window
T = tk.Text(window)
T.pack()
T.insert(tk.END, "Petes number 1, \nJens" )

def ReavealId():
    T.insert(tk.END, "\nJens is shitanusdick")

# Add a button
b = tk.Button(text="What is Jens?", command=ReavealId)
b.pack()

# Start the GUI
window.mainloop()
'''


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