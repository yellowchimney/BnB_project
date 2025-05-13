import os
from flask import Flask, request, render_template, flash
from flask_login import LoginManager, login_user
from lib.database_connection import get_flask_database_connection
from lib.user import User
from lib.user_repository import UserRepository

# Create a new Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

users = {"user_1": {"username": "user_1", "password": "password_1"},
        "user_2" :{"username": "user_2", "password": "password_2"}}

# == Your Routes Here ==

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5001/index
@app.route('/index', methods=['GET'])
def get_index():
    return render_template('index.html')

@app.route('/sign_in', methods=['GET','POST'])
def get_login():
    conn = get_flask_database_connection()
    repo = UserRepository(conn)

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        active_user = repo.get_user_by_username(username)
        if active_user.password == password:
            login_user(active_user)
            return render_template('index.html')
        else:
            flash('Invalid Credentials')
    return render_template('sign_in.html')


@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        user_data = users[user_id]
        return User(user_id, user_data["name"])
    return None

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
