# imports app from __init__ - there the name is designated as app
from app import app
from flask import render_template

@app.route('/')
def index():
	return render_template('index.html')