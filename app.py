from flask import Flask, request
from telegram.ext import Dispatcher
from telegram import Bot, Update

from telegram.ext import (
    Updater, 
    MessageHandler, 
    CommandHandler, 
    CallbackQueryHandler, 
    Filters, 
    )
TOKEN="6425520521:AAFQ0HJkUvNF4Y94LnH7LiCfhAmA4o_XHNo"

from handlers import (
    start,
    send_location,
    send_weather,
    hudud,
    aloqa
)


app = Flask(__name__)

@app.route("/obhavo/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
    
        bot = Bot(TOKEN)
        dp = Dispatcher(bot, None, workers=0)
        data = request.get_json()
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(MessageHandler(Filters.location, send_location))
        dp.add_handler(MessageHandler(Filters.text("⛅️ Hozirgi ob-havo"), send_weather))
        dp.add_handler(MessageHandler(Filters.text("📍 Hududni o'zgartirish"), hudud))
        dp.add_handler(MessageHandler(Filters.text("📞 Aloqa"), aloqa))

        update = Update.de_json(data, bot)
        
        dp.process_update(update)

        print("OK")
        return "ok"
    
    else:
        return "Not allowed GET request"