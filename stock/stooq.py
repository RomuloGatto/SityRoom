import requests
import csv

def checkStock(inputTicker):
    try:
        if inputTicker == '':
            return 'ERR: input ticker is missing'

        urlCSV = 'https://stooq.com/q/l/?s={}&f=sd2t2ohlcv&h&e=csv'.format(inputTicker)

        with requests.Session() as s:
            download = s.get(urlCSV)

            decoded_content = download.content.decode('utf-8')

            content = list(csv.reader(decoded_content.splitlines(), delimiter=','))
        
            realTicker = content[1][0]
            quoteClose = content[1][6]

            return '{} quote is ${} per share'.format(realTicker, quoteClose)
    except Exception as e:
        return "ERR: " + str(e)