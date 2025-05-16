import os
from flask import Flask, request, render_template, flash, redirect, url_for, session
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from lib.database_connection import get_flask_database_connection
from lib.user import User
from lib.user_repository import UserRepository
from lib.space_repository import SpaceRepository
from lib.space import Space
from lib.booking_repo import BookingRepository
from lib.booking import Booking
from datetime import datetime, timedelta, date
from flask_bcrypt import Bcrypt
import calendar


app = Flask(__name__, static_folder='static')
app.secret_key = os.urandom(24)
# app.secret_key = 'dev-key-123'
app.permanent_session_lifetime = timedelta(hours=1)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "sign_in"


@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html')

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    conn = get_flask_database_connection(app)
    repo = UserRepository(conn)

    if request.method == "POST":
        password = request.form['password']
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(None, request.form['username'], request.form['email'], pw_hash, request.form['phone_number'])
        active_user_id = repo.create_user(new_user)
        login_user(active_user_id)
        return redirect('/all_spaces')
    else:
        return render_template('/sign_up.html')

@app.route('/sign_in', methods=['GET','POST'])
def sign_in():
    conn = get_flask_database_connection(app)
    repo = UserRepository(conn)
    

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        hash_password = bcrypt.generate_password_hash(password)
        bcrypt.check_password_hash(hash_password, password)
        if repo.user_exists(username): 
            active_user = repo.get_user_by_username(username)
            if bcrypt.check_password_hash(active_user.password, password):
                login_user(active_user)
                session.permanent = True
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
@login_required
def get_user_profile(id):
    conn = get_flask_database_connection(app)
    repository = UserRepository(conn)
    space_repository = SpaceRepository(conn)
    booking_repository = BookingRepository(conn)


    user_data = repository.get_user_by_id(current_user.id)
    spaces = space_repository.get_all_owner_spaces(user_data.id)

    space_bookings = booking_repository.get_all_bookings_by_owner_id(current_user.id)
    holidays_booked = booking_repository.get_bookings_by_user_id(current_user.id)


    return render_template('dashboard.html', user_data = user_data, spaces = spaces, space_bookings = space_bookings, holidays_booked = holidays_booked)

@app.route('/approve_booking/<id>', methods=['POST'])
def approve_booking(id):
    conn = get_flask_database_connection(app)
    booking_repository = BookingRepository(conn)
    approved_booking = booking_repository.approve_booking(id)
    booking_repository.delete_duplicate_bookings(approved_booking.space_id, approved_booking.date)
    return redirect(f'/dashboard/{current_user.id}')

@app.route('/decline_booking/<id>', methods=['POST'])
def decline_booking(id):
    conn = get_flask_database_connection(app)
    booking_repository = BookingRepository(conn)
    booking_repository.decline_booking(id)
    return redirect(f'/dashboard/{current_user.id}')



############################################################################################################
############################################################################################################


def get_month_calendar(year, month, blocked_dates):
    """Generate calendar data for the given month"""
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]

    calendar_data = []
    for week in cal:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append({"day": "", "blocked": False, "empty": True})
            else:
                current_date = date(year, month, day)
                is_blocked = current_date in blocked_dates
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

@app.route('/bookspace/<space_id>', methods=['GET', 'POST'])
def booking(space_id):
    year = int(request.args.get('year', datetime.now().year))
    month = int(request.args.get('month', datetime.now().month))

    conn = get_flask_database_connection(app)
    repo = BookingRepository(conn)
    blocked_dates = repo.get_booked_dates_for_space(space_id)

    today = date.today()

    booked_date_objects = [datetime.strptime(d, "%Y-%m-%d").date() for d in blocked_dates]

    past_dates = [
        date(year, month, day)
        for week in calendar.monthcalendar(year, month)
        for day in week if day != 0 and date(year, month, day) < today
]

    blocked_date_objects = booked_date_objects + past_dates

    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1
    generated_calendar = get_month_calendar(year, month, blocked_date_objects)
    
    if request.method == "GET":
        return render_template('calendar.html', 
                        blocked_dates=blocked_date_objects,
                        calendar=generated_calendar,    
                        space_id=space_id,
                        month=month,
                        year=year)
    else:
        user_id = current_user.id
        booking_date = request.form['date']
        booking = Booking(None, user_id, space_id, booking_date)
        repo.create_booking(booking)
        return redirect(url_for('get_user_profile', id=user_id))


@app.route('/logout')
@login_required
def logout():
    logout_user() 
    return redirect(url_for('sign_in'))





##########################################################################################################
##########################################################################################################


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
