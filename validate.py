def validate_ticker(ticker:str, site:str):
	ticker = ticker.replace(' ', '')
	if ticker.count('/') == 0 and ticker.count("\\") == 0:
		return 'Тикер введен не в нужном формате'
	elif ticker.count('/') != 0:
		coin1 = ticker[0:ticker.find('/')]
		coin2 = ticker[ticker.find('/')+1:len(ticker)]
	else:
		coin1 = ticker[0:ticker.find('\\')]
		coin2 = ticker[ticker.find('\\')+1:len(ticker)]

	if site == 'bybit':
		return (coin1 + coin2).upper()
	if site == 'exmo':
		return f'{coin1.upper()}_{coin2.upper()}'
	if site == 'binance':
		return (coin1 + coin2).upper()
	if site == 'huobi':
		return coin1.lower() + coin2.lower()

	return -1