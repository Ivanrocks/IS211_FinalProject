import os
import dbutility
from flask import Flask, session, redirect, render_template, url_for, request, flash

import initializeDB

app = Flask(__name__)
app.secret_key = os.urandom(24)

def is_authenticated():
    return 'user_id' in session

@app.route('/')
def index():
    posts = dbutility.get_all_posts()
    print(posts)
    return render_template('dashboard.html', posts = posts)



@app.route('/login', methods=('GET', 'POST'))
def login():
    if is_authenticated():
        return redirect('/')
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        user = dbutility.authenticate_user(username, password)
        if user is None:
            error = 'Incorrect credentials. Try again'
            flash(error)
        else:
            error = 'User Authenticated'
            session.clear()
            session['user_id'] = username
            print("User authenticated")
            return redirect('/')
    return render_template('login.html')





if __name__ == "__main__":
    print("Creating Database.......")
    initializeDB.create_database()
    print("Database Created.")
    print("Starting application")
    app.run()