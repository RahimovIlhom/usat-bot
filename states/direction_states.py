from aiogram.dispatcher.filters.state import StatesGroup, State


class AddDirectionStates(StatesGroup):
    newId = State()
    nameUz = State()
    nameRu = State()


class TypesOfEduStates(StatesGroup):
    newId = State()
    nameUz = State()
    nameRu = State()
