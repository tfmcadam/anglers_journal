from flask_app import app
from flask_app.models.users_model import User
from flask_app.models.locations_model import Location
from flask import render_template, redirect, request, session, flash, jsonify


# new location form

@app.route('/locations/new')
def new_location():
    user_data = {
        'id': session['user_id']
    }
    logged_user = User.get_by_id(user_data)
    return render_template("location_new.html", logged_user=logged_user)


# new location submit/validation
@app.route('/locations/create', methods=['POST'])
def create_location():
    if 'user_id' not in session:
        return redirect('/')
    if not Location.validator(request.form):
        return redirect('/locations/new')
    data = {
        **request.form,
        'user_id': session['user_id']
    }
    Location.create(data)
    return redirect(f'/user_page/{session["user_id"]}')


# JSON to get all locations

@app.route('/get_data')
def get_data():
    # jsonify will serialize data into JSON format.
    return jsonify(Location.get_all_JSON())

# EDIT ROUTE TO FORM
    # EDIT TAG


@app.route("/locations/<int:id>/edit")
def edit_location(id):
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
            'id': session['user_id']
        }
    logged_user = User.get_by_id(user_data)
    this_location = Location.get_by_id({'id': id})
    return render_template("location_edit.html", this_location=this_location, logged_user=logged_user)

# updated info passing

@app.route('/locations/<int:id>/update', methods=['POST'])
def update_location(id):
    if not Location.validator(request.form):
        return redirect(f'/locations/{id}/edit')
    location_data = {
        **request.form,
        'id': id
    }
    Location.edit_location(location_data)
    return redirect('/dashboard')

# for show one page 

@app.route('/get_location_id')
def json_get_by_id1():
    
    data = session['location_id']
    return jsonify(Location.get_by_json(data))

# view location entire location


@app.route('/locations/<int:id>')
def one_location(id):
    if 'user_id' not in session:
        return redirect('/')
    session['location_id'] = {'id' : id}
    this_location = Location.get_by_id({'id': id})
    logged_user = User.get_by_id({"id": session['user_id']})
    return render_template('location_one.html', this_location=this_location, logged_user=logged_user)

# delete location

@app.route('/locations/<int:id>/delete')
def del_location(id):
    Location.del_location({'id': id})
    return redirect(f'/user_page/{session["user_id"]}')

