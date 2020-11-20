from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from threading import Thread, Lock
import requests
import datetime
import pika
import re 

app = Flask(__name__) 
app.debug = True
app.secret_key = '35ba1b653d97423f9bd67d3309bd012b'

socketio = SocketIO(app, logger=True, engineio_logger=True)
#socketio.init_app(app)  
  
### App Routes ###

@app.route('/') 
@app.route('/login', methods =['GET', 'POST']) 
def login(): 
    from functions.sqlquery import sql_query2

    msg = '' 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form: 
        username = request.form['username'] 
        password = request.form['password'] 
        room = request.form['room'] 
        cursor = sql_query2('SELECT * FROM data_table WHERE username = ? AND password = ?', (username, password)) 
        if len(cursor) > 0: 
            account = cursor[0]
            session['loggedin'] = True
            session['room'] = room
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
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form: 
        email = request.form['email']  
        username = request.form['username'] 
        password = request.form['password'] 
        cursor = sql_query2(''' SELECT * FROM data_table where username = ?''', (username,))
        if len(cursor) > 0: 
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', username): 
            msg = 'Username must contain only characters and numbers!'
        elif not re.search(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',email):
            msg = 'Email must be a valid one!'
        elif not username or not password or not email: 
            msg = 'Please fill out the form !'
        else: 
            sql_edit_insert('INSERT INTO data_table(email,username,password) VALUES (?, ?, ?)', (email,username,password)) 
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

@app.route('/rmq-redirect', methods=['GET'])
def sendBotReply():
    data = request.args.get('msg').split('|')
    message = data[0]
    room = data[1]

    dtMsg = datetime.datetime.now()
    curDate = '{}-{}-{}'.format(dtMsg.year, dtMsg.month, dtMsg.day)
    curTime = '{}:{}:{}'.format(dtMsg.hour, dtMsg.minute, dtMsg.second)
    
    emit('message', {'msg': curDate + ' ' + curTime + ' | ' + 'StooqBot' + ': ' +message}, room=room, namespace='/chat')

@socketio.on('joined', namespace='/chat')
def joined(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('username') + ' has entered the room.'}, room=room)
    
@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    dtMsg = datetime.datetime.now()
    curDate = '{}-{}-{}'.format(dtMsg.year, dtMsg.month, dtMsg.day)
    curTime = '{}:{}:{}'.format(dtMsg.hour, dtMsg.minute, dtMsg.second)

    emit('message', {'msg': curDate + ' ' + curTime + ' | ' + session.get('username') + ': ' + message['msg']}, room=room)
    if "/stock=" in message['msg']:
        stock = re.search('(?<=\/stock=).*?(?=\s)', message['msg'])
        sendMessageRabbitMQ('{}|{}'.format(message['msg'][stock.start():stock.end()], room))

@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('username') + ' has left the room.'}, room=room)

def sendMessageRabbitMQ(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials('user', 'password')))
    channel = connection.channel()
    channel.basic_publish(exchange='my_exchange', routing_key='test', body=message)
    connection.close()

### Consumer RabbitMQ

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials("user", "password")))
channel = connection.channel()

def callback(ch, method, properties, body):
    requests.get('http://localhost:5000/rmq-redirect?msg=' + body.decode("utf-8"))

channel.basic_consume(queue="my_app", on_message_callback=callback, auto_ack=True)

thread = Thread(target = channel.start_consuming)
thread.start() 

### Start API

if __name__ == "__main__":
    socketio.run(app)