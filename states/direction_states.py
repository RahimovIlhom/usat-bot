from aiogram.dispatcher.filters.state import StatesGroup, State


class AddDirectionStates(StatesGroup):
    nameUz = State()
    nameRu = State()
