from flask import Flask

# create app - a flask object of name __name__
app = Flask(__name__)
# the views module - for running the views of the app
from app import views