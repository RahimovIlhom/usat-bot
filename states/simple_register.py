from aiogram.dispatcher.filters.state import StatesGroup, State


class SimpleRegisterStates(StatesGroup):
    language = State()
