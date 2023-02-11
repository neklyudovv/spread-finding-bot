from telegram import Update
from telegram.ext.dispatcher import run_async
from telegram.ext import Updater, CallbackContext, Filters, MessageHandler, CommandHandler, ConversationHandler
from parser import parse
import os
from dotenv import load_dotenv
from time import sleep

WAIT_FOR_ITEM, WAIT_FOR_LINK, WAIT_FOR_TRACK_END, WHICH_TO_STOP = range(4)
global is_active
is_active = 0

def get_prices(ticker, sites=['bybit', 'exmo', 'binance', 'huobi']):
	prices = {}
	for site in sites:
		if site == 'bybit':
			prices['bybit'] = parse('bybit', ticker)
		if site == 'exmo':
			prices['exmo'] = parse('exmo', ticker)
		if site == 'binance':
			prices['binance'] = parse('binance', ticker)
		if site == 'huobi':
			prices['huobi'] = parse('huobi', ticker)
	return prices


def track(update: Update, context: CallbackContext, ticker='', sites=[]):
	try:
		prices = get_prices(ticker)
	except:
		update.message.reply_text(text='Такого тикера не существует | что-то пошло не так')
		return ConversationHandler.END
	*p, = prices
	s = ''
	for i in range(0, len(prices)):
		s += f'{p[i]} : {prices[p[i]]}\n'

	context.bot.sendMessage(chat_id=update.message.from_user['id'], text=s)
	while is_active != 0: # пока отслеживание активно
		sleep(2)
		prices = get_prices(ticker) # получаем свежие данные
		s = ''
		for i in range(0, len(prices)):
			for j in range(1, len(prices)):
				*p, = prices
				first = float(prices[p[i]])
				second = float(prices[p[j]])
				if max(first, second) > min(first, second):
					if ((max(first, second) - min(first, second))/min(first, second))*100 >= 2:
						s += f'{((max(first, second) - min(first, second))/min(first, second))*100}% : {first} ({p[i]}) - {second} ({p[j]}) \n'
		if s != '': # оповещаем пользователя при изменении
			context.bot.sendMessage(chat_id=update.message.from_user['id'], text=s)
	return None 


def start(update: Update, context: CallbackContext): # стартовая функция
	update.message.reply_text(text='trading tool bot - бот для нахождения разницы в 2% в курсах монет на разных биржах. Просто пришли мне тикер в формате BTC/USDT и я начну отслеживать изменения')
	return WAIT_FOR_LINK # запускает ожидание ссылки от пользователя


# def entry(update: Update, context: CallbackContext): # добавить новое отслеживание в случае если бот уже запущен
# 	update.message.reply_text(text='Пришли мне тикер, который хочешь отслеживать')
# 	return WAIT_FOR_LINK # запускает ожидание тикера от пользователя


def wait_for_link(update, _): # обработка ожидания тикера
	global ticker
	ticker = update.message.text
	sites = ''
	global is_active
	is_active = 1
	update.message.reply_text(text='Отлично! Я начал отслеживать '+ ticker + ' на следующих биржах:')# + {sites})
	track(update, _, ticker)
	return cancel(update, _)
	#return WAIT_FOR_ITEM

	

def cancel(update, _): # закрывает все ветки
	global is_active
	is_active = 0
	#update.message.reply_text(text='stopped')
	return ConversationHandler.END


def main():
	# Loading token from .env
	dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
	if os.path.exists(dotenv_path):
		load_dotenv(dotenv_path)
	ACCESS_TOKEN = os.getenv("TOKEN")
	updater = Updater(token=ACCESS_TOKEN, use_context=True)
	stop_handler = CommandHandler('stop', cancel)
	updater.dispatcher.add_handler(stop_handler)
    #start_handler = CommandHandler('start', start)
    #updater.dispatcher.add_handler(start_handler)  # start handler
    #updater.dispatcher.add_handler(MessageHandler(filters=Filters.all, callback=message_handler))  # all messages handler

	conv_handler = ConversationHandler( # здесь строится логика разговора
	        # точка входа в разговор
			#entry_points=[CommandHandler('new', entry), CommandHandler('start', start)],
			entry_points=[CommandHandler('start', start)],
	        # этапы разговора, каждый со своим списком обработчиков сообщений
			states={
			WAIT_FOR_LINK: [MessageHandler(Filters.all, wait_for_link)],
	           # WAIT_FOR_ITEM: [MessageHandler(Filters.all, wait_for_item)],        
			},
	        # точка выхода из разговора
			fallbacks=[CommandHandler('cancel', cancel)], 
			run_async=True,
	)
	updater.dispatcher.add_handler(conv_handler)
	updater.start_polling()
	updater.idle()


if __name__ == '__main__':
	main()
