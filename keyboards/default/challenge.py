from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

default_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='My Challenges')
        ],
        [
            KeyboardButton(text="Join a challange"),
            KeyboardButton(text='Settings')
        ]
    ], resize_keyboard=True
)