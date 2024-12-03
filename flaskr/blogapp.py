import os

import dbutility
from flask import Flask, session, redirect, render_template, url_for, request, flash

import initializeDB

app = Flask('__name__')
app.secret_key = os.urandom(24)

def is_authenticated():
    return 'user_id' in session

@app.route('/')
def index():
    posts = dbutility.get_all_posts()
    print(posts)
    return render_template('index.html', posts = posts)

@app.route('/publish/<int:user_id>')
def publish():
    if not is_authenticated():
        return redirect('/')
    message = "Post Published"
    flash(message)
    return render_template('dashboard.html')

@app.route('/unpublish/<int:user_id>')
def unpublish():
    if not is_authenticated():
        return redirect('/')
    message = "Post unpublished"
    flash(message)
    return render_template('dashboard.html')

@app.route('/dashboard')
def dashboard():
    if not is_authenticated():
        return redirect('/')
    print(session['user_id'])
    posts = dbutility.get_all_posts_by_user(int(session['user_id']))
    return render_template('dashboard.html', posts = posts)

@app.route('/draft', methods=('GET', 'POST'))
def create_draft():
    if not is_authenticated():
        return redirect('/')

    error = None

    if request.method == 'POST':
        postContent = request.form['editordata']
        title = request.form['title']
        dbutility.create_post(postContent, title, session['user_id'])
        error = "Post created. Make sure to publish it"
        flash(error)


    return render_template('draftpost.html')

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
            session['user_id'] = user[0]
            print("User authenticated")
            return redirect('/')
    return render_template('login.html')


if __name__ == "__main__":
    print("Creating Database.......")
    initializeDB.create_database()
    print("Database Created.")
    print("Starting application....")
    app.run()