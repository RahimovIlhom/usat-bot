from aiogram.dispatcher.filters.state import StatesGroup, State


class AddDirectionStates(StatesGroup):
    nameUz = State()
    nameRu = State()
    examPassPercentage = State()


class TypesOfEduStates(StatesGroup):
    nameUz = State()
    nameRu = State()
