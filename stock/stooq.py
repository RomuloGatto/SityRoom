import requests
import csv

def checkStock(inputTicker):
    try:
        if inputTicker == '':
            return 'ERR: Input is missing'

        data = inputTicker.split('|')
        
        if len(data) != 2:
            return 'ERR: Wrong No of parameters'

        ticker = data[0]
        room = data[1]

        urlCSV = r'https://stooq.com/q/l/?s={}&f=sd2t2ohlcv&h&e=csv'.format(ticker)

        with requests.Session() as s:
            download = s.get(urlCSV)

            decoded_content = download.content.decode('utf-8')

            content = list(csv.reader(decoded_content.splitlines(), delimiter=','))
        
            realTicker = content[1][0]
            quoteClose = content[1][6]

            return '{} quote is ${} per share|{}'.format(realTicker, quoteClose, room)
    except Exception as e:
        return "ERR: " + str(e)