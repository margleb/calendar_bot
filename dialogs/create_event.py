import operator
from datetime import datetime, date
from typing import Any

from aiogram.dispatcher.middlewares.user_context import EventContext
from aiogram.enums import ContentType, ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.api.entities import MediaId, MediaAttachment
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Next, Back, SwitchTo, Select, Calendar
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Jinja, Format


class CreateEventDialog(StatesGroup):
    title = State() # что
    description = State() # описание
    photo = State() # фото
    city = State() # где
    date = State() # дата
    result = State() # событие

async def get_event_data(dialog_manager: DialogManager, event_context: EventContext, **kwargs) -> dict:
    city = dialog_manager.dialog_data['city']
    date_event = dialog_manager.dialog_data['selected_date']
    image_id = dialog_manager.dialog_data['photo']  # Your file_id
    image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(image_id))
    username = event_context.chat.username  # получаем username
    return {
        'title': dialog_manager.find('title').get_value(),
        'description': dialog_manager.find('description').get_value(),
        'photo': image,
        'city': city,
        'date': date_event,
        'username': username
    }

async def handle_photo(message: Message, message_input: MessageInput, manager: DialogManager):
    if message.photo:
        manager.dialog_data['photo'] = message.photo[-1].file_id
        await manager.next()
    else:
        await message.reply('🔴 Пожалуйста, загрузите свою фотографию')

async def on_date_selected(callback: CallbackQuery, widget, manager: DialogManager, selected_date: date):
    if selected_date < datetime.now().date():
        # Если дата в прошлом - показываем предупреждение
        await callback.answer("Нельзя запланировать событие на прошедшую дату.", show_alert=True)
    else:
        # Если дата валидна - сохраняем и уведомляем
        manager.dialog_data["selected_date"] = selected_date
    await manager.next()  # Переходим к следующему шагу

async def selected_city(callback: CallbackQuery, widget: Any, manager: DialogManager, city: str):
    manager.dialog_data['city'] = city
    await manager.next()

def validate_text(title: str, min_letters: int, max_letters: int) -> str:
    # Проверка, что текст не состоит только из цифр
    if title.replace(" ", "").isdigit():
        raise ValueError("🔴 Текст не может состоять только из цифр")
    # Проверка длины
    if len(title) < min_letters or len(title) > max_letters:
        raise ValueError(f"🔴 Текст должен быть <b>{min_letters} - {max_letters}</b> символов")
    return title

async def error_text(
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