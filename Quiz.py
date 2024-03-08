# Quiz Minigame

# Minigame: Type the term that correlates with the definition
# Clara Holst

# Imports
import tkinter as tk

# Variables
questions = 1

# Define your lists
list_of_display = ["a", "b", "c", "d"]
list_of_answers = ["1", "2", "3", "4"]
list_of_hints = ["one", "", "three", "four"]

# Create a Tkinter application window
window = tk.Tk()
window.title("Quiz")

# defining the "give up" function
def give_up():
    global l_giveup
    l_giveup = tk.Label(text = list_of_answers[0])
    l_giveup.pack()
    b_giveup.config(state = "disabled") # disables the button
    b_hint.config(state = "disabled") # disables the "hint" button, because why would you use a hint if you have the answer?
    l_hint.pack_forget() # clears the hint

# defining the "hint" function
def hint():
    global l_hint
    l_hint = tk.Label(text = list_of_hints[0])
    l_hint.pack()
    b_hint.config(state = "disabled") # disables the button
    l_giveup.pack_forget() # clears the answer
    

# creating the buttonframe
buttonframe = tk.Frame(window)
buttonframe.columnconfigure(0, weight = 1)
buttonframe.pack(side = tk.BOTTOM)

# creating the "give up" and "hint" button
b_giveup = tk.Button(buttonframe, text = "Give up", height = 1, width = 10, command = give_up)
b_giveup.grid(row = 0, column = 0, padx = 20, pady = 10)
b_hint = tk.Button(buttonframe, text = "Hint", height = 1, width = 10, command = hint)
b_hint.grid(row = 0, column = 1, padx = 10, pady = 10)

# Function to update the label text
def update_label():
    if list_of_display:
        label_text.set(list_of_display[0])
    else:
        label_text.set("No more questions \nYou answered " + str(questions) + " questions")

# Create and pack a label to display the definition
label_text = tk.StringVar()
label = tk.Label(window, textvariable=label_text, font=("Arial", 12))
label.pack(padx=20, pady=50)

# Update the label with the first definition
update_label()

# User input handling
def handle_input(event):
    global questions  # Declare questions as a global variable

    user_input = entry.get().lower()
    entry.delete(0, tk.END)  # Clear the entry field after each enter

    if user_input == "q" or user_input in ["quit", "exit", "quit game", "exit game"]:
        window.quit()
    elif user_input in list_of_answers:
        term_index = list_of_answers.index(user_input)
        if term_index < len(list_of_display) and list_of_display[0] == list_of_display[term_index]:
            list_of_display.pop(0)
            list_of_answers.pop(0)  
            list_of_hints.pop(0) # Ensure all lists are synchronized
            update_label()
            questions += 1  # Increment questions by 1
            if list_of_display:
                b_giveup.config(state = "normal") # reverts the "give up" button to normal
                if list_of_hints[0] == "":
                    b_hint.config(state = "disabled") # if there is no hint, the button is disabled
                else:
                    b_hint.config(state = "normal") # reverts the "hint" button to normal
            else:
                b_giveup.config(state = "disabled")
                b_hint.config(state = "disabled")
            l_giveup.pack_forget() # clears the answer
            l_hint.pack_forget() # clears the hint

# Entry widget to take user input
entry = tk.Entry(window, font=("Arial", 12))
entry.pack(padx=20, pady=10, side = tk.BOTTOM)
entry.focus_set()
entry.bind("<Return>", handle_input)

# Run the Tkinter event loop
window.mainloop()
