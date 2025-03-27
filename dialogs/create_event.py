from typing import Any

from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const


class CreateEventDialog(StatesGroup):
    title = State() # что
    description = State() # описание
    photo = State() # фото
    address = State() # где
    datetime = State() # дата/время

def validate_title(title: str):
    # Проверка, что title не состоит только из цифр
    if title.replace(" ", "").isdigit():
        raise ValueError("Название не может состоять только из цифр")
    # Проверка длины
    if len(title) < 5 or len(title) > 15:
        raise ValueError("Заголовок мероприятия должен быть 5 - 15 символов")

async def error_title(
        message: Message,
        dialog_: Any,
        manager: DialogManager,
        error_: ValueError
):
    await message.answer(str(error_))

dialog_create_event = Dialog(
    Window(
        Const('Название мероприятия:'),
        TextInput(
            id='title',
            type_factory=validate_title,
            # on_success=Next(),
            on_error=error_title,
        ),
        state=CreateEventDialog.title,
    )
)