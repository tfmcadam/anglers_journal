# model the class after the friend table from our database
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import locations_model
from flask_app import DATABASE
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DATABASE = 'fish_schema'


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# CREATE USER

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL(DATABASE).query_db(query, data)

# GET USER BY ID
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users LEFT JOIN locations on users.id = locations.user_id WHERE users.id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) > 0:
            user = cls(results[0])
            list_of_locations = []
            for row in results:
                if row['locations.id'] == None:
                    break
                location_data = {
                    **row,
                    'id': row['locations.id'],
                    'created_at': row['locations.created_at'],
                    'updated_at': row['locations.updated_at'],
                }
                this_location = locations_model.Location(location_data)
                list_of_locations.append(this_location)
            user.locations = list_of_locations
            return user
        return False

        # GET USER BY ID JSON
    @classmethod
    def get_by_id_json(cls, data):
        query = "SELECT lat, lng FROM locations WHERE user_id = %(user_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results


#CALL USERS EMAIL 

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) > 0:
            return cls(results[0])
        return False

# VALIDATOR WITH EMAIL CHECK AND PASSWORD

    @staticmethod
    def validator(potential_user):
        print(potential_user)
        is_valid = True
        if len(potential_user['first_name']) < 2:
            flash("First name is must be 2 characters", "reg")
            is_valid = False

        if len(potential_user['last_name']) < 2:
            flash("Last name must be 2 characters", "reg")
            is_valid = False

# VALIDATE EMAIL

        if len(potential_user['email']) < 1:
            flash("Email is required", "reg")
            is_valid = False
        elif not EMAIL_REGEX.match(potential_user['email']):
            flash("Email must be valid", "reg")
            is_valid = False
        else:
            data = {
                'email' : potential_user['email'] 
            }
            user_in_db = User.get_by_email(data)
            if user_in_db:
                flash('Email already registered', "reg")
                is_valid = False

#VALIDATE PASSWORD 

        if len(potential_user['password']) < 8:
            flash("Password is must be 8 characters", "reg")
            is_valid = False
        elif potential_user['password'] != potential_user['confirm_pass']:
            flash("double check your password confirmation", "reg")
            is_valid = False
        return is_valid
