# "Before they fall" minigame 
# Endless

# Clara Holst

# Imports
import tkinter as tk
import random

# Variables
questions = 0
movement_speed = 1

# Define your lists
list_of_display = ["a", "b", "c", "d"]
list_of_answers = ["1", "2", "3", "4"]

# Shuffle indices and randomize
indices = list(range(len(list_of_display)))
random.shuffle(indices)
shuffled_display = [list_of_display[i] for i in indices]
shuffled_answers = [list_of_answers[i] for i in indices]

# Create a Tkinter application window
window = tk.Tk()
window.title("Before they fall")
window.geometry("350x650") 

# Entry widget to take user input
entry = tk.Entry(window, font=("Arial", 12))
entry.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
entry.focus_set()

# Create a canvas to draw animation
canvas = tk.Canvas(window, bg="white", width=300, height=500) 
canvas.grid(row=1, column=0, padx=20, pady=20)

# Point counter label
point_label = tk.Label(window, text=f"Questions Answered: {questions}", font=("Arial", 12))
point_label.grid(row=0, column=0, pady=10, padx=0, sticky="ew")

# Function to update the point counter
def update_point_counter():
    global questions
    point_label.config(text=f"Questions Answered: {questions}")
    # Update the point counter label position to the top of the canvas
    point_label.grid(row=0, column=0, pady=10, padx=0, sticky="ew")

# Function to update the label text and animate
def update_label():
    global label_id, box_id, initial_y_position, shuffled_display, shuffled_answers

    if not shuffled_answers:  # Check if no more questions left
        if questions > 0:  # Check if at least one question was answered
            # Display Congratulations message
            canvas.create_text(150, 225, text="You won!", font=("Arial", 20), fill="green", tags="win")
            entry.destroy()  # Remove user-text-box
            point_label.destroy()
            window.geometry("350x560")
            canvas.delete("label", "box")  # Delete previous label and box
            if questions == 0:
                canvas.create_text(150, 300, text=("You did not answer any questions"), font=("Arial", 12), anchor='center', tags="label")
            elif questions == 1:
                canvas.create_text(150, 300, text=("You answered one question"), font=("Arial", 12), anchor='center', tags="label")
            else:
                canvas.create_text(150, 300, text=("You answered " + str(questions+1) + " questions"), font=("Arial", 12), anchor='center', tags="label")
            return 

    canvas.delete("label", "box", "game_over")  # Delete previous label, box, and game over message
    # Create a rectangle box around the text
    box_id = canvas.create_rectangle(50, 70, 250, 100, fill="skyblue", tags="box")
    # Calculate the center of the box
    box_center_x = (50 + 250) / 2
    box_center_y = (70 + 100) / 2
    # Create the text at the center of the box
    label_id = canvas.create_text(box_center_x, box_center_y, text=shuffled_display[0], font=("Arial", 12), anchor='center', tags="label")
    initial_y_position = 70  # Reset initial y-position
    animate_label(label_id, box_id, initial_y_position)  # Start animation
    entry.bind("<Return>", handle_input)

# Function to animate the label and box falling down
def animate_label(label_id, box_id, y_position):
    global initial_y_position

    bbox = canvas.bbox(label_id)  # Get the bounding box of the label

    if bbox is not None:  # Check if bbox is not None
        label_height = bbox[3] - bbox[1]  # Calculate the height of the label text

        if y_position + label_height < 480:
            canvas.move(label_id, 0, movement_speed)
            canvas.move(box_id, 0, movement_speed)
            window.after(20, animate_label, label_id, box_id, y_position + movement_speed)
        else:
            initial_y_position = 70  # Reset initial y-position
            canvas.delete(label_id, box_id)  # Delete label and box when they reach the bottom
            print("Reached bottom threshold")
            # Display Game Over message
            canvas.create_text(150, 225, text="Game Over", font=("Arial", 20), fill="red", tags="game_over")
            # Remove the entry widget when the game is over
            entry.destroy()
            point_label.destroy()
            window.geometry("350x560")
            canvas.delete("label", "box")  # Delete previous label and box
            if questions == 0:
                canvas.create_text(150, 300, text=("You did not answer any questions"), font=("Arial", 12), anchor='center', tags="label")
            if questions == 1:
                canvas.create_text(150, 300, text=("You answered one question"), font=("Arial", 12), anchor='center', tags="label")
            if questions > 1:
                canvas.create_text(150, 300, text=("You answered " + str(questions) + " questions"), font=("Arial", 12), anchor='center', tags="label")

# User Input
def handle_input(event):
    global questions  # Declare questions as a global variable

    user_input = entry.get().lower()
    entry.delete(0, tk.END)  # Clear the entry field after each enter

    if user_input.lower() == "q" or user_input.lower() in ["quit", "exit", "quit game", "exit game"]:
        window.quit()
    elif user_input in shuffled_answers:
        if shuffled_answers:  # Check if list_of_answers is not empty
            term_index = shuffled_answers.index(user_input)
            if term_index < len(shuffled_display) and shuffled_display[0] == shuffled_display[term_index]:
                shuffled_display.pop(0)
                shuffled_answers.pop(0)  # Ensure both lists are synchronized
                canvas.delete("label", "box")  # Remove displayed label and box from canvas
                update_label()  # Update the label with the next definition
                questions += 1  # Increment questions by 1
                update_point_counter()  # Update the point counter

# Update the label with the first definition
update_label()

# Run the Tkinter event loop
window.mainloop()
