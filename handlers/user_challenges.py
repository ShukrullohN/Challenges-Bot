from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, db
from states.challenge import ChallengeCreation
from datetime import datetime, timedelta

# Display "My Challenges" with options to add tasks or modify challenges
@dp.message_handler(Text(equals="My Challenges"))
async def my_challenges(message: types.Message):
    user_id = message.from_user.id
    challenges = db.get_created_challenges(user_id)
    if not challenges:
        await message.answer("You haven't created any challenges yet.")
        return

    for challenge in challenges:
        keyboard = InlineKeyboardMarkup()
        if challenge.is_different:
            keyboard.add(InlineKeyboardButton("Add Task", callback_data=f"add_task:{challenge.id}"))
        else:
            keyboard.add(InlineKeyboardButton("Write Task for All Days", callback_data=f"write_task:{challenge.id}"))
        
        keyboard.add(InlineKeyboardButton("Change Challenge", callback_data=f"change_challenge:{challenge.id}"))
        
        await message.answer(
            f"Challenge: {challenge.name}\nfull_time: {challenge.start_at} - {challenge.end_at}",
            reply_markup=keyboard
        )

    # Add option to create a new challenge
    create_challenge_keyboard = InlineKeyboardMarkup()
    create_challenge_keyboard.add(InlineKeyboardButton("Create New Challenge", callback_data="create_new_challenge"))
    await message.answer("Or you can create a new challenge:", reply_markup=create_challenge_keyboard)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("add_task:"))
async def add_task(callback_query: types.CallbackQuery, state: FSMContext):
    challenge = callback_query.data.split(":")[1]
    async with get_session() as session:
        challenge = await session.execute(f"SELECT * FROM challenges WHERE id = {challenge}")
        challenge = challenge.fetchone()

    if not challenge:
        await callback_query.answer("Challenge not found.")
        return

    # Calculate the available task days
    task_limited_time = challenge.limited_time
    start_at = challenge.start_at

    # Get all tasks already added
    async with get_session() as session:
        tasks = await session.execute(f"SELECT * FROM tasks WHERE challenge = {challenge}")
        tasks = tasks.fetchall()

    existing_due_dates = {task.due_date for task in tasks}
    
    # Generate keyboard for available task days
    keyboard = InlineKeyboardMarkup()
    current_day = start_at
    while current_day <= challenge.end_at:
        if current_day not in existing_due_dates:
            keyboard.add(InlineKeyboardButton(str(current_day), callback_data=f"select_task_date:{challenge}:{current_day}"))
        current_day += task_limited_time

    await callback_query.message.answer("Select a date to add a task:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("select_task_date:"))
async def select_task_date(callback_query: types.CallbackQuery, state: FSMContext):
    _, challenge, due_date = callback_query.data.split(":")
    await state.update_data(challenge=challenge, due_date=due_date)
    await callback_query.message.answer("Please send the task description for this date:")
    await state.set_state("adding_task_description")

@dp.message_handler(state="adding_task_description")
async def add_task_description(message: types.Message, state: FSMContext):
    task_description = message.text
    data = await state.get_data()
    challenge = data['challenge']
    due_date = data['due_date']

    async with get_session() as session:
        new_task = Task(
            challenge=challenge,
            due_date=due_date,
            task_description=task_description
        )
        session.add(new_task)
        await session.commit()

    await message.answer("Task added successfully!")
    await state.finish()





@dp.message_handler(commands=["create_challenge"])
async def create_challenge(message: types.Message):
    await message.answer("Let's create a new challenge! What's the name of the challenge?")
    await ChallengeCreation.name.set()

@dp.message_handler(state=ChallengeCreation.name)
async def set_challenge_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text, owner=message.from_user.id)
    await message.answer("What is the challenge about?")
    await ChallengeCreation.info.set()

@dp.message_handler(state=ChallengeCreation.info)
async def set_challenge_name(message: types.Message, state: FSMContext):
    await state.update_data(info=message.text)
    await message.answer("What is the goal of the challenge?")
    await ChallengeCreation.goal.set()

@dp.message_handler(state=ChallengeCreation.goal)
async def set_challenge_name(message: types.Message, state: FSMContext):
    await state.update_data(goal=message.text)
    await message.answer("What is the mission?")
    await ChallengeCreation.mission.set()

@dp.message_handler(state=ChallengeCreation.mission)
async def set_challenge_name(message: types.Message, state: FSMContext):
    await state.update_data(mission=message.text)
    await message.answer("When does the challenge start? (format: YYYY-MM-DD)")
    await ChallengeCreation.start_at.set()


