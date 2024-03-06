# viewing the flashcards

# imports
import tkinter as tk
import time

# defining index and lists of terms and answers
current_index = 0
current_side = "t" # "t" as in "term", "d" as in "definition"
list_of_terms = ["a", "b", "c", "d"]
list_of_definitions = ["1", "2", "3", "4"]
list_type = list_of_terms # start by showing the terms

# creating a window
window = tk.Tk()
window.title("Flashcards")

# creating a button frame with previous/flip/next buttons
buttonframe = tk.Frame(window)
buttonframe.columnconfigure(0, weight = 1)

# defining the function which updates the label - changes from term to definition and vice versa
# moving from one list to another - BUT!!! ensure that after pressing next and previous, it starts from the terms list (so the term shows first, and you have to press the button to see the definition)
def flip_flashcard():
    global current_side
    global list_type
    if current_side == "t":
        list_type = list_of_definitions
        flashcard.config(text = list_type[current_index])
        current_side = "d" # overwrite the variable
    elif current_side == "d":
        list_type = list_of_terms
        flashcard.config(text = list_type[current_index])
        current_side = "t" # overwrite the variable
    else:
        flashcard.config(text = "How the heck did that happen?")

# defining the previous button function
# moving from current index to previous index - changing the global index by one
def prev_flashcard():
    global current_index
    global current_side
    list_type = list_of_terms # to display the term side of the previous flashcard first
    current_side = "t" # same as above, but to make it work while flipping
    if current_index == 0:
        flashcard.config(text = "There are no previous flashcards.")
        flashcard.after(1000, lambda: flashcard.config(text = list_type[current_index]))
    else:
        current_index = (current_index - 1)
        flashcard.config(text = list_type[current_index])

# defining the next button function  
# moving from current index to next index - changing the global index by one
def next_flashcard():
    global current_index
    global current_side
    list_type = list_of_terms # to display the term side of the next flashcard first
    current_side = "t" # same as above, but to make it work while flipping
    if current_index == ((len(list_type)) - 1):
        flashcard.config(text = "There are no more flashcards.")
        flashcard.after(1000, lambda: flashcard.config(text = list_type[current_index]))
    else:
        current_index = (current_index + 1)
        flashcard.config(text = list_type[current_index])

# adding buttons to the frame
b_previous = tk.Button(buttonframe, text = "Previous", height = 1, width = 10, command = prev_flashcard)
b_previous.grid(row = 0, column = 0, sticky = tk.W + tk.N, padx = 10, pady = 10)
b_flip = tk.Button(buttonframe, text = "Flip", height = 1, width = 10, command = flip_flashcard)
b_flip.grid(row = 0, column = 1, padx = 10, pady = 10)
b_next = tk.Button(buttonframe, text = "Next", height = 1, width = 10, command = next_flashcard)
b_next.grid(row = 0, column = 2, sticky = tk.E + tk.N, padx = 10, pady = 10)

# creating a label to display the definition
flashcard_text = list_of_terms[current_index]
flashcard = tk.Label(window, text = flashcard_text, font = ("Arial", 12))
flashcard.pack(padx = 20, pady = 50)

# packing the buttonframe
buttonframe.pack()

window.mainloop()