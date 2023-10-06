from telegram import Bot
TOKEN="6425520521:AAFQ0HJkUvNF4Y94LnH7LiCfhAmA4o_XHNo"
bot = Bot(token=TOKEN)

def get_info():
    print(bot.get_webhook_info())


def delete():
    print(bot.delete_webhook())


def set():
    url = 'https://mardon1207.pythonanywhere.com/setwebhook/'
    print(bot.set_webhook(url=url))

set()