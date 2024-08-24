from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Handler for the "Settings" button
@dp.message_handler(Text(equals="Settings"))
async def settings(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Change first_name", callback_data="change_first_name"))
    keyboard.add(InlineKeyboardButton("Change last_name", callback_data="change_last_name"))
    keyboard.add(InlineKeyboardButton("Change Phone Number", callback_data="change_phone"))
    keyboard.add(InlineKeyboardButton("Change Username", callback_data="change_username"))

    await message.answer("What would you like to change?", reply_markup=keyboard)

# Handlers for changing user details
@dp.callback_query_handler(lambda c: c.data == "change_first_name")
async def change_first_name(callback_query: types.CallbackQuery, state=FSMContext):
    await callback_query.message.answer("Please enter your new first_name:")
    await state.set_state("change_first_name")

@dp.message_handler(state="change_first_name")
async def update_first_name(message: types.Message, state: FSMContext):
    new_first_name = message.text
    user_id = message.from_user.id

    db.update_first_name(new_first_name, user_id)

    await message.answer("Your first_name has been updated!")
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == "change_last_name")
async def change_last_name(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Please enter your new last name:")
    await state.set_state("change_last_name")  # Correct way to set the state

@dp.message_handler(state="change_last_name")
async def update_last_name(message: types.Message, state: FSMContext):
    new_last_name = message.text
    user_id = message.from_user.id

    db.update_last_name(new_last_name, user_id)
    await message.answer("Your last name has been updated!")
    await state.finish()  # Finish the state when done

@dp.callback_query_handler(lambda c: c.data == "change_phone")
async def change_phone(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Please enter your new phone number:")
    await state.set_state("change_phone")

@dp.message_handler(state="change_phone")
async def update_phone(message: types.Message, state: FSMContext):
    new_phone = message.text
    user_id = message.from_user.id

    db.update_phone_number(new_phone, user_id)

    await message.answer("Your phone number has been updated!")
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == "change_username")
async def change_username(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Please enter your new username:")
    await state.set_state("change_username")

@dp.message_handler(state="change_username")
async def update_username(message: types.Message, state: FSMContext):
    new_username = message.text
    user_id = message.from_user.id

    db.update_username(new_username, user_id)
    await message.answer("Your username has been updated!")
    await state.finish()
