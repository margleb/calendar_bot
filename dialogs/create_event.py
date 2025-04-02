from aiogram.dispatcher.middlewares.user_context import EventContext
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.api.entities import MediaId, MediaAttachment
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Next, Back, Select, Calendar
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Jinja, Format

from dialogs.getters import get_event_data
from dialogs.handlers import error_text, validate_text, selected_city, on_date_selected, handle_photo
from dialogs.states import CreateEventDialog

dialog_create_event = Dialog(
    Window(
        Const('Название мероприятия:'),
        TextInput(
            id='title',
            type_factory=lambda x: validate_text(x, 5, 20),
            on_error=error_text,
            on_success=Next()
        ),
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
        Const('Выберите дату проведения мероприятия:'),
        Calendar(
            id='calendar',
            on_click=on_date_selected
        ),
        Back(Const('Назад')),
        state=CreateEventDialog.date,
    ),
    Window(
        DynamicMedia("photo"),
        Jinja(
            "\n\n"
            "{{description}}\n\n"
            "<b>______</b>\n"
            "<b>Что</b> {{title}}\n"
            "<b>Где:</b> {{city}}\n"
            "<b>Дата:</b> {{date}}\n"
            "<b>Пишите:</b> @{{username}}\n"
        ),
        parse_mode="HTML",
        getter=get_event_data,
        state=CreateEventDialog.result
    ),
)