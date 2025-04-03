from aiogram.fsm.state import StatesGroup, State


class CreateEventDialog(StatesGroup):
    title = State() # что
    description = State() # описание
    photo = State() # фото
    city = State() # где
    date = State() # дата
    result = State() # событие