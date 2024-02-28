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

# Create a Tkinter application window
window = tk.Tk()
window.title("Quiz")

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
            list_of_answers.pop(0)  # Ensure both lists are synchronized
            update_label()
            questions += 1  # Increment questions by 1

# Entry widget to take user input
entry = tk.Entry(window, font=("Arial", 12))
entry.pack(padx=20, pady=10)
entry.focus_set()
entry.bind("<Return>", handle_input)

# Run the Tkinter event loop
window.mainloop()
