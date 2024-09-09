from telegram import Update
from telegram.ext import Updater, CallbackContext, Filters, MessageHandler, CommandHandler, ConversationHandler
from parser import parse
import os
from dotenv import load_dotenv
from time import sleep

WAIT_FOR_ITEM, WAIT_FOR_TICKER = range(2)  # conv handler


def get_prices(ticker:str, sites=['exmo', 'binance', 'huobi']):
    prices = {}
    for site in sites:
        prices[site] = parse(site, ticker)
    return prices


def track(update: Update, context: CallbackContext, ticker='', track_id=0):
    prices = get_prices(ticker)
    try:
        prices = get_prices(ticker)
    except:
        update.message.reply_text(text='Такого тикера не существует | что-то пошло не так')
        return ConversationHandler.END
    *p, = prices
    s = ticker + '\n'
    for i in range(0, len(prices)):
        s += f'{p[i]} : {prices[p[i]]}\n'

    context.bot.sendMessage(chat_id=update.message.from_user['id'], text=s)
    try:
        while context.user_data['is_active'][track_id] != 0:  # пока отслеживание активно
            prices = get_prices(ticker)  # получаем свежие данные
            s = ''
            for i in range(0, len(prices)):
                for j in range(1, len(prices)):
                    *p, = prices
                    first, second = float(prices[p[i]]), float(prices[p[j]])
                    maxprice, minprice = max(first, second), min(first, second)
                    if maxprice > minprice:
                        percentage = (maxprice - minprice) / minprice * 100
                        if percentage >= 2:
                            s += f'{percentage}% : {first} ({p[i]}) - {second} ({p[j]}) \n'
            if s != '':  # оповещаем пользователя при изменении
                context.bot.sendMessage(chat_id=update.message.from_user['id'], text=s)
            sleep(2)
    except:
        print('stopped idcc')
        return None
    return None


def start(update: Update, context: CallbackContext):  # стартовая функция
    if 'is_active' not in context.user_data.keys():
        context.user_data['is_active'] = []
    update.message.reply_text(text='trading tool bot - бот для нахождения разницы в >2% в курсах монет на разных '
                                   'биржах. Пришли мне тикер в формате BTC/USDT и я начну отслеживать изменения')
    return WAIT_FOR_TICKER  # запускает ожидание ссылки от пользователя


def wait_for_ticker(update, context):  # обработка ожидания тикера
    ticker = update.message.text
    sites = ''  # TODO
    print(context.user_data['is_active'])
    context.user_data['is_active'].append(1)
    update.message.reply_text(text='Я начал отслеживать ' + ticker + ' на следующих биржах:')  # + {sites})
    track(update, context, ticker, len(context.user_data['is_active']) - 1)
    return cancel(update, context)


def cancel(update, context):
    return ConversationHandler.END


def stop(update, context):  # закрывает все ветки
    msg = update.message.text
    if msg.replace(' ', '') == '/stop':
        update.message.reply_text(context.user_data['is_active'])
    else:
        track_id = msg.replace('/stop', '').replace(' ', '')
        context.user_data['is_active'][int(track_id) - 1] = 0
        update.message.reply_text(text=f'Отслеживание #{track_id} остановлено')
    # update.message.reply_text(text='stopped')
    # update.message.reply_text(text='incorrect data')


# return ConversationHandler.END


def main():
    # Loading token from .env
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    ACCESS_TOKEN = os.getenv("TOKEN")
    updater = Updater(token=ACCESS_TOKEN, use_context=True)
    stop_handler = CommandHandler('stop', stop)
    updater.dispatcher.add_handler(stop_handler)
    # start_handler = CommandHandler('start', start) updater.dispatcher.add_handler(start_handler)  # start handler
    # updater.dispatcher.add_handler(MessageHandler(filters=Filters.all, callback=message_handler))  # all messages
    # handler

    conv_handler = ConversationHandler(  # здесь строится логика разговора
        # точка входа в разговор
        # entry_points=[CommandHandler('new', entry), CommandHandler('start', start)],
        entry_points=[CommandHandler('start', start)],
        # этапы разговора, каждый со своим списком обработчиков сообщений
        states={
            WAIT_FOR_TICKER: [MessageHandler(Filters.all, wait_for_ticker)],
            # WAIT_FOR_SITES: [MessageHandler(Filters.all, wait_for_item)],
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
