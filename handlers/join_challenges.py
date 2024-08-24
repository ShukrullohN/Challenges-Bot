from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, db
from aiogram.dispatcher.filters import Text


# Handler for "Join the Challenge" button
@dp.message_handler(Text(equals="Join the Challenge"))
async def join_challenge(message: types.Message):
    public_challenges = db.get_public_challenges()

    if not public_challenges:
        await message.answer("There are no public challenges available.")
        return

    for challenge in public_challenges:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Join", callback_data=f"join:{challenge.id}"))
        keyboard.add(InlineKeyboardButton("Details", callback_data=f"details:{challenge.id}"))

        await message.answer(
            f"Challenge: {challenge.name}\nStart: {challenge.start_at}\nEnd: {challenge.and_at}",
            reply_markup=keyboard
        )

    # Add "Join via Secret Key" option
    join_secret_key_keyboard = InlineKeyboardMarkup()
    join_secret_key_keyboard.add(InlineKeyboardButton("Join via Secret Key", callback_data="join_secret_key"))
    await message.answer("Or you can join using a secret key:", reply_markup=join_secret_key_keyboard)

# Handler for joining a challenge
@dp.callback_query_handler(lambda c: c.data and c.data.startswith("join:"))
async def process_join_challenge(callback_query: types.CallbackQuery):
    challenge_id = callback_query.data.split(":")[1]
    user_id = callback_query.from_user.id

    async with get_session() as session:
        # Check if the user is already a member
        existing_member = db.join_challenges(challenge_id, user_id)
        if existing_member:
            await callback_query.answer("You are already a member of this challenge.")
            return

        # Add the user as a member of the challenge
        result = db.add_member(challenge_id, user_id)

    if result == True:
        await callback_query.answer("You have successfully joined the challenge!")
        await callback_query.message.answer("Returning to the main menu.")
    else:
        await callback_query.answer("The bot has some problems")

# Handler for showing challenge details
@dp.callback_query_handler(lambda c: c.data and c.data.startswith("details:"))
async def show_challenge_details(callback_query: types.CallbackQuery):
    challenge_id = callback_query.data.split(":")[1]

    challenges = db.get_challenge_by_id(challenge_id)

    if not challenge:
        await callback_query.answer("Challenge not found.")
        return

    details_text = (
        f"Name: {challenge.name}\n"
        f"Start Date: {challenge.start_at}\n"
        f"End Date: {challenge.and_at}\n"
        f"limited_time: {challenge.limited_time} days\n"
        f"Tasks: {'Same tasks each day' if challenge.is_different else 'Different tasks each day'}\n"
        f"Created by: {challenge.owner}\n"
        f"Challenge is {'Public' if challenge.status else 'Private'}"
    )

    await callback_query.message.answer(details_text)

# Handler for joining a challenge via secret key
@dp.callback_query_handler(lambda c: c.data == "join_secret_key")
async def join_via_secret_key(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Please enter the secret key:")
    await FSMContext.set_state("enter_secret_key")

@dp.message_handler(state="enter_secret_key")
async def process_secret_key(message: types.Message, state: FSMContext):
    secret_key = message.text

    Challenge = db.search_challenge_via_secret_key(secret_key)

    if not challenge:
        await message.answer("Invalid secret key. Please try again.")
        await state.finish()
        return

    # Ask for the secret pass
    await state.update_data(challenge_id=challenge.id)
    await message.answer("Please enter the secret pass:")
    await state.set_state("enter_secret_pass")

@dp.message_handler(state="enter_secret_pass")
async def process_secret_pass(message: types.Message, state: FSMContext):
    secret_pass = message.text
    data = await state.get_data()
    challenge_id = data['challenge_id']
    user_id = message.from_user.id

    Challenge = db.check_secret_pass(challenge_id, secret_pass)

    if not challenge:
        await message.answer("Invalid secret pass. Please try again.")
        await state.finish()
        return

    result = db.add_member(challenge_id, user_id)

    if result == True:
        await callback_query.answer("You have successfully joined the challenge!")
        await callback_query.message.answer("Returning to the main menu.")
    else:
        await callback_query.answer("The bot has some problems")

    await state.finish()

