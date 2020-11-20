import requests
import csv

def checkStock(inputContent):
    if inputContent == '':
        return 'ERR: Input is missing'

    data = inputContent.split('|')
    
    if len(data) != 3:
        return 'ERR: Wrong No of parameters'

    try:
        cmd =  data[0]
        ticker = data[1]
        room = data[2]

        if cmd != 'stock':
            return 'ERR: Command({}) not supported|{}'.format(cmd, room)

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