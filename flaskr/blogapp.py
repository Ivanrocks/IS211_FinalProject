import os  # For generating secret keys and handling OS-level operations
import dbutility  # Custom module for database operations
from flask import Flask, session, redirect, render_template, url_for, request, flash  # Flask framework for web development
import initializeDB  # Module for initializing the database

# Initialize Flask application
app = Flask('__name__')
app.secret_key = os.urandom(24)  # Generate a random secret key for session management
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Set maximum upload content size to 16MB

# Helper function to check if the user is authenticated
def is_authenticated():
    return 'user_id' in session

# Route for the home page
@app.route('/')
def index():
    posts = dbutility.get_all_posts()  # Fetch all posts from the database
    return render_template('index.html', posts=posts)  # Render the home page with posts

# Route to publish a post
@app.route('/publish/<int:post_id>')
def publish(post_id):
    if not is_authenticated():  # Redirect to home page if not authenticated
        return redirect('/')
    dbutility.publish_post(post_id)  # Publish the post
    flash("Post Published")  # Display a success message
    posts = dbutility.get_all_posts_by_user(int(session['user_id']))  # Fetch posts for the logged-in user
    return render_template('dashboard.html', posts=posts)  # Render the dashboard with updated posts

# Route to unpublish a post
@app.route('/unpublish/<int:post_id>')
def unpublish(post_id):
    if not is_authenticated():  # Redirect to home page if not authenticated
        return redirect('/')
    dbutility.unpublish_post(post_id)  # Unpublish the post
    flash("Post unpublished")  # Display a success message
    posts = dbutility.get_all_posts_by_user(int(session['user_id']))  # Fetch posts for the logged-in user
    return render_template('dashboard.html', posts=posts)  # Render the dashboard with updated posts

# Route to delete a post
@app.route('/delete/<int:post_id>')
def delete(post_id):
    if not is_authenticated():  # Redirect to home page if not authenticated
        return redirect('/')
    dbutility.delete_post(post_id)  # Delete the post
    flash("Post deleted")  # Display a success message
    posts = dbutility.get_all_posts_by_user(int(session['user_id']))  # Fetch posts for the logged-in user
    return render_template('dashboard.html', posts=posts)  # Render the dashboard with updated posts

# Route to edit a post
@app.route('/edit/<int:post_id>', methods=('GET', 'POST'))
def edit(post_id):
    if not is_authenticated():  # Redirect to home page if not authenticated
        return redirect('/')
    if request.method == "POST":  # Handle form submission
        title = request.form['title']  # Get the title from the form
        content = request.form['editordata']  # Get the content from the form
        dbutility.update_post(post_id, title, content)  # Update the post in the database
        flash("Post Saved")  # Display a success message
    post = dbutility.get_post(post_id)  # Fetch the post details
    return render_template('edit.html', post=post)  # Render the edit page with the post details

# Route for the user dashboard
@app.route('/dashboard')
def dashboard():
    if not is_authenticated():  # Redirect to home page if not authenticated
        return redirect('/')
    posts = dbutility.get_all_posts_by_user(int(session['user_id']))  # Fetch posts for the logged-in user
    return render_template('dashboard.html', posts=posts)  # Render the dashboard with posts

# Route to create a draft post
@app.route('/draft', methods=('GET', 'POST'))
def create_draft():
    if not is_authenticated():  # Redirect to home page if not authenticated
        return redirect('/')
    if request.method == 'POST':  # Handle form submission
        postContent = request.form['editordata']  # Get the content from the form
        title = request.form['title']  # Get the title from the form
        dbutility.create_post(postContent, title, session['user_id'])  # Create a new draft post
        flash("Post created. Make sure to publish it")  # Display a success message
    return render_template('draftpost.html')  # Render the draft creation page

# Route for user login
@app.route('/login', methods=('GET', 'POST'))
def login():
    if is_authenticated():  # Redirect to home page if already authenticated
        return redirect('/')
    if request.method == 'POST':  # Handle form submission
        username = request.form['email']  # Get the email from the form
        password = request.form['password']  # Get the password from the form
        user = dbutility.authenticate_user(username, password)  # Authenticate the user
        if user is None:
            flash('Incorrect credentials. Try again')  # Display an error message
        else:
            session.clear()  # Clear the current session
            session['user_id'] = user[0]  # Store the user ID in the session
            return redirect('/dashboard')  # Redirect to the dashboard
    return render_template('login.html')  # Render the login page

# Main entry point for the application
if __name__ == "__main__":
    print("Creating Database.......")
    initializeDB.create_database()  # Initialize the database
    print("Database Created.")
    print("Starting application....")
    app.run()  # Run the Flask application
