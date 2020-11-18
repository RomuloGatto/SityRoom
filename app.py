from flask import Flask, render_template, request, redirect, url_for, session
import re 

app = Flask(__name__) 
app.debug = True
app.secret_key = '35ba1b653d97423f9bd67d3309bd012b'

### App Routes ###

@app.route('/') 
@app.route('/login', methods =['GET', 'POST']) 
def login(): 
    from functions.sqlquery import sql_query2

    msg = '' 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form: 
        username = request.form['username'] 
        password = request.form['password'] 
        cursor = sql_query2('SELECT * FROM data_table WHERE username = ? AND password = ?', (username, password)) 
        if len(cursor) > 0: 
            account = cursor[0]
            session['loggedin'] = True
            session['room'] = 12345
            session['username'] = account['username'] 
            msg = 'Logged in successfully !'
        else: 
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg) 

@app.route('/logout') 
def logout(): 
    session.pop('loggedin', None) 
    session.pop('room', None) 
    session.pop('username', None) 
    return redirect(url_for('login')) 

@app.route('/register', methods =['GET', 'POST']) 
def register(): 
    from functions.sqlquery import sql_query2, sql_edit_insert

    msg = '' 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'first_name' in request.form and 'last_name' in request.form : 
        first_name = request.form['first_name']  
        last_name = request.form['last_name'] 
        username = request.form['username'] 
        password = request.form['password'] 
        cursor = sql_query2(''' SELECT * FROM data_table where username = ?''', (username,))
        if len(cursor) > 0: 
            msg = 'Account already exists !'
        elif not re.match(r'[A-Za-z0-9]+', username): 
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not first_name or not last_name: 
            msg = 'Please fill out the form !'
        else: 
            sql_edit_insert('INSERT INTO data_table(first_name,last_name,username,password) VALUES (?, ?, ?, ?)', (first_name,last_name,username,password)) 
            msg = 'You have successfully registered !'
    elif request.method == 'POST': 
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg) 
