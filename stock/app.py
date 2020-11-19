import flask
import stooq

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'

@app.route('/stock', methods=['GET'])
def stock():
    return stooq.checkStock(flask.request.args.get('ticker'))

if __name__ == '__main__':
    app.run(port=3000)