from aiogram.fsm.state import StatesGroup, State


class ModerateEvents(StatesGroup):
    events = State()