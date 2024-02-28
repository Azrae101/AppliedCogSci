# "Before they fall" minigame

# Clara Holst

# Imports
import tkinter as tk

# Variables
questions = 0
movement_speed = 10

# Define your lists
list_of_display = ["a", "b", "c", "d"]
list_of_answers = ["1", "2", "3", "4"]

# Create a Tkinter application window
window = tk.Tk()
window.title("Before they fall")
window.geometry("350x600")

# Entry widget to take user input
entry = tk.Entry(window, font=("Arial", 12))
entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
entry.focus_set()

# Create a canvas to draw animation
canvas = tk.Canvas(window, bg="white", width=300, height=500)  # Adjust canvas height
canvas.grid(row=0, column=0, padx=20, pady=20)

# Function to update the label text and animate
def update_label():
    global label_id, box_id, initial_y_position
    if list_of_display:
        canvas.delete("label", "box", "game_over")  # Delete previous label, box, and game over message
        # Create a rectangle box around the text
        box_id = canvas.create_rectangle(50, 20, 250, 50, fill="skyblue", tags="box")
        # Calculate the center of the box
        box_center_x = (50 + 250) / 2
        box_center_y = (20 + 50) / 2
        # Create the text at the center of the box
        label_id = canvas.create_text(box_center_x, box_center_y, text=list_of_display[0], font=("Arial", 12), anchor='center', tags="label")
        initial_y_position = 20  # Reset initial y-position
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
            initial_y_position = 20  # Reset initial y-position
            canvas.delete(label_id, box_id)  # Delete label and box when they reach the bottom
            print("Reached bottom threshold")
            # Display Game Over message
            canvas.create_text(150, 225, text="Game Over", font=("Arial", 20), fill="red", tags="game_over")
            # Remove the entry widget when the game is over
            entry.destroy()
            canvas.delete("label", "box")  # Delete previous label and box
            if questions == 0:
                canvas.create_text(150, 300, text="You answered 0 questions", font=("Arial", 12), anchor='center', tags="label")
            elif questions < 0:
                canvas.create_text(150, 300, text=("You answered " + str(questions) + " questions"), font=("Arial", 12), anchor='center', tags="label")

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

# Update the label with the first definition
update_label()

# Run the Tkinter event loop
window.mainloop()
