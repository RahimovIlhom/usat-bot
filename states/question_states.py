from aiogram.dispatcher.filters.state import StatesGroup, State


class AddQuestionStates(StatesGroup):
    image = State()
    question = State()
