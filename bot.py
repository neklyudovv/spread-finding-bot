from telegram.ext import Application, Updater, CommandHandler, ConversationHandler
from config import TOKEN
from handlers import start, tracking_handler, stop


def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(tracking_handler)

    # Run bot
    application.run_polling(1.0)


if __name__ == "__main__":
    main()