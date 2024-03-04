# Tetris minigame

# Clara Holst

# Imports
import tkinter as tk

# Variables
questions = 1
movement_speed = 10  # Adjust as needed

# Define your lists
list_of_display = ["a", "b", "c", "d"]
list_of_answers = ["1", "2", "3", "4"]

# Create a Tkinter application window
window = tk.Tk()
window.title("Tetris")
window.geometry("520x680")

# Create a canvas to draw animation
canvas = tk.Canvas(window, bg="white", width=480, height=580)  # Adjust canvas height
canvas.grid(row=0, column=0, padx=20, pady=20)

# Function to update the label text and animate
def update_label():
    global label_id, box_id, current_index
    if list_of_display:
        canvas.delete("label", "box")  # Delete previous label and box
        # Create a rectangle box around the text
        box_id = canvas.create_rectangle(50, 20, 250, 50, fill="skyblue", tags="box")
        # Calculate the center of the box
        box_center_x = (50 + 250) / 2
        box_center_y = (20 + 50) / 2
        # Create the text at the center of the box
        label_id = canvas.create_text(box_center_x, box_center_y, text=list_of_display[0], font=("Arial", 12), anchor='center', tags="label")
        animate_label(label_id, box_id, 20)  # Start animation
        if len(list_of_display) > 1:
            window.after(5000, add_next_element)  # Schedule adding the next element after 5 seconds
    else:
        canvas.delete("label", "box")  # Delete previous label and box
        message = "No more questions\nYou answered " + str(questions) + " questions"
        label_id = canvas.create_text(150, 250, text=message, font=("Arial", 12), anchor='center', tags="label")

# Function to animate the label and box falling down
def animate_label(label_id, box_id, y_position):
    if y_position < 540:  # Bottom threshold
        canvas.move(label_id, 0, movement_speed)
        canvas.move(box_id, 0, movement_speed)
        window.after(10, animate_label, label_id, box_id, y_position + movement_speed)

# Function to add the next element from list_of_display
def add_next_element():
    global current_index
    if len(list_of_display) >= 2:
        canvas.delete("next_label", "next_box")  # Delete previous next label and box
        # Create a rectangle box around the next text
        next_box_id = canvas.create_rectangle(50, 70, 250, 100, fill="lightgreen", tags="next_box")
        # Calculate the center of the next box
        next_box_center_x = (50 + 250) / 2
        next_box_center_y = (70 + 100) / 2
        # Create the next text at the center of the next box
        next_label_id = canvas.create_text(next_box_center_x, next_box_center_y, text=list_of_display[1], font=("Arial", 12), anchor='center', tags="next_label")
        animate_label(next_label_id, next_box_id, 70)  # Start animation for the next label
        list_of_display.pop(1)  # Remove the first element from the list
        window.after(5000, add_next_element)  # Schedule adding the next next element after 5 seconds
    else:
        canvas.delete("next_label", "next_box")  # Delete previous next label and box

# User Input
def handle_input(event):
    global questions  # Declare questions as a global variable

    user_input = entry.get().lower()
    entry.delete(0, tk.END)  # Clear the entry field after each enter

    if user_input.lower() == "q" or user_input.lower() in ["quit", "exit", "quit game", "exit game"]:
        window.quit()
    elif user_input in list_of_answers:
        if list_of_answers:  # Check if list_of_answers is not empty
            term_index = list_of_answers.index(user_input)
            if term_index < len(list_of_display) and list_of_display[0] == list_of_display[term_index]:
                list_of_display.pop(0)
                list_of_answers.pop(0)  # Ensure both lists are synchronized
                canvas.delete("label", "box")  # Remove displayed label and box from canvas
                update_label()  # Update the label with the next definition
                questions += 1  # Increment questions by 1

# Entry widget to take user input
entry = tk.Entry(window, font=("Arial", 12))
entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
entry.focus_set()
entry.bind("<Return>", handle_input)

# Update the label with the first definition
update_label()

# Run the Tkinter event loop
window.mainloop()
