from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import users_model
from flask_app import DATABASE
from flask import flash


class Location:
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.lat = data['lat']
        self.lng = data['lng']
        self.time = data['time']
        self.date = data['date']
        self.weather = data['weather']
        self.comments = data['comments']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        
    @classmethod
    def create(cls, data):
        query = "INSERT INTO locations (location, lat, lng, time, date, weather, comments, user_id) VALUES (%(location)s,%(lat)s,%(lng)s,%(time)s,%(date)s,%(weather)s,%(comments)s,%(user_id)s)"
        return connectToMySQL(DATABASE).query_db(query, data)

    # UPDATE locations
    #REQUIRES WHERE FOR ID

    @classmethod
    def edit_location(cls, data):
        query = "UPDATE locations SET location = %(location)s, time = %(time)s,date = %(date)s,date = %(date)s,weather = %(weather)s,comments = %(comments) WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    # GET location BY ID
    # JOIN FOR USER TO DISPLAY USER location
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM locations JOIN users ON locations.user_id = users.id WHERE locations.id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return False
        row = results[0]
        this_location = cls(row)
        user_data = {
            **row,
            'id': row['users.id'],
            'created_at': row['created_at'],
            'updated_at': row['updated_at']
        }
        this_user = users_model.User(user_data)
        this_location.create = this_user
        return this_location


    @classmethod
    def get_by_json(cls, data):
        query = "SELECT lat, lng FROM locations JOIN users ON locations.user_id = users.id WHERE locations.id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results

# get one JSON
    @classmethod
    def get_by_id_json(cls, data):
        query = "SELECT * FROM locations JOIN users ON locations.user_id = users.id WHERE locations.id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
        

# to get all locations on dashboard, needed join to display with user

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM locations JOIN users ON locations.user_id = users.id"
        results = connectToMySQL(DATABASE).query_db(query)
        if len(results) > 0:
            all_locations = []
            for row in results:
                this_location = cls(row)
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at']
                }
                this_user = users_model.User(user_data)
                this_location.create = this_user
                all_locations.append(this_location)
            return all_locations
        return []

# get all json

    @classmethod
    def get_all_JSON(cls):
        query = "SELECT location, lat, lng FROM locations JOIN users ON locations.user_id = users.id"
        results = connectToMySQL(DATABASE).query_db(query)
        return results

#DELETE location

    @classmethod
    def del_location(cls, data):
        query = "DELETE FROM locations WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

# VALIDATOR


    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['location']) < 3:
            flash("Location must have 3 characters")
            is_valid = False
        if len(form_data['time']) < 3:
            flash("Must have a valid time")
            is_valid = False
        if len(form_data['date']) < 1:
            flash("Date is Required")
            is_valid = False
        if len(form_data['weather']) < 1:
            flash("Must have number of Sasquatches")
            is_valid = False
        return is_valid
