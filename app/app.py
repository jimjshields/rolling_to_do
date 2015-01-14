import sqlite3
from flask import Flask, request, render_template, g, flash, url_for, redirect
from contextlib import closing
from datetime import datetime, date

# configuration - figure out later how to port into separate file
DATABASE = '/tmp/db.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

### url routing/view functions ###

@app.route('/')
def index():
	"""Renders the index template."""
	return render_template("index.html")

@app.route('/to_do/<show_date>')
def show_to_dos(show_date):
	"""Renders the user's to-do list."""
	if show_date == 'today':
		show_date = stringify_date(datetime.now())

	today_cur = g.db.execute('select item, entry_time, is_completed, completed_time from to_dos where entry_time = ? and is_completed = 0', [show_date])
	today_to_dos = [dict(item=row[0], entry_time=row[1], is_completed=row[2], completed_time=row[3]) for row in today_cur.fetchall()]

	past_cur = g.db.execute('select item, entry_time, is_completed, completed_time from to_dos where entry_time < ? and is_completed = 0', [show_date])
	past_to_dos = [dict(item=row[0], entry_time=row[1], is_completed=row[2], completed_time=row[3]) for row in past_cur.fetchall()]

	today_completed_cur = g.db.execute('select item, entry_time, is_completed, completed_time from to_dos where completed_time = ? and is_completed = 1', [show_date])
	today_completed_to_dos = [dict(item=row[0], entry_time=row[1], is_completed=row[2], completed_time=row[3]) for row in today_completed_cur.fetchall()]
	
	return render_template('to_dos.html', today_to_dos = today_to_dos, past_to_dos = past_to_dos, today_completed_to_dos = today_completed_to_dos)

@app.route('/to_do/add', methods=['POST'])
def add_to_do():
	"""Adds a to-do from the form to the to-do list."""
	today = stringify_date(datetime.now())
	g.db.execute('insert into to_dos (item, entry_time, is_completed, completed_time) values (?, ?, ?, ?)',
				 [request.form['item'], today, False, 'NULL'])
	g.db.commit()
	flash('New entry was successfully posted.')
	return redirect(url_for('show_to_dos', show_date='today'))

@app.route('/to_do/complete', methods=['POST'])
def complete_to_do():
	"""Changes a checked to-do to completed."""
	completed_items = [item[0] for item in request.form.items()]
	today = stringify_date(datetime.now())
	for item in completed_items:
		g.db.execute('update to_dos set is_completed = ?, completed_time = ? where item = ?;',
					 [True, today, item])
		g.db.commit()
	return redirect(url_for('show_to_dos', show_date='today'))

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

### utility functions ###
def stringify_date(date):
	return date.strftime('%m-%d-%Y')

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