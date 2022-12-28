from flask_app.controllers import locations_controller, users_controller
from flask_app import app
# from config.config_files import Keys
# URL = "https://maps.googleapis.com/maps/api/js?key=" + Keys.GoogleAPI

if __name__ == "__main__":
    app.run(debug=True)



