import os
from flask import Flask, request, render_template, flash
from flask_login import LoginManager, login_user, login_required
from lib.database_connection import get_flask_database_connection
from lib.user import User
from lib.user_repository import UserRepository
from lib.space_repository import SpaceRepository
from lib.space import Space

# Create a new Flask app
app = Flask(__name__, static_folder='static')
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
    conn = get_flask_database_connection(app)
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


@app.route('/create_space', methods=['GET'])
# @login_required
def create_space():
    return render_template('create_space.html')

@app.route('/create_space', methods=["POST"])
# @login_required
def create_space_post():
    conn = get_flask_database_connection(app)
    repository = SpaceRepository(conn)
    # FLASK_LOGIN.CURRENT_USER.id, PLACEHOLDER FOR NOW 
    owner_id = 1
    name = request.form['name']
    description = request.form['description']
    price_per_night = request.form['price_per_night']
    url = request.form['url']

    space = Space(
        None,
        name,
        description,
        price_per_night,
        url,
        owner_id
    )

    new_space_id = repository.create_space(space)
    return get_single_space(new_space_id)


@app.route('/space/<id>', methods=['GET'])
# @login_required
def get_single_space(id):
    conn = get_flask_database_connection(app)
    repository = SpaceRepository(conn)

    space_data = repository.get_single_space(id)
    return render_template('/single_space.html', space = space_data)

    


@login_manager.user_loader
def load_user(user_id):
    return None

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
