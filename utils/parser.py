import requests
from utils.validate import validate_ticker


def get_prices(ticker, exchanges):
    prices = {}
    for exchange in exchanges:
        prices[exchange] = parse(exchange, ticker)
    return prices


def parse(url, coin=''):
    if url == 'exmo':
        coin = validate_ticker(coin, 'exmo')
        if coin == -1:
            return 'no such ticker'
        r = requests.post('https://api.exmo.me/v1.1/ticker',
                          headers={'Content-Type': 'application/x-www-form-urlencoded'})
        try:
            return float(r.json()[coin]['sell_price'])
        except:
            return 'no such coin | exmo // something went wrong'
    if url == 'binance':
        coin = validate_ticker(coin, 'binance')
        if coin == -1:
            return 'no such ticker'
        r = requests.get('https://www.binance.com/api/v3/ticker/price')
        for i in range(0, len(r.json())):
            if r.json()[i]['symbol'] == coin:
                return round(float(r.json()[i]['price']), 2)
        return 'no such coin | binance // something went wrong'
    if url == 'huobi':
        coin = validate_ticker(coin, 'huobi')
        if coin == -1:
            return 'no such ticker'
        r = requests.get('https://api.huobi.pro/market/tickers')
        for arr in r.json()['data']:
            if arr['symbol'] == coin:
                return arr['ask']
    return -1
