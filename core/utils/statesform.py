from aiogram.fsm.state import StatesGroup, State


class StepsForm(StatesGroup):
    GET_NAME = State()
    GET_SURNAME = State()
    GET_AGE = State()


class UserVoting(StatesGroup):
    START_VOTING = State()
    CHOOSE_CANDIDATE = State()
    CONFIRM = State()


class Valentine(StatesGroup):
    GET_TO = State()
    GET_MSG = State()
    GET_FROM = State()

