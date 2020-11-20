import flask
import stooq
import pika
from threading import Thread

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'

@app.route('/stock', methods=['GET'])
def stock():
    data = flask.request.args.get('ticker')
    return stooq.checkStock(data)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials("user", "password")))
channel = connection.channel()

def callback(ch, method, properties, body):
    data = body.decode("utf-8")
    res = stooq.checkStock(data)
    channel.basic_publish(exchange='my_exchange2', routing_key='test2', body=res)
    
channel.basic_consume(queue="my_app", on_message_callback=callback, auto_ack=True)

thread = Thread(target = channel.start_consuming)
thread.start()

if __name__ == '__main__':
    app.run(port=3000)