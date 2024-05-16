from aiogram.dispatcher.filters.state import StatesGroup, State


class ApplicantRegisterStates(StatesGroup):
    phone = State()
    pinfl = State()
    direction_type_lan = State()
