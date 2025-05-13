import os
from flask import Flask, request, render_template, flash
from flask_login import LoginManager, login_user
from lib.database_connection import get_flask_database_connection
from lib.user import User
from lib.user_repository import UserRepository
from lib.space_repository import SpaceRepository

# Create a new Flask app
app = Flask(__name__, static_folder='static')
app.secret_key = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

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
    conn = get_flask_database_connection(app)
    repo = UserRepository(conn)
    

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if repo.user_exists(username): 
            active_user = repo.get_user_by_username(username)
            if active_user.password == password:
                login_user(active_user)
                return render_template('index.html')
            else:
                flash('Invalid Credentials')
        else:
            flash('Invalid Credentials')
    return render_template('sign_in.html')

@app.route('/all_spaces', methods=['GET'])
def get_all_spaces():
    conn = get_flask_database_connection(app)
    repo = SpaceRepository(conn)
    spaces = repo.get_all()
    return render_template('all_spaces.html', spaces=spaces)

@login_manager.user_loader
def load_user(user_id):
    conn = get_flask_database_connection(app)
    repo = UserRepository(conn)
    user = repo.get_user_by_id(user_id)
    if user:
        return user
    return None

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
