from flask import Flask, render_template, request, redirect, session, flash
# from config.config_files import Keys
app = Flask(__name__)
app.secret_key = "shhhhhhhhh"


DATABASE = 'fish_schema'

# api key = AIzaSyClKEEHbC22jQ60u5ti6AOD-KA14AbNSM8
