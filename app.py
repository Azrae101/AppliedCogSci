# Flask app
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Quiz data
list_of_display = ["a", "b", "c", "d"]
list_of_answers = ["1", "2", "3", "4"]
list_type = list_of_display
current_index = 0
current_side = "t"

questions = 1

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/flashcards')
def flashcards():
    global current_index
    global current_side
    global list_of_display
    global list_of_answers

    term = list_of_display[current_index]
    if current_side == "d":
        term = list_of_answers[current_index]
    return render_template('flashcards.html', term=term, list_of_display=list_of_display, list_of_answers=list_of_answers, current_index=current_index, current_side=current_side)

@app.route('/prev')
def prev_flashcard():
    global current_side
    current_side = "t"
    global current_index
    if current_index > 0:
        current_index -= 1
    return redirect('/flashcards')

@app.route('/next')
def next_flashcard():
    global current_side
    current_side = "t"
    global current_index
    if current_index < len(list_of_display) - 1:
        current_index += 1
    return redirect('/flashcards')

@app.route('/flip', methods=['POST'])
def flip_flashcard():
    global current_side
    if current_side == "t":
        current_side = "d"
    else:
        current_side = "t"
    return redirect('/flashcards')

@app.route('/quiz')
def quiz():
    if list_of_display:
        current_question = list_of_display[0]
    else:
        current_question = f"No more questions. You answered {questions} questions."
    return render_template('quiz.html', question=current_question)

@app.route('/answer', methods=['POST'])
def handle_answer():
    global questions
    user_input = request.form.get('answer').lower()

    if user_input in list_of_answers:
        term_index = list_of_answers.index(user_input)
        if term_index < len(list_of_display) and list_of_display[0] == list_of_display[term_index]:
            list_of_display.pop(0)
            list_of_answers.pop(0)
            questions += 1

    return redirect(url_for('quiz'))

if __name__ == '__main__':
    app.run(debug=True)
