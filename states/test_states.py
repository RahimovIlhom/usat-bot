from aiogram.dispatcher.filters.state import StatesGroup, State


class TestExecutionStates(StatesGroup):
    execution = State()
