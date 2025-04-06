from aiogram.fsm.state import StatesGroup, State


class MainDialog(StatesGroup):
    city = State()
    calendar = State()
    choice = State()
    choose_event = State()