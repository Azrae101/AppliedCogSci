# Flask app

from flask import Flask, render_template, request

app = Flask(__name__)

# Your existing quiz data
list_of_display = ["a", "b", "c", "d"]
list_of_answers = ["1", "2", "3", "4"]
questions = 1

@app.route('/')
def index():
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

    return index()

if __name__ == '__main__':
    app.run(debug=True)
