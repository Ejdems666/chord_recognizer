import tkinter as tk

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

