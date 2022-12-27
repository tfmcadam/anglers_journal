from flask_app import app
from flask_app.models.users_model import User
from flask_app.models.locations_model import Location
from flask import render_template, redirect, request, session, flash, jsonify
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 

#exam code 46b357F3

# STARTING POINT

@app.route("/")
@app.route("/dashboard")
def landing():
    if "user_id" not in session:
        all_locations = Location.get_all()
        return render_template('dashboard.html',all_locations=all_locations)
    return redirect('logged/dashboard')

@app.route("/g_map")
def g_map():
    return render_template("simple_map.html")

# if not in session you can't go to dashboard

@app.route('/logged/dashboard')
def dash():
    if not "user_id" in session:
        return redirect('/')
    user_data = {
            'id': session['user_id']
        }
    logged_user = User.get_by_id(user_data)
    all_locations = Location.get_all()
    return render_template("logged_dashboard.html", logged_user=logged_user, all_locations=all_locations)

@app.route("/sign_up")
def register_user():
    return render_template("register.html")

#REGISTER PATH FOR REGISTRATION FORM
# bcrypt and log in path
# if not valid goes back to landing, otherwise to the dashboard

@app.route('/users/register', methods=['POST'])
def reg_user():
    if not User.validator(request.form):
        return redirect('/sign_up')
    hash_browns =bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password' : hash_browns
    }
    new_id = User.create(data)
    session["user_id"] = new_id
    return redirect(f'/user_page/{new_id}')

# LOG IN A USER
@app.route('/users/login', methods=['POST'] )
def log_user():
    data = {
        'email' : request.form['email']
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid credentials", "log")
        return redirect('/sign_up')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid credentials **", "log")
        return redirect('/dashboard')
    session['user_id'] = user_in_db.id
    
    return redirect(f'/user_page/{session["user_id"]}')

@app.route("/user_page/<int:id>")
def user_page(id):
    if not "user_id" in session:
        return redirect('/dashboard')
    logged_user = User.get_by_id({"id": session['user_id']})
    return render_template("user_page.html", logged_user=logged_user)

# jsonify to get id
@app.route('/get_id')
def get_by_id_json():
    data = {"user_id": session['user_id']}
    return jsonify(User.get_by_id_json(data))
    

# Logout

@app.route('/users/logout')
def log_out_user():
    del session["user_id"]
    return redirect('/dashboard')



@app.errorhandler(404)
def page_not_found(error):
    return "<h1>Sorry! No response. Try again.</h1>"

