from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room, leave_room
import re 

app = Flask(__name__) 
app.debug = True
app.secret_key = '35ba1b653d97423f9bd67d3309bd012b'

socketio = SocketIO()
socketio.init_app(app)  
  
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
            return render_template('chat.html', name=account['username'], room=session['room'])
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

@app.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('username', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('login'))
    return render_template('chat.html', name=name, room=room)

### SocketIO Listeners ###

@socketio.on('joined', namespace='/chat')
def joined(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('username') + ' has entered the room.'}, room=room)

@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    emit('message', {'msg': session.get('username') + ':' + message['msg']}, room=room)
    if "/stock=" in message['msg']:
        stock = re.search('(?<=\/stock=).*?(?=\s)', message['msg'])
        print(stock.match)

@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)

if __name__ == "__main__":
    socketio.run(app)