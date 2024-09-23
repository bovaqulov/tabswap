from telebot import types
from telebot.types import InlineKeyboardButton, WebAppInfo

from tapswap.settings import FRONTEND_HOST


def start_inline_btn():
    markup = types.InlineKeyboardMarkup()
    url = f"{FRONTEND_HOST}/telegram-user/"
    markup.add(InlineKeyboardButton("Start 💫", web_app=WebAppInfo(url=url)))
    return markup

