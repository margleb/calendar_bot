from aiogram.fsm.state import StatesGroup, State


class MyEvents(StatesGroup):
    events = State()