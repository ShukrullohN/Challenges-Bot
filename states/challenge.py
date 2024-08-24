from aiogram.dispatcher.filters.state import State, StatesGroup
class ChallengeCreation(StatesGroup):
    name = State()
    info = State()
    goal = State()
    mission = State()
    start_at = State()
    full_time = State()
    limited_time = State()
    is_different = State()
    status = State()
    secret_key = State()
    secret_pass = State()
    confirmation = State()