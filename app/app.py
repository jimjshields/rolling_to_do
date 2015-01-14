import sqlite3
from flask import Flask, render_template, flash, redirect
from contextlib import closing

app = Flask(__name__)
app.config.from_object('config')

### url routing/view functions ###

@app.route('/')
def index():
	"""Renders the index template."""
	return render_template("index.html")

@app.route('/to_do')
def show_to_do():
	"""Renders the user's to-do list."""
	# cur = g.db.execute('select to_do')

### database functions ###
def connect_db():
	"""Connects to the configured database."""
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	"""Initializes the database with the provided schema."""
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()
		print "Initialized the database."

@app.before_request
def before_request():
	"""Before the db request, connects to the database."""
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	"""After the db request, closes the connection,
	   and handles any exceptions."""
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()


if __name__ == '__main__':
	app.run()


# login - hold off until later
# from forms import LoginForm
# this function accepts GET and POST requests
# both must be specified if you want more than GET
# @app.route('/login', methods=['GET', 'POST'])
# def login():
# 	"""Validates the login form.
# 	   If validated, redirects user to index."""
# 	form = LoginForm()
# 	# this does the validation work
# 	if form.validate_on_submit():
# 		# quick way to show message to users on the next page; here just used for debugging
# 		flash('Login requested for OpenID = %s, remember_me=%s' % (form.openid.data, str(form.remember_me.data)))
# 		# if it's all validated, redirect user to index
# 		return redirect('/')
# 	# if it's not, render the login page
# 	return render_template('login.html', title='Sign In', form=form, providers=app.config['OPENID_PROVIDERS'])