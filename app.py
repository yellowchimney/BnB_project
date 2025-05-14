import os
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, login_required
from lib.database_connection import get_flask_database_connection
from lib.user import User
from lib.user_repository import UserRepository
from lib.space_repository import SpaceRepository
from lib.space import Space
from datetime import datetime, timedelta, date
import calendar


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

@app.route('/dashboard/<id>', methods=['GET'])
# @login_required
def get_user_profile(id):
    conn = get_flask_database_connection(app)
    repository = UserRepository(conn)
    space_repository = SpaceRepository(conn)

    user_data = repository.get_user_by_id(id)
    spaces = space_repository.get_all_owner_spaces(user_data.id)

    return render_template('/dashboard.html', user_data = user_data, spaces = spaces)



############################################################################################################
############################################################################################################

# Define the dates you want to block
blocked_dates = [
    "2025-05-20",  # Example blocked date
    "2025-05-25",  # Example blocked date
    "2025-06-01",  # Example blocked date
    "2025-05-15",  # Today's date (for demonstration)
    "2025-05-16",  # Tomorrow (for demonstration)
]

def get_month_calendar(year, month):
    """Generate calendar data for the given month"""
    # Get the calendar for the month
    cal = calendar.monthcalendar(year, month)
    
    # Get the month name
    month_name = calendar.month_name[month]
    
    # Convert blocked_dates to datetime objects for comparison
    blocked_date_objects = [datetime.strptime(d, "%Y-%m-%d").date() for d in blocked_dates]
    
    # Create calendar data with blocked status
    calendar_data = []
    for week in cal:
        week_data = []
        for day in week:
            if day == 0:
                # Day is outside the month
                week_data.append({"day": "", "blocked": False, "empty": True})
            else:
                # Check if this date is blocked
                current_date = date(year, month, day)
                is_blocked = current_date in blocked_date_objects
                formatted_date = current_date.strftime("%Y-%m-%d")
                
                week_data.append({
                    "day": day, 
                    "blocked": is_blocked, 
                    "empty": False,
                    "date": formatted_date
                })
        calendar_data.append(week_data)
    
    return {
        "month_name": month_name,
        "year": year,
        "calendar_data": calendar_data
    }

@app.route('/testroute')
def testing():
    # Get current year and month or from query parameters
    year = int(request.args.get('year', datetime.now().year))
    month = int(request.args.get('month', datetime.now().month))
    
    # Generate calendar data
    calendar_data = get_month_calendar(year, month)
    
    # Calculate next month

    next_month = month + 1
    if next_month == 13:
        next_month = 0
    
    
    return render_template('test.html', 
                        blocked_dates=blocked_dates,
                        calendar=calendar_data,    
                        )



##########################################################################################################
##########################################################################################################

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
