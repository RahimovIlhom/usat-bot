from aiogram.dispatcher.filters.state import StatesGroup, State


class ApplicantRegisterStates(StatesGroup):
    phone = State()
    additional_phone = State()
    passport = State()
    birth_date = State()
    region = State()
    city = State()
    certificate = State()
    direction_type_lan = State()
