from flask import Flask, flash, redirect, render_template, url_for, request, session 
from random import randint 
from datetime import datetime 
users = {}

app = Flask(__name__)
app.secret_key = 'your_secret_key' #i guess this is the replacement for jwt_authentication

puzzles = [
    {"puzzle": "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?", "answer": "an echo", "hint": "It repeats"},
    {"puzzle": "What is always coming, but never arrives?", "answer": "tomorrow"},
    {"puzzle": "What has an endless supply but the more you take, the larger it becomes?", "answer": "a hole", "hint": "It's an empty space"},
    {"puzzle": "What is light as a feather, yet the strongest person can't hold it for five minutes?", "answer": "breath", "hint": "You need it to live"},
    {"puzzle": "What has one head, one foot, and four legs, but can't walk?", "answer": "a bed", "hint": "You sleep on it"},
    {"puzzle": "What is full of ups and downs but always remains in the same place?", "answer": "a staircase", "hint": "It helps you go up and down"},
    {"puzzle": "What can you hold in your right hand, but never in your left hand?", "answer": "your left elbow", "hint": "It's part of your arm"},
    {"puzzle": "What has no voice, yet can tell you stories?", "answer": "a book", "hint": "You read it"},
    {"puzzle": "The more there is, the less you see. What is it?", "answer": "darkness", "hint": "It's the absence of light"},
    {"puzzle": "What is taken from a mine and shut up in a wooden case, from which it is never released, and used by almost everybody?", "answer": "pencil lead", "hint": "You write with it"}
]

@app.route("/")
def index():
    #return "Index!"
    return render_template(
        'index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    #return "This will become the login page"
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username 
            session['correct_count'] = 0 
            flash('Login successful!', 'success')
            #return redirect(url_for('dashboard',name=username))  # Redirect to a logged-in page
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    #return "This will become the register page"
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash('Username already taken', 'danger')
        else:
            users[username] = password
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route("/hello")
def hi_not_dashboard():
    return render_template('dashboard.html')

@app.route("/dashboard")
def dashboard():
    if 'username' in session: 
        name = session['username']
        if 'current_puzzle_index' not in session:
            session['current_puzzle_index'] = randint(0, len(puzzles) - 1)
            session['start_time'] = datetime.now() 
        elif 'feedback' in session and "Correct!" in session['feedback']:
            session['start_time'] = datetime.now() 

        puzzle_index = session['current_puzzle_index']
        puzzle_data = puzzles[puzzle_index]
        puzzle = puzzle_data["puzzle"]
        correct_answer = puzzle_data["answer"] 
        #hint = puzzle_data["hint"] 
        session['hint_available'] = True 
        correct_count = session.get('correct_count', 0)
        time_taken = session.pop('time_taken', None) 
        feedback = session.pop('feedback', None)
        
        print(f"hint_available in dashboard: {session.get('hint_available')}")  # Add this
        return render_template('test.html', name=name, puzzle=puzzle, correct_answer=correct_answer, hint=hint, feedback=feedback, correct_count=correct_count, time_taken=time_taken)
    else: 
        return redirect(url_for('login'))

@app.route("/check_answer", methods=['POST'])
def check_answer():
    user_answer = request.form['answer']
    correct_answer = request.form['correct_answer']
    session['correct_count'] = session.get('correct_count', 0) + 1

    if user_answer.lower() == correct_answer.lower():
        end_time = datetime.now()
        start_time = session.pop('start_time', None)
        time_taken = None 
        if start_time:
            time_taken = str(end_time - start_time).split('.')[0] # Calculate duration and remove microseconds
            session['time_taken'] = time_taken

        session['feedback'] = f"Correct! Time taken: {time_taken}. Here's a new puzzle:"
        session['hint_available'] = False
        session['current_puzzle_index'] = randint(0, len(puzzles) - 1)
        session['correct_count'] = session.get('correct_count', 0) + 1 # Increment correct count
        return redirect(url_for('dashboard'))
    else:
        session['feedback'] = "Try again!"
        session['hint_available'] = True 
        return redirect(url_for('dashboard'))

@app.route("/hint") # added route for hint
def hint():
    #print(session)
    if 'username' in session and 'current_puzzle_index' in session: #and session.get('hint_available')
        index = session['current_puzzle_index']
        hint = puzzles[index]["hint"]
        flash(f"Hint: {hint}", 'info') #flash the hint
        #session['hint_available'] = False 
        return redirect(url_for('dashboard'))
    else:
        if 'username' not in session:
            return redirect(url_for('login'))
        elif not session.get('hint_available'):
            flash("You have already used the hint for this puzzle.", 'warning')
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80) 