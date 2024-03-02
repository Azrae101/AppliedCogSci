# viewing the flashcards

# imports
import tkinter as tk

# defining lists of terms and answers
list_of_terms = ["a", "b", "c", "d"]
list_of_answers = ["1", "2", "3", "4"]

# creating a window
window = tk.Tk()
window.title("Flashcards")

# creating a button frame with previous/next buttons
buttonframe = tk.Frame(window)
buttonframe.columnconfigure(0, weight = 1)

# adding buttons to the frame
b_previous = tk.Button(buttonframe, text = "Previous", height = 1, width = 10)
b_previous.grid(row = 0, column = 0, sticky = tk.W + tk.N, padx = 10, pady = 10)
b_next = tk.Button(buttonframe, text = "Next", height = 1, width = 10)
b_next.grid(row = 0, column = 1, sticky = tk.E + tk.N, padx = 10, pady = 10)

# packing the buttonframe
buttonframe.pack()

window.mainloop()