from flask import Flask, flash, redirect, render_template, url_for, request, session 
from random import randint 
users = {}

app = Flask(__name__)
app.secret_key = 'your_secret_key' #i guess this is the replacement for jwt_authentication

puzzles = puzzles_with_answers = [
    {"puzzle": "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?", "answer": "an echo"},
    {"puzzle": "What is always coming, but never arrives?", "answer": "tomorrow"},
    {"puzzle": "What has an endless supply but the more you take, the larger it becomes?", "answer": "a hole"},
    {"puzzle": "What is light as a feather, yet the strongest person can't hold it for five minutes?", "answer": "breath"},
    {"puzzle": "What has one head, one foot, and four legs, but can't walk?", "answer": "a bed"},
    {"puzzle": "What is full of ups and downs but always remains in the same place?", "answer": "a staircase"},
    {"puzzle": "What can you hold in your right hand, but never in your left hand?", "answer": "your left elbow"},
    {"puzzle": "What has no voice, yet can tell you stories?", "answer": "a book"},
    {"puzzle": "The more there is, the less you see. What is it?", "answer": "darkness"},
    {"puzzle": "What is taken from a mine and shut up in a wooden case, from which it is never released, and used by almost everybody?", "answer": "pencil lead"}
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
        random_index = randint(0,len(puzzles)-1)
        puzzle_data = puzzles[random_index]
        puzzle = puzzle_data["puzzle"]
        correct_answer = puzzle_data["answer"] 
        return render_template('test.html', name=name, puzzle=puzzle, correct_answer=correct_answer, feedback=session.pop('feedback', None))
    else: 
        return redirect(url_for('login'))

@app.route("/check_answer", methods=['POST'])
def check_answer():
    user_answer = request.form['answer']
    correct_answer = request.form['correct_answer']
    #name = "User"  # You might want to get the user's name from session

    if user_answer.lower() == correct_answer.lower():
        session['feedback'] = "Correct! Here's a new puzzle:"
        return redirect(url_for('dashboard'))
    else:
        session['feedback'] = "Try again!"
        return redirect(url_for('dashboard'))
        #return render_template('dashboard.html', name=name, puzzle=puzzles[0]["puzzle"], correct_answer=correct_answer, feedback=session.pop('feedback', None)) 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80) 