from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterState(StatesGroup):
    first_name = State()
    last_name = State()
    username = State()
    phone_number = State()

