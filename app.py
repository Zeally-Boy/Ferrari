from flask import Flask, render_template, request, redirect, url_for, session, logging
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
 
 
app = Flask(__name__)
 

 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'data'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
 
mysql = MySQL(app)
 
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'fullname' in request.form and 'password' in request.form:
        fullname = request.form['fullname']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM log WHERE fullname = % s AND password = % s', (fullname, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['fullname'] = account['fullname']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect fullname / password !'
    return render_template('login.html', msg = msg)
 
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('fullname', None)
    return redirect(url_for('login'))
 
@app.route('/register', methods =['GET','POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'fullname' in request.form and 'password' in request.form and 'email' in request.form :
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO log VALUES (NULL, % s, % s, % s)', (fullname, email, password ))
        mysql.connection.commit()
        cursor.close()
        msg = 'You have successfully registered !'
    # elif request.method == 'POST':
    #     msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=False, host='0.0.0.0')