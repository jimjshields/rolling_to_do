from app import app

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

	today = datetime.strptime(show_date, "%m-%d-%Y")
	yesterday = stringify_date(today - timedelta(days=1))
	tomorrow = stringify_date(today + timedelta(days=1))
	today = stringify_date(today)

	today_cur = g.db.execute('select item, entry_time, is_completed, completed_time from to_dos where entry_time = ? and is_completed = 0', [show_date])
	today_to_dos = [dict(item=row[0], entry_time=row[1], is_completed=row[2], completed_time=row[3]) for row in today_cur.fetchall()]

	past_cur = g.db.execute('select item, entry_time, is_completed, completed_time from to_dos where entry_time < ? and is_completed = 0', [show_date])
	past_to_dos = [dict(item=row[0], entry_time=row[1], is_completed=row[2], completed_time=row[3]) for row in past_cur.fetchall()]

	today_completed_cur = g.db.execute('select item, entry_time, is_completed, completed_time from to_dos where completed_time = ? and is_completed = 1', [show_date])
	today_completed_to_dos = [dict(item=row[0], entry_time=row[1], is_completed=row[2], completed_time=row[3]) for row in today_completed_cur.fetchall()]
	
	return render_template('to_dos.html', today_to_dos=today_to_dos, past_to_dos=past_to_dos, today_completed_to_dos=today_completed_to_dos, today=today, yesterday=yesterday, tomorrow=tomorrow)

@app.route('/to_do/add', methods=['POST'])
def add_to_do():
	"""Adds a to-do from the form to the to-do list."""
	today = stringify_date(datetime.now())
	g.db.execute('insert into to_dos (item, entry_time, is_completed, completed_time) values (?, ?, ?, ?)',
				 [request.form['item'], today, False, 'NULL'])
	g.db.commit()
	# flash('New entry was successfully posted.')
	return redirect(url_for('show_to_dos', show_date='today'))

@app.route('/to_do/update', methods=['POST'])
def update_to_do():
	"""Either completes or deletes all checked to-dos.
	   Checks whether the button pressed is 'Complete' or 'Delete.'"""
	
	checked_items = [item[0] for item in request.form.items()]
	today = stringify_date(datetime.now())
	button = request.form['btn']
	
	for item in checked_items:
		if button == 'Complete':
			g.db.execute('update to_dos set is_completed = ?, completed_time = ? where item = ?;',
						 [True, today, item])
			g.db.commit()
		elif button == 'Delete':
			g.db.execute('delete from to_dos where item = ?;',
					 [item])
			g.db.commit()
	return redirect(url_for('show_to_dos', show_date='today'))