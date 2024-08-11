from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Mening Chellenjlarim"),
            KeyboardButton(text="Chellenjga qo'shilish"),
        ]
    ], resize_keyboard=True
)

phone_number_share = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Telefon raqam jo'natish", request_contact=True)
        ]
    ], resize_keyboard=True
)

