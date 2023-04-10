from aiogram.dispatcher.filters.state import State, StatesGroup



class Giveaway(StatesGroup):
    START = State()
    IDCODE = State()
