# Basic Blog Application

This is a simple blog application built with Flask, a lightweight web framework for Python. It allows users to create drafts, publish and unpublish posts, edit posts, and view their posts on a dashboard.

**Requirements:**

* Python 3
* Flask
* Additional dependencies may be required for the `dbutility` and `initializeDB` modules (check their documentation).

**Installation:**

1. Create a virtual environment to isolate project dependencies (recommended).
2. Install Flask: `pip install Flask`
3. Install any additional dependencies for `dbutility` and `initializeDB`.
4. Implement the `dbutility` and `initializeDB` modules according to your database needs.

**Running the application:**

1. Open a terminal in the project directory.
2. Run the application: `python app.py`
3. emil: admin
4. pass: admin

**Features:**

* User login and authentication (implementation in `dbutility.authenticate_user`)
* Draft post creation
* Post publishing and unpublishing
* Post editing
* User dashboard to view published posts

**Note:**

* This is a basic example and requires further development for functionalities like user registration, password hashing, etc. 
* Secure your database credentials and implement proper error handling.

**Further Development:**

* Implement user registration
* Enhance user profile management
* Add features like comments, categories, etc.
* Deploy the application to a web server

**Contributing:**

* Pull requests are welcome! Please follow coding conventions and create clear issue descriptions.