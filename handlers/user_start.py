from aiogram.dispatcher import FSMContext

from keyboards.default.user import phone_number_share
from keyboards.default.challenge import default_keyboard
from loader import dp, db
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from states.user import RegisterState

@dp.message_handler(commands=['start'])
async def user_start(message: types.Message):
    if db.get_user_by_chat_id(chat_id=message.chat.id):
        text = "Assalomu alaykum, xush kelibsiz"
        await message.answer(text=text, reply_markup=default_keyboard)
    else:
        text = "Assalomu alaykum, ismingizni kiriting"
        await message.answer(text=text)
        await RegisterState.first_name.set()


@dp.message_handler(state=RegisterState.first_name)
async def get_first_name(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text, chat_id=message.chat.id)

    text = "Familyangizni kiriting"
    await message.answer(text=text)
    await RegisterState.last_name.set()


@dp.message_handler(state=RegisterState.last_name)
async def get_last_name(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    text = 'Username kiriting'
    await message.answer(text=text)
    await RegisterState.username.set()
    


@dp.message_handler(state=RegisterState.username)
async def get_username(message: types.Message, state=FSMContext):
    if db.check_username(message.text):
        text = "Bunday username mavjud"
        await message.answer(text=text)
        return get_username(message=types.Message, state=FSMContext)
    await state.update_data(username=message.text)
    text = "Telefon raqamingizni kiriting"
    await message.answer(text=text, reply_markup=phone_number_share)
    await RegisterState.phone_number.set()

@dp.message_handler(state=RegisterState.phone_number, content_types=types.ContentTypes.CONTACT)
async def get_phone_number(message: types.Message, state=FSMContext):
    await state.update_data(phone_number=message.text)

    data = await state.get_data()
    if db.add_user(data):
        text = "Muvaffaqiyatli ro'yhatdan o'tildi ✅"
    else:
        text = "Botda qandaydur muammo mavjud!"
    await message.answer(text=text, reply_markup=default_keyboard)
    await state.finish()