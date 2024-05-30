from aiogram.dispatcher.filters.state import StatesGroup, State


class ScienceAddStates(StatesGroup):
    nameUz = State()
    nameRu = State()
