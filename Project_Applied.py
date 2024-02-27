# Project for Applied Cognitive Science
# Clara Holst and Ola Budrewicz 

list_of_definitions = ["def1","def2","def3","def4"]

list_of_terms = ["term1","term2","term3","term4"]

print("Welcome!")

# User input
while True: # while is running:
   
    user_input = input(" ")

    # Remove term
    if user_input.lower() == "term1":
        list_of_definitions.remove("def1")
        print("removed def1")
    elif user_input.lower() == "term2":
        list_of_definitions.remove("def2")
        print("removed def2")
    elif user_input.lower() == "term3":
        list_of_definitions.remove("def3")
        print("removed def3")
    elif user_input.lower() == "term4":
        list_of_definitions.remove("def4")
        print("removed def4")
    
    # Quit
    if user_input.lower() == "q" or user_input.lower() == "quit" or user_input.lower() == "exit" or user_input.lower() == "quit game" or user_input.lower() == "exit game":
        exit()
        # or break