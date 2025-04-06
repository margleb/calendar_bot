from aiogram.fsm.state import StatesGroup, State


class MainDialog(StatesGroup):
    main = State()
    choice = State()
    choose_event = State()