from aiogram.dispatcher.filters.state import StatesGroup, State


class TestExecutionStates(StatesGroup):
    science = State()


class AddTestStates(StatesGroup):
    faculty = State()
    science = State()
    count = State()
    language = State()
