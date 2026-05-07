from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import CATEGORIES


def buttons_category():
    buttons = []

    for category in CATEGORIES.keys():
        buttons.append([KeyboardButton(text=category)])

    markup = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=False,
    )
    return markup