@dp.message_handler(state=ChallengeCreation.start_at)
async def set_start_at(message: types.Message, state: FSMContext):
    try:
        start_at = datetime.strptime(message.text, "%Y-%m-%d").date()
        await state.update_data(start_at=start_at)
        await message.answer("how long will the challenge last")
        await ChallengeCreation.full_time.set()
    except ValueError:
        await message.answer("Invalid date format. Please enter the date in YYYY-MM-DD format.")

@dp.message_handler(state=ChallengeCreation.full_time)
async def set_end_at(message: types.Message, state: FSMContext):
    try:
        full_time = int(message.text)
        await state.update_data(full_time=full_time)
        await message.answer("How many days are the tasks due?")
        await ChallengeCreation.limited_time.set()
    except ValueError:
        await message.answer("Pleace enter a valid number for the full time in days")


@dp.message_handler(state=ChallengeCreation.limited_time)
async def set_limited_time(message: types.Message, state: FSMContext):
    try:
        limited_time = int(message.text)
        await state.update_data(limited_time=limited_time)
        await message.answer("The daily tasks are different? (yes/no)")
        await ChallengeCreation.is_different.set()
    except ValueError:
        await message.answer("Please enter a valid number for the limited time in days.")



@dp.message_handler(state=ChallengeCreation.is_different)
async def set_is_different(message: types.Message, state: FSMContext):
    response = message.text.lower()
    if response in ["yes", "no"]:
        is_different = response == "yes"
        await state.update_data(is_different=is_different)
        await message.answer("Is this challenge public or private? (public/private)")
        await ChallengeCreation.status.set()
    else:
        await message.answer("Please answer with 'yes' or 'no'.")


@dp.message_handler(state=ChallengeCreation.status)
async def set_status(message: types.Message, state: FSMContext):
    response = message.text.lower()
    if response in ["public", "private"]:
        status = response == 'public'
        await state.update_data(status=status)
        if status == False:
            await message.answer("Please enter a secret key for this challenge.")
            await ChallengeCreation.secret_key.set()
        else:
            await confirm_challenge(message, state)  # Skip asking for secret_key/secret_pass if public
    else:
        await message.answer("Please choose either 'Public' or 'Private'.")


@dp.message_handler(state=ChallengeCreation.secret_key)
async def set_secret_key(message: types.Message, state: FSMContext):
    await state.update_data(secret_key=message.text)
    await message.answer("Please enter a secret password for this challenge.")
    await ChallengeCreation.secret_pass.set()


@dp.message_handler(state=ChallengeCreation.secret_pass)
async def set_secret_pass(message: types.Message, state: FSMContext):
    await state.update_data(secret_pass=message.text)
    await confirm_challenge(message, state)


async def confirm_challenge(message: types.Message, state: FSMContext):
    data = await state.get_data()
    end_at = data['start_at'] + timedelta(days=data['full_time'])
    challenge_info = (
        f"Challenge Name: {data['name']}\n"
        f"Start Date: {data['start_at']}\n"
        f"Full date: {data['full_time']}\n"
        f"End date: {end_at}\n" 
        f"Task limited_time (days): {data['limited_time']}\n"
        f"Different Tasks Daily: {'Yes' if data['is_different'] else 'No'}\n"
        f"status: {'Public' if data['status'] else 'Private'}\n"
    )
    if data['status'] == False:
        challenge_info += (
            f"Secret Key: {data['secret_key']}\n"
            f"Secret Password: {data['secret_pass']}\n"
        )
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Confirm"), KeyboardButton("Cancel"))
    await message.answer(f"Please confirm the challenge details:\n\n{challenge_info}", reply_markup=markup)
    await ChallengeCreation.confirmation.set()

@dp.message_handler(state=ChallengeCreation.confirmation)
async def confirm_creation(message: types.Message, state: FSMContext):
    if message.text.lower() == "confirm":
        data = await state.get_data()
        db.save_challenge(data)
        await message.answer("Challenge created successfully!")
    else:
        await message.answer("Challenge creation canceled.")
    await state.finish()


# Register handlers
def register_handlers_challenge(dp=dp):
    dp.register_message_handler(start_challenge_creation, commands="create_challenge", state="*")
    dp.register_message_handler(set_name, state=ChallengeCreation.name)
    dp.register_message_handler(set_start_at, state=ChallengeCreation.start_at)
    dp.register_message_handler(set_end_at, state=ChallengeCreation.end_at)
    dp.register_message_handler(set_limited_time, state=ChallengeCreation.limited_time)
    dp.register_message_handler(set_is_different, state=ChallengeCreation.is_different)
    dp.register_message_handler(set_status, state=ChallengeCreation.status)
    dp.register_message_handler(set_secret_key, state=ChallengeCreation.secret_key)
    dp.register_message_handler(set_secret_pass, state=ChallengeCreation.secret_pass)
    dp.register_message_handler(confirm_creation, state=ChallengeCreation.confirmation)
