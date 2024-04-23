# Flask app
from flask import (
    Flask, g, render_template, redirect, url_for, request, flash,
    session, jsonify
)
import hashlib
import sqlite3
import os
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

# Configuration
app.config['SECRET_KEY'] = "create-your-own"

# Database setup
def get_db():
    if 'db' not in g:
        db_path = os.path.join('database', 'database.sqlite')
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
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Quiz data
list_of_display = ["Question A", "Question B", "Question C", "Question D"]
list_of_answers = ["1", "2", "3", "4"]
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

@app.route('/find')
def find():
    return render_template('find.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/minigames')
def minigames():
    return render_template('minigames.html')

@app.route('/cardchase')
def cardchase():
    return render_template('games/cardchase.html')

@app.route('/tetris')
def tetris():
    return render_template('games/tetris.html')

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
    if list_of_display:
        current_question = list_of_display[0]
    else:
        current_question = f"No more questions. You answered {questions} questions."
    return render_template('games/quiz.html', question=current_question)

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

### Search
@app.route('/search', methods=['POST'])
def search_results():
    search_query = request.form['search']
    # Predefined search results
    predefined_results = ['login', 'register', 'flashcards', 'quiz', 'cardchase']
    # Check if the search query matches any predefined result
    results = [result for result in predefined_results if search_query.lower() in result]
    return render_template('search_results.html', search_query=search_query, results=results)

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

if __name__ == '__main__':
    app.run(debug=True)
