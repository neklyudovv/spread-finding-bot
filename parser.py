import requests
from pybit import spot
from validate import validate_ticker

def parse(url, coin=''):
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
		r = requests.get('https://www.binance.com/api/v3/ticker/price')
		print(r.json())
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