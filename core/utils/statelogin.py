from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    AUTH_ID = State()
