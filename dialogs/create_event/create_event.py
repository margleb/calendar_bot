from datetime import datetime

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Next, Back, Select, Calendar, Button, CalendarConfig, Column, Cancel
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Jinja, Format

from dialogs.create_event.getters import get_event_data
from dialogs.create_event.handlers import error_text, validate_text, selected_city, handle_photo, \
    on_public_event
from dialogs.create_event.states import CreateEventDialog


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
        Const('Фотография мероприятия:'),
        MessageInput(
            handle_photo,  # Обработчик загрузки фото
        ),
        Back(Const('Назад')),
        state=CreateEventDialog.photo,
    ),
    Window(
        Const('Укажите город:'),
        Select(
            Format("{item}"),
            id='city',
            item_id_getter=lambda x: x,
            items=['Москва', 'Санкт-Петербург'],
            on_click=selected_city
        ),
        Back(Const('Назад')),
        state=CreateEventDialog.city
    ),
    Window(
        DynamicMedia("photo"),
        Jinja(
            "{{description}}\n\n"
            "<b>______</b>\n\n"
            "<b>Что</b> {{title}}\n"
            "<b>Где:</b> {{city}}\n"
            "<b>Когда:</b> {{date}}\n"
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