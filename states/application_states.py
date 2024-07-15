from aiogram.dispatcher.filters.state import StatesGroup, State


class ApplicantRegisterStates(StatesGroup):
    phone = State()
    additional_phone = State()
    passport = State()
    birth_date = State()
    first_name = State()
    last_name = State()
    middle_name = State()
    pinfl = State()
    # passport_image_front = State()
    # passport_image_back = State()
    region = State()
    city = State()
    certificate = State()
    direction_type_lan = State()
