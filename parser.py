import requests
from pybit import spot
from validate import validate_ticker

def parse(url, coin=''):
	if url == 'bybit':
		coin = validate_ticker(coin, 'bybit')
		if coin == -1:
			return 'no such ticker'
		session = spot.HTTP(endpoint='https://api.bybit.com')
		symbol = session.orderbook(symbol=coin)
		return symbol['result']['asks'][0][0]
	if url == 'exmo':
		coin = validate_ticker(coin, 'exmo')
		if coin == -1:
			return 'no such ticker'
		r = requests.post('https://api.exmo.me/v1.1/ticker', headers={'Content-Type': 'application/x-www-form-urlencoded'})
		try:
			return r.json()[coin]['sell_price']
		except:
			return 'no such coin | exmo // something went wrong'
	if url == 'binance':
		coin = validate_ticker(coin, 'binance')
		if coin == -1:
			return 'no such ticker'
		r = requests.get('https://data.binance.com/api/v3/ticker/price')
		for i in range(0, len(r.json())):
			if r.json()[i]['symbol'] == coin:
				return r.json()[i]['price']
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