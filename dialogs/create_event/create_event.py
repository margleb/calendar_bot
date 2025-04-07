from datetime import datetime
from typing import Any

from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Next, Back, Select, Calendar, Button, CalendarConfig, Column, Cancel
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Jinja, Format
from pydantic import ValidationError

from dialogs.create_event.getters import get_event_data
from dialogs.create_event.handlers import error_text, validate_text, selected_city, handle_photo, \
    on_public_event
from dialogs.create_event.states import CreateEventDialog


def validate_participants(number: str) -> int:
    print(number)
    if not number.isdigit():
        raise ValueError("Укажите цифру от 1 до 30")
    number = int(number)
    if number < 1 or number > 30:
        raise ValueError("Количество участников должно быть от 1 до 30")
    return number

async def error_participants(
        message: Message,
        dialog_: Any,
        manager: DialogManager,
        error_: ValueError
):
    await message.reply(str(error_), parse_mode=ParseMode.HTML)


dialog_create_event = Dialog(
    Window(
        Const('Название мероприятия:'),
        TextInput(
            id='title',
            type_factory=lambda x: validate_text(x, 5, 20),
            on_error=error_text,
            on_success=Next()
        ),
        Cancel(Const('Назад')),
        state=CreateEventDialog.title
    ),
    Window(
        Const('Описание мероприятия:'),
        TextInput(
            id='description',
            type_factory=lambda x: validate_text(x, 15, 150),
            on_error=error_text,
            on_success=Next()
        ),
        Back(Const('Назад')),
        state=CreateEventDialog.description
    ),
    Window(
        Const('Укажите количество участников:'),
        TextInput(
            id='participants',
            type_factory=validate_participants,
            on_error=error_participants,
            on_success=Next()
        ),
        Back(Const('Назад')),
        state=CreateEventDialog.participants,
    ),
    Window(
        Const('Фотография мероприятия:'),
        MessageInput(
            handle_photo,  # Обработчик загрузки фото
        ),
        Back(Const('Назад')),
        state=CreateEventDialog.photo,
    ),
    Window(
        DynamicMedia("photo"),
        Jinja(
            "{{description}}\n\n"
            "<b>______</b>\n\n"
            "<b>Что</b> {{title}}\n"
            "<b>Где:</b> {{city}}\n"
            "<b>Когда:</b> {{date}}\n"
            "<b>Участников:</b> {{participants}}\n"
            "<b>Пишите:</b> @{{username}}\n"
        ),
        Column(
            Button(Const('Опубликовать событие'), id='public_event', on_click=on_public_event),
            Back(Const('Назад'))
        ),
        parse_mode="HTML",
        getter=get_event_data,
        state=CreateEventDialog.result
    ),
)