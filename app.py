# Flask app
from flask import (Flask, g, render_template, redirect, url_for, 
                  request, flash, session)
import hashlib
import sqlite3
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-fallback-key')

# Database setup
def get_db():
    if 'db' not in g:
        # db_path = os.path.join('database', 'database.sqlite') # for testing
        db_path = os.path.join(os.path.dirname(__file__), 'instance', 'database.sqlite')
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
        # Add the column if it doesn't exist
        cursor = g.db.cursor()
        cursor.execute("PRAGMA table_info(user)")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]
        if 'first_name' not in column_names:
            cursor.execute("ALTER TABLE user ADD COLUMN first_name TEXT")
            g.db.commit()
        if 'last_name' not in column_names:
            cursor.execute("ALTER TABLE user ADD COLUMN last_name TEXT")
            g.db.commit()
        if 'email' not in column_names:
            cursor.execute("ALTER TABLE user ADD COLUMN email TEXT")
            g.db.commit()
        if 'account_name' not in column_names:
            cursor.execute("ALTER TABLE user ADD COLUMN account_name TEXT")
            g.db.commit()

        # Q & A in deck
        if 'question' not in column_names:
            cursor.execute("ALTER TABLE user ADD COLUMN question TEXT")
            g.db.commit()
        if 'answer' not in column_names:
            cursor.execute("ALTER TABLE user ADD COLUMN answer TEXT")
            g.db.commit()
        if 'question1' not in column_names:
            cursor.execute("ALTER TABLE user ADD COLUMN question1 TEXT")
            g.db.commit()
        if 'answer1' not in column_names:
            cursor.execute("ALTER TABLE user ADD COLUMN answer1 TEXT")
            g.db.commit()
        if 'question2' not in column_names:
            cursor.execute("ALTER TABLE user ADD COLUMN question2 TEXT")
            g.db.commit()
        if 'answer2' not in column_names:
            cursor.execute("ALTER TABLE user ADD COLUMN answer2 TEXT")
            g.db.commit()
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Quiz data
list_of_display = ["A condition where an individual can perceive visual stimuli but cannot recognize or interpret them correctly.", "A theory proposing that attention is necessary to bind individual features of an object together to perceive it as a whole.", "The process by which a skill becomes automatic through practice and experience.", "A brain structure involved in processing emotions, particularly fear and aggression."]
list_of_answers = ["Visual Agnosia", "Feature Integration Theory", "Proceduralization", "Amygdala"]
list_type = list_of_display
current_index = 0
current_side = "t"

questions = 1

@app.before_request
def before_request():
    g.logged_in = session.get('logged_in', False)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/publiclibrary')
def publiclibrary():
    return render_template('public_library.html')

@app.route('/sciencebehind')
def sciencebehind():
    return render_template('science_behind.html')

@app.route('/minigames')
def minigames():
    return render_template('minigames.html')

# Decks
@app.route('/mydecks')
def mydecks():
    return render_template('my_decks/my_decks.html')

@app.route('/deck_two')
def deck_two():
    return render_template('my_decks/deck_two.html')

# Games
@app.route('/cardchase')
def cardchase():
    return render_template('games/cardchase.html')

@app.route('/tetricards')
def tetricards():
    return render_template('games/tetricards.html')

@app.route('/termtime')
def termtime():
    return render_template('games/termtime.html')

@app.route('/definedash')
def definedash():
    return render_template('games/definedash.html')

# Game settings
@app.route('/cardchase_settings')
def cardchase_settings():
    return render_template('game_settings/cardchase_settings.html')

@app.route('/definedash_settings')
def definedash_settings():
    return render_template('game_settings/definedash_settings.html')

@app.route('/flashcards_settings')
def flashcards_settings():
    return render_template('game_settings/flashcards_settings.html')

@app.route('/tetris_settings')
def tetris_settings():
    return render_template('game_settings/tetris_settings.html')

@app.route('/termtime_settings')
def termtime_settings():
    return render_template('game_settings/termtime_settings.html')

@app.route('/quiz_settings')
def quiz_settings():
    return render_template('game_settings/quiz_settings.html')

# Flashcards viewing
@app.route('/flashcards')
def flashcards():
    global current_index
    global current_side
    global list_of_display
    global list_of_answers

    term = list_of_display[current_index]
    if current_side == "d":
        term = list_of_answers[current_index]
    return render_template('games/flashcards.html', term=term, list_of_display=list_of_display, list_of_answers=list_of_answers, current_index=current_index, current_side=current_side)

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
    global questions
    if list_of_display:
        current_question = list_of_display[0]
    else:
        current_question = f"No more questions. You answered {questions-1} questions."
    return render_template('games/quiz.html', question=current_question)

@app.route('/answer', methods=['POST'])
def handle_answer():
    global questions
    user_input = request.form.get('answer').strip().lower()  # Normalize user input

    # Check if user input is in list_of_answers
    if user_input in map(str.lower, list_of_answers):
        # Get the index of the answer
        answer_index = list(map(str.lower, list_of_answers)).index(user_input)

        # Check if the index is within bounds
        if answer_index < len(list_of_display):
            # Check if the question corresponding to the answer matches the current question
            if list_of_display[0].lower() == list_of_display[answer_index].lower():
                # If matched, remove both question and answer
                list_of_display.pop(0)
                list_of_answers.pop(answer_index)
                questions += 1

    return redirect(url_for('quiz'))

### Search
@app.route('/search', methods=['POST'])
def search_results():
    search_query = request.form['search']
    # Predefined search results
    predefined_results = ['login', 'register', 'flashcards', 'quiz', 'cardchase','definedash','termtime','tetricards']
    # Check if the search query matches any predefined result
    results = [result for result in predefined_results if search_query.lower() in result]
    return render_template('search_results.html', search_query=search_query, results=results)


@app.route('/deck_one')
def deck_one():
    # Check if the user is logged in
    if not g.logged_in:
        # Redirect the user to the login page or handle it based on your logic
        flash('Please log in to access this page.')
        return redirect(url_for('login'))

    # Retrieve the logged-in user's information
    db = get_db()
    user_id = session.get('user_id')
    cur = db.execute("SELECT * FROM user WHERE id=?", (user_id,))
    user = cur.fetchone()

    # Check if user information is found in the database
    if user is None:
        flash('User information not found. Please try again.')
        return redirect(url_for('login'))

    # Pass the user variable to the template context
    return render_template('my_decks/deck_one.html', user=user)

### Deck
@app.route('/my_decks/deck_one', methods=['GET', 'POST'])
def edit_deck():
    """Update flashcard"""

    if request.method == 'POST':
        # Connect to the database
        db = get_db()

        # Retrieve the logged-in user's ID
        user_id = session.get('user_id')

        # Retrieve form data for each question and answer pair
        question = request.form.get('question', '')
        answer = request.form.get('answer', '')
        question1 = request.form.get('question1', '')
        answer1 = request.form.get('answer1', '')
        question2 = request.form.get('question2', '')
        answer2 = request.form.get('answer2', '')

        # Get the card identifier from the form data
        card_id = request.form.get('card_id')

        # Update user data in the database based on the card identifier
        if card_id == '1':
            db.execute("UPDATE user SET question=?, answer=? WHERE id=?", (question, answer, user_id))
        elif card_id == '2':
            db.execute("UPDATE user SET question1=?, answer1=? WHERE id=?", (question1, answer1, user_id))
        elif card_id == '3':
            db.execute("UPDATE user SET question2=?, answer2=? WHERE id=?", (question2, answer2, user_id))

        db.commit()

        flash('Flashcards updated successfully.')

        # Redirect to the page
        return redirect(url_for('deck_one'))

    # Retrieve the logged-in user's information
    db = get_db()
    user_id = session.get('user_id')
    cur = db.execute("SELECT * FROM user WHERE id=?", (user_id,))
    user = cur.fetchone()

    if user is None:
        # Handle the case where the user is not found in the database
        flash('User not found.')
        return redirect(url_for('login'))

    # Pass the user variable to the template context
    return render_template('my_decks/deck_one.html', user=user)


### Profile
@app.route('/profile/settings', methods=['GET', 'POST'])
def profile_settings():
    """Update user profile settings"""
    if request.method == 'POST':
        # Connect to the database
        db = get_db()

        # Retrieve the logged-in user's ID
        user_id = session.get('user_id')

        # Retrieve form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        account_name = request.form['account_name']
        # You can handle profile picture upload here if needed

        # Update user profile in the database
        db.execute("UPDATE user SET first_name=?, last_name=?, email=?, account_name=? WHERE id=?",
                   (first_name, last_name, email, account_name, user_id))
        db.commit()

        flash('Profile updated successfully.')

        # Redirect to the profile settings page or any other appropriate page
        return redirect(url_for('profile_settings'))

    # Retrieve the logged-in user's information
    db = get_db()
    user_id = session.get('user_id')
    cur = db.execute("SELECT * FROM user WHERE id=?", (user_id,))
    user = cur.fetchone()

    # Pass the user variable to the template context
    return render_template('profile_settings.html', user=user)

### LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log in user"""

    # If we receive form data try to log the user in
    if request.method == 'POST':

        # Connect to the database
        db = get_db()

        # Retrieve the users password from database (and check if user exist)
        cur = db.execute("SELECT * FROM user WHERE username=?", (request.form['username'],))
        user = cur.fetchone()
        
        # Check if a user was found
        if user is None:
            flash('User not found.')
            return render_template('login.html')

        # TODO: Check if the passwords match
        print(user['password'])
        # flash('Invalid password.', 'error')

        # If everything is okay, log in the user 
        session.clear()
        session['user_id'] = user['id']
        flash('You were logged in.')

        if user is not None:
            session['logged_in'] = True
            session['user_id'] = user['id']
            flash('You were logged in.')
            return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You were logged out.')
    return redirect(url_for('home'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    """Registers a new user"""

    # If we receive form data try to register the new user
    if request.method == 'POST':
        
        # Connect to the database
        db = get_db()

        # Username length limit:
        if len((request.form["username"])) > 10:
            flash("Your username is too long, please try again")
            return render_template('register.html')

        # Check if username is available
        cur = db.execute("SELECT * FROM user WHERE username=?", (request.form['username'],))
        existing_user = cur.fetchone()
        if existing_user:
            flash("Username '{}' already taken".format(request.form['username']), 'error')
            return render_template('register.html')

        # Check if the two passwords match
        if request.form['password1'] != request.form['password2']:
            flash("Passwords do not match, try again.", 'error')
            return render_template('register.html')

        # Strong password check (not implemented rn)
        '''
        def is_strong_password(password):
            # Password must be at least 8 characters long
            if len(password) < 8:
                return False
            # Password must contain at least one uppercase letter
            if not re.search(r'[A-Z]', password):
                return False
            # Password must contain at least one lowercase letter
            if not re.search(r'[a-z]', password):
                return False
            # Password must contain at least one digit
            if not re.search(r'\d', password):
                return False
            # Password must contain at least one symbol
            if not re.search(r'[^a-zA-Z0-9]', password):
                return False
            # If all conditions are met, the password is strong
            return True

        # Check if the password is strong
        if not is_strong_password(request.form['password1']):
            flash("Password is too weak, try again.", 'error')
            return render_template('register.html')
        '''

        # If all above is approved: create the user
        hashed_password = hashlib.sha256(request.form['password1'].encode()).hexdigest()
        db=get_db()
        db.execute("INSERT INTO user (username, password) VALUES (?,?)",
                   (request.form['username'], hashed_password))
        db.commit()
        flash("User '{}' registered, you can now log in.".format(request.form['username']), 'info')
        
        return redirect(url_for('login'))

    # If we receive no data: just show the registration form again
    else:
        return render_template('register.html')

# for testing:
#if __name__ == '__main__':
#    app.run(debug=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render uses $PORT
    app.run(host="0.0.0.0", port=port, debug=False)  # Must bind to 0.0.0.0