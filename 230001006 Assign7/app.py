from flask import Flask, render_template, request as req, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = "aiqw179"
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "root"
app.config['MYSQL_DB'] = 'IITI_Website'
app.config['MYSQL_PORT'] = int(3307)

mysql = MySQL(app)
@app.route('/')   
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if req.method == 'POST' and 'username' in req.form and 'password' in req.form:
		username = req.form['username']
		password = req.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('select * from user where username = % s and password = % s', (username, password, ))
		acc = cursor.fetchone()
		if acc:
			session['loggedin'] = True
			session['id'] = acc['user_id']
			session['username'] = acc['username']
			session['mobile'] = acc['mobile']
			msg = 'Logged in successfully !'
			return render_template('index.html', msg = msg,username = session['username'])
		else:
			msg = 'User does not exists'
	return render_template('login.html', msg = msg)

@app.route('/signup', methods=['GET', 'POST'])
def signup(): 
    msg = ''
    if req.method == 'POST' and 'username' in req.form and 'password' in req.form and 'mobile' in req.form:
        username = req.form['username']
        password = req.form['password']
        mobile = req.form['mobile']
        if not re.match(r'^[0-9]{10}$', mobile):
            msg = 'Mobile number must contain exactly 10 digits!'
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO user VALUES (NULL, %s, %s, %s)', (username, mobile, password))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return redirect(url_for('login'))
    elif req.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('signup.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('mobile', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True, port=6969)