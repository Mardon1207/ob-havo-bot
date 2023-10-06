from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext
import os
import requests
from .temp import FORECAST_TAMP
from .db import DB,LOC

db = DB('db.json')
loc=LOC('location.json')
API_KEY="e103948f1d6901c91a9f0781706e976b"


def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    user = update.effective_user

    keyboard_karkup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='📍 Location', request_location=True)]
        ],
        resize_keyboard=True
    )
    
    if db.is_user(user.id):
        update.message.reply_text(
            text=f"Hi {user.first_name}! Welcome back to the bot!\n\nsend your location",
            reply_markup=keyboard_karkup
        )
    else:
        db.add_user(user.id, user.first_name, user.last_name, user.username)
        update.message.reply_text(
            text=f"Hello {user.first_name}! Welcome to the bot!\n\nsend your location",
            reply_markup=keyboard_karkup
        )


def send_location(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    chat_id=update.message.chat.id
    location = update.message.location
    lat=location.latitude
    lon=location.longitude
    loc.save(chat_id=chat_id,lat=lat,lon=lon)
    keyboard=ReplyKeyboardMarkup([
        [KeyboardButton(text="⛅️ Hozirgi ob-havo")],
        [KeyboardButton(text="🕔 Soatlik ob-havo"),KeyboardButton(text="🗓 Haftalik ob-havo")],
        [KeyboardButton(text="📍 Hududni o'zgartirish")],
        [KeyboardButton(text="📞 Aloqa")]
        ],resize_keyboard=True)
    update.message.reply_text(
        text=f"Select the desired command👇🏻",
        reply_markup=keyboard
    )

def send_weather(update: Update, context: CallbackContext):
    chat_id=update.message.chat.id
    data=loc.lakatsiya(str(chat_id))
    payload = {
        "lat" : data['lat'],
        "lon": data['lon'],
        "appid" : API_KEY
    }  
    response = requests.get(url="https://api.openweathermap.org/data/2.5/weather", params=payload)
    data = response.json()
    if data["cod"] == 200:
        update.message.reply_text(
            text=FORECAST_TAMP.format(
                date=update.message.date.strftime("%A, %d-%B"),
                city=data["name"],
                description=data["weather"][0]["description"],
                temp=data["main"]["temp"] - 273.15,
                feels_like=data["main"]["feels_like"] - 273.15,
                clouds=data["clouds"]["all"],
                humidity=data["main"]["humidity"],
                wind=data["wind"]["speed"]
            )
        )
    
    else:
        update.message.reply_text(
            text=f"The city {update.message.text} doesn't exist."
        )

def hudud(update: Update, context: CallbackContext):
    chat_id=update.message.chat.id
    keyboard_karkup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='📍 Location', request_location=True)]
        ],
        resize_keyboard=True
    )
    update.message.reply_text(
        text=f"send your location!!!",
        reply_markup=keyboard_karkup
    )

def aloqa(update: Update, context: CallbackContext):
    user=update.effective_user
    text=f"""Assalomu alaykum {user.full_name}
Ob-havo botiga hush kelibsiz

🚀 Bu bot orqali O'zbekistonnig barcha hududlaridagi ob-havo ma'lumotini ko'rishingiz mumkin. Bot sizga foyda keltirsa biz hursand bo'lamiz. 

Bot orqali siz, hududingizdagi 3 xil obhavo ma'lumotni bilishingiz mumkin

1️⃣ Hozirgi ob-havo ✅
2️⃣ Haftalik ob-havo ❌ 
3️⃣ Soatlik ob-havo ❌ 

📩 Takliflaringiz bo'lsa @S_M_M_1207 ga yuborishingiz mumkin.

Qilgan ishlarimiz va foaliyatimiz haqida shu kanalda tanishish mumkin
👉 @S_M_M_1207_blog

Foydali deb bilgan bo'lsangiz yaqinlaringizga ham ulashing"""
    update.message.reply_text(text=text)