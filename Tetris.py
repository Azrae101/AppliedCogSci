# Tetris minigame

# Clara Holst

# Imports
import tkinter as tk
import random

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

# Dictionary to store the positions of elements
element_positions = {}

# Global variable to store label_id
label_id = None

# Function to generate random spawn points
def generate_random_spawn():
    while True:
        x1 = random.randint(50, 250)
        y1 = random.randint(20, 50)
        x2 = x1 + 200
        y2 = y1 + 30
        # Check if the generated spawn point has enough space between elements
        if all(not intersect((x1, y1, x2, y2), pos) for pos in element_positions.values()):
            return x1, y1, x2, y2

# Function to update the label with the next definition
def update_label():
    global label_id, box_id

    if not list_of_display:  # Check if list_of_display is empty
        # Update the text of the existing label
        display_element = list_of_display.pop(0)
        canvas.itemconfig(label_id, text=display_element)
        # Update the position of the box
        x1, y1, x2, y2 = generate_random_spawn()
        canvas.coords(box_id, x1, y1, x2, y2)
        # Update the position of the label
        box_center_x = (x1 + x2) / 2
        box_center_y = (y1 + y2) / 2
        canvas.coords(label_id, box_center_x, box_center_y)
        element_positions[label_id] = (x1, y1, x2, y2)  # Update position of the current element
    else:
        # Create a rectangle box around the next text
        next_box_id = canvas.create_rectangle(50, 70, 250, 100, fill="skyblue", tags="next_box")
        # Calculate the center of the next box
        next_box_center_x = (50 + 250) / 2
        next_box_center_y = (70 + 100) / 2
        # Create the next text at the center of the next box
        next_label_id = canvas.create_text(next_box_center_x, next_box_center_y, text=list_of_display[0], font=("Arial", 12), anchor='center', tags="next_label")
        element_positions[next_label_id] = (50, 70, 250, 100)  # Store position of the next element
        animate_label(next_label_id, next_box_id, 70)  # Start animation for the next label
        list_of_display.pop(0)  # Remove the first element from the list
        if len(list_of_display) >= 1:
            window.after(1000, add_next_element)  # Schedule adding the next element after x seconds
        else:
            message = "No more questions\nYou answered " + str(questions) + " questions"
            canvas.create_text(150, 250, text=message, font=("Arial", 12), anchor='center', tags="message")

def animate_label(label_id, box_id, y_position):
    global element_positions
    label_x1, label_y1, label_x2, label_y2 = canvas.bbox(label_id)
    collision_detected = False

    for other_label_id, other_position in element_positions.items():
        if other_label_id != label_id:
            other_x1, other_y1, other_x2, other_y2 = other_position
            # Check if the labels will collide in the next movement
            if (label_x1 < other_x2 and label_x2 > other_x1 and
                    label_y1 + movement_speed + 20 < other_y2 and label_y2 + movement_speed + 20 > other_y1):
                collision_detected = True
                break

    # Check if collision detected or at bottom threshold
    if collision_detected or y_position + movement_speed >= 540:  # Adjusted threshold to stop 40 pixels before bottom
        element_positions[label_id] = canvas.bbox(label_id)  # Update element position
        check_collision()  # Check for collisions after updating the label
        return
    else:
        canvas.move(label_id, 0, movement_speed)
        canvas.move(box_id, 0, movement_speed)
        window.after(10, animate_label, label_id, box_id, y_position + movement_speed)

# Function to add the next element from list_of_display
def add_next_element():
    if len(list_of_display) >= 2:
        # Create a rectangle box around the next text
        next_box_id = canvas.create_rectangle(50, 70, 250, 100, fill="skyblue", tags="next_box")
        # Calculate the center of the next box
        next_box_center_x = (50 + 250) / 2
        next_box_center_y = (70 + 100) / 2
        # Create the next text at the center of the next box
        next_label_id = canvas.create_text(next_box_center_x, next_box_center_y, text=list_of_display[1], font=("Arial", 12), anchor='center', tags="next_label")
        element_positions[next_label_id] = (50, 70, 250, 100)  # Store position of the next element
        animate_label(next_label_id, next_box_id, 70)  # Start animation for the next label
        list_of_display.pop(1)  # Remove the first element from the list
        window.after(1000, add_next_element)  # Schedule adding the next next element after 5 seconds

# Function to check for collisions between elements
def check_collision():
    global label_id

    user_input = entry.get().lower()
    if user_input in list_of_answers:
        term_index = list_of_answers.index(user_input)
        if term_index < len(list_of_display) and list_of_display[0] == list_of_display[term_index]:
            list_of_display.pop(0)
            list_of_answers.pop(0)  # Ensure both lists are synchronized
            entry.delete(0, tk.END)  # Clear the entry field after each enter
            update_label()  # Update the label with the next definition
            global questions
            questions += 1  # Increment questions by 1
        else:
            # Incorrect answer, do not remove label and box
            entry.delete(0, tk.END)  # Clear the entry field after each enter

# Function to check if two rectangles intersect
def intersect(rect1, rect2):
    x1, y1, x2, y2 = rect1
    x3, y3, x4, y4 = rect2
    return not (x2 < x3 or x4 < x1 or y2 < y3 or y4 < y1)

def handle_input(event):
    global questions  # Declare questions as a global variable

    user_input = entry.get().lower()
    entry.delete(0, tk.END)  # Clear the entry field after each enter

    if user_input.lower() == "q" or user_input.lower() in ["quit", "exit", "quit game", "exit game"]:
        window.quit()
    elif user_input in list_of_answers:
        if list_of_display:  # Check if list_of_display is not empty
            term_index = list_of_answers.index(user_input)
            if term_index < len(list_of_display) and list_of_display[0] == list_of_display[term_index]:
                list_of_display.pop(0)
                list_of_answers.pop(0)  # Ensure both lists are synchronized
                canvas.delete("label", "box")  # Remove displayed label and box from canvas
                update_label()  # Update the label with the next definition
                questions += 1  # Increment questions by 1
            else:
                # Incorrect answer, do not remove label and box
                entry.delete(0, tk.END)  # Clear the entry field after each enter

# Entry widget to take user input
entry = tk.Entry(window, font=("Arial", 12))
entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
entry.focus_set()
entry.bind("<Return>", handle_input)

# Update the label with the first definition
update_label()

# Run the Tkinter event loop
window.mainloop()