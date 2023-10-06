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

from handlers import (
    start,
    send_location,
    send_weather,
    hudud,
    aloqa
)

updater = Updater(token=TOKEN)
dp = updater.dispatcher


dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.location, send_location))
dp.add_handler(MessageHandler(Filters.text("⛅️ Hozirgi ob-havo"), send_weather))
dp.add_handler(MessageHandler(Filters.text("📍 Hududni o'zgartirish"), hudud))
dp.add_handler(MessageHandler(Filters.text("📞 Aloqa"), aloqa))

updater.start_polling()
updater.idle()