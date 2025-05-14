import os
from flask import Flask, request, render_template, flash, redirect
from flask_login import LoginManager, login_user, login_required
from lib.database_connection import get_flask_database_connection
from lib.user import User
from lib.user_repository import UserRepository
from lib.space_repository import SpaceRepository
from lib.space import Space


app = Flask(__name__, static_folder='static')
app.secret_key = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "sign_in"

@app.route('/index', methods=['GET'])
def get_index():
    return render_template('index.html')

@app.route('/sign_in', methods=['GET','POST'])
def sign_in():
    conn = get_flask_database_connection(app)
    repo = UserRepository(conn)
    

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if repo.user_exists(username): 
            active_user = repo.get_user_by_username(username)
            if active_user.password == password:
                login_user(active_user)
                return redirect('/all_spaces')
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

@app.route('/create_space', methods=['GET'])
@login_required
def create_space():
    return render_template('create_space.html')

@app.route('/create_space', methods=["POST"])
@login_required
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
        owner_id,
        url
    )

    new_space_id = repository.create_space(space)
    return redirect(f'/space/{new_space_id}')


@app.route('/space/<id>', methods=['GET'])
@login_required
def get_single_space(id):
    conn = get_flask_database_connection(app)
    repository = SpaceRepository(conn)

    space_data = repository.get_single_space(id)
    return render_template('/single_space.html', space = space_data)

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    conn = get_flask_database_connection(app)
    repo = UserRepository(conn)
    
    if request.method == "POST":
        new_user = User(None, request.form['username'], request.form['email'], request.form['password'], request.form['phone_number'])
        active_user_id = repo.create_user(new_user)
        login_user(active_user_id)
        return redirect('/all_spaces')
    else:
        return render_template('/sign_up.html')


@login_manager.user_loader
def load_user(user_id):
    conn = get_flask_database_connection(app)
    repo = UserRepository(conn)
    user = repo.get_user_by_id(user_id)
    if user:
        return user
    return None



if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
