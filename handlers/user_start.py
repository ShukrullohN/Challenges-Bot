from aiogram.dispatcher import FSMContext

from keyboards.default.user import user_main_menu, phone_number_share, location_share
from loader import dp, db
from aiogram import types

from states.user import RegisterState

@dp.message_handler(commands=['start'])
async def user_start(message: types.Message):
    if db.get_user_by_chat_id(chat_id=message.chat.id):
        text = "Assalomu alaykum, xush kelibsiz"
        await message.answer(text=text, reply_markup=user_main_menu)
    else:
        text = "Assalomu alaykum, ismingizni kiriting"
        await message.answer(text=text)
        await RegisterState.full_name.set()


@dp.message_handler(state=RegisterState.full_name)
async def get_full_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text, chat_id=message.chat.id)

    text = "Telefon raqam"
    await message.answer(text=text, reply_markup=phone_number_share)
    await RegisterState.phone_number.set()


@dp.message_handler(state=RegisterState.phone_number, content_types=types.ContentTypes.CONTACT)
async def get_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    
    data = await state.get_data()
    if db.add_user(data):
        text = "Muvaffaqiyatli ro'yhatdan o'tildi ✅"
    else:
        text = "Botda qandaydur muammo mavjud!"
    await message.answer(text=text, reply_markup=user_main_menu)
    await state.finish()