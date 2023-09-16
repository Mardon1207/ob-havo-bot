from dotenv import load_dotenv
import os

load_dotenv()
TOKEN="6425520521:AAFQ0HJkUvNF4Y94LnH7LiCfhAmA4o_XHNo"

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
)

from .handlers import (
    start,
    send_weather,
)

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

def register_handlers():
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.location, send_weather))

    updater.start_polling()
    updater.idle()