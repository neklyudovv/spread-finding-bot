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

    await update.message.reply_text(f"Отслеживание {ticker} запущено на следующих биржах:\n" + str(get_prices(ticker)))
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