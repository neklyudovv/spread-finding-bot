from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler
import asyncio
from utils.tracker import track_price
from utils.parser import get_prices


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привет! Отправь тикер в формате BTC/USDT")


async def track(update: Update, context: CallbackContext):
    ticker = update.message.text
    context.user_data['is_active'] = True

    context.user_data['task'] = asyncio.create_task(track_price(update, context, ticker))
    s = f"Отслеживание {ticker} запущено на следующих биржах:\n"
    prices = get_prices(ticker)
    for item in prices:
        s += f"{item}: {prices[item]}\n"
    await update.message.reply_text(s)
    return ConversationHandler.END


async def stop(update: Update, context: CallbackContext):
    context.user_data['is_active'] = False

    if 'task' in context.user_data:
        context.user_data['task'].cancel()

    await update.message.reply_text("Отслеживание остановлено.")


tracking_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, track)],
    states={},
    fallbacks=[],
)