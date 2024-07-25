from aiogram.dispatcher.filters.state import StatesGroup, State


class AddQuestionStates(StatesGroup):
    image = State()
    question = State()
    response1 = State()
    response2 = State()
    response3 = State()
    response4 = State()
