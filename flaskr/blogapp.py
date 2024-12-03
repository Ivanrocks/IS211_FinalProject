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
    return render_template('index.html', posts = posts)

@app.route('/publish/<int:post_id>')
def publish(post_id):
    if not is_authenticated():
        return redirect('/')
    dbutility.publish_post(post_id)
    message = "Post Published"
    flash(message)
    posts = dbutility.get_all_posts_by_user(int(session['user_id']))
    return render_template('dashboard.html', posts=posts)

@app.route('/unpublish/<int:post_id>')
def unpublish(post_id):
    if not is_authenticated():
        return redirect('/')
    dbutility.unpublish_post(post_id)
    message = "Post unpublished"
    flash(message)
    posts = dbutility.get_all_posts_by_user(int(session['user_id']))
    return render_template('dashboard.html', posts=posts)

@app.route('/delete/<int:post_id>')
def delete(post_id):
    if not is_authenticated():
        return redirect('/')
    dbutility.delete_post(post_id)
    message = "Post deleted"
    flash(message)
    posts = dbutility.get_all_posts_by_user(int(session['user_id']))
    return render_template('dashboard.html', posts=posts)

@app.route('/edit/<int:post_id>', methods=('GET', 'POST'))
def edit(post_id):
    if not is_authenticated():
        return redirect('/')
    if request.method == "POST":
        title = request.form['title']
        content = request.form['editordata']
        dbutility.update_post(post_id,title, content)
        message = "Post Saved"
        flash(message)
    post = dbutility.get_post(post_id)
    return render_template('edit.html', post=post)

@app.route('/dashboard')
def dashboard():
    if not is_authenticated():
        return redirect('/')
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
            return redirect('/dashboard')
    return render_template('login.html')


if __name__ == "__main__":
    print("Creating Database.......")
    initializeDB.create_database()
    print("Database Created.")
    print("Starting application....")
    app.run()