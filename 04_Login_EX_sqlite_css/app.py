from flask import Flask, url_for, render_template
from flask import request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from service import blogopen

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

@app.errorhandler(404)
def page_not_found(error):
     return render_template('page_not_found.html'), 404

class User(db.Model):
	""" Create user table"""
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(80))
	email = db.Column(db.String(80), unique=True)

	def __init__(self, username, password, email):
		self.username = username
		self.password = password
		self.email = email

@app.route('/', methods=['GET', 'POST'])
def home():
	if not session.get('logged_in'):
		return render_template('index.html')
	else:
		if request.method == 'POST':
			username = request.form['username']
			return render_template('index.html', data=blogopen(username))
		return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	"""Login Form"""
	if request.method == 'GET':
		return render_template('login.html')
	else:
		name = request.form['username']
		passw = request.form['password']
		try:
			data = User.query.filter_by(username=name, password=passw).first()
			if data is not None:
				session['logged_in'] = True
				return redirect(url_for('home'))
			else:
				return 'Dont Login'
		except:
			return "Dont Login"

@app.route('/register/', methods=['GET', 'POST'])
def register():
	"""Register Form"""
	if request.method == 'POST':
		new_user = User(username=request.form['username'], password=request.form['password'], 
			email=request.form['email'])

		db.session.add(new_user)
		db.session.commit()
		return render_template('login.html')
	return render_template('register.html')

@app.route("/logout")
def logout():
	"""Logout Form"""
	session['logged_in'] = False
	return redirect(url_for('home'))

if __name__ == '__main__':
	db.create_all()
	app.secret_key = "123123123"
	app.run(host='0.0.0.0', debug=True)