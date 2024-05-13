from aiogram.dispatcher.filters.state import StatesGroup, State


class AddContractSumma(StatesGroup):
    summa = State()
