from flask import Flask, render_template, flash
from forms import LoginForm

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
def index():
	"""Renders the index template."""
	return render_template("index.html")

# this function accepts GET and POST requests
# both must be specified if you want more than GET
@app.route('/login', methods=['GET', 'POST'])
def login():
	"""Validates the login form.
	   If validated, redirects user to index."""
	form = LoginForm()
	# this does the validation work
	if form.validate_on_submit():
		# quick way to show message to users on the next page; here just used for debugging
		flash('Login requested for OpenID = %s, remember_me=%s' % (form.openid.data, str(form.remember_me.data)))
		# if it's all validated, redirect user to index
		return redirect('/index')
	# if it's not, render the login page
	return render_template('login.html', title='Sign In', form=form)

if __name__ == '__main__':
	app.run(debug=True)