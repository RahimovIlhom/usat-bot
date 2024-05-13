from aiogram.dispatcher.filters.state import StatesGroup, State


class ApplicantRegisterStates(StatesGroup):
    phone = State()
    pinfl = State()
    direction = State()
    type_of_edu = State()
    language = State()
