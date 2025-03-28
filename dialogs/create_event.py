import operator
from datetime import datetime, timedelta, date
from typing import Any
from zoneinfo import available_timezones

from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Next, Back, Select, Calendar, CalendarConfig
from aiogram_dialog.widgets.text import Const, Format


class CreateEventDialog(StatesGroup):
    title = State() # что
    description = State() # описание
    photo = State() # фото
    city = State() # где
    datetime = State() # дата/время

def validate_text(title: str, min_letters: int, max_letters: int):
    # Проверка, что title не состоит только из цифр
    if title.replace(" ", "").isdigit():
        raise ValueError("🔴 Текст не может состоять только из цифр")
    # Проверка длины
    if len(title) < min_letters or len(title) > max_letters:
        raise ValueError(f"🔴 Текст должен быть <b>{min_letters} - {max_letters}</b> символов")

async def error_text(
        message: Message,
        dialog_: Any,
        manager: DialogManager,
        error_: ValueError
):
    await message.reply(str(error_), parse_mode=ParseMode.HTML)

async def handle_photo(message: Message, message_input: MessageInput, manager: DialogManager):
    # Проверяем, что сообщение содержит фото
    if message.photo:
        photo = message.photo[-1]  # Берем самое большое изображение
        file_id = photo.file_id
        # Сохраняем file_id в DialogManager (например, в dialog_data)
        manager.dialog_data["photo_id"] = file_id
        await manager.next()  # Переходим к следующему шагу
    else:
        await message.reply("🔴 Пожалуйста, отправьте фотографию!")

async def available_cities(**kwargs):
    cities = [
        ("Москва", '1'),
        ("Санкт-Петербург", '2'),
    ]
    return {
        "cities": cities,
        "count": len(cities),
    }

async def selected_city(callback: CallbackQuery, widget: Any, manager: DialogManager, city: str):
    manager.dialog_data["selected_city"] = city
    await manager.next()  # Переходим к следующему шагу

# Создаем конфигурацию для календаря
# calendar_config = CalendarConfig(
#    min_date=datetime.now().date(),
#    max_date=datetime.now().date() + timedelta(days=365)
# )

async def on_date_selected(callback: CallbackQuery, widget, manager: DialogManager, selected_date: date):
    if selected_date < datetime.now().date():
        # Если дата в прошлом - показываем предупреждение
        await callback.answer("Нельзя запланировать событие на прошедшую дату!", show_alert=True)
    else:
        # Если дата валидна - сохраняем и уведомляем
        manager.dialog_data["selected_date"] = selected_date
    await manager.next()  # Переходим к следующему шагу

dialog_create_event = Dialog(
    Window(
        Const('Название мероприятия:'),
        TextInput(
            id='title',
            type_factory=lambda x: validate_text(x, 5, 20),
            on_success=Next(),
            on_error=error_text,
        ),
        state=CreateEventDialog.title,
    ),
    Window(
        Const('Описание мероприятия:'),
        TextInput(
            id='description',
            type_factory=lambda x: validate_text(x, 20, 100),
            on_success=Next(),
            on_error=error_text,
        ),
        Back(Const('Назад')),
        state=CreateEventDialog.description,
    ),
    Window(
        Const('Фотография мероприятия:'),
        MessageInput(
            handle_photo,  # Обработчик загрузки фото
            # content_types=[ContentType.PHOTO],  # Принимаем только фото
            # filter=photo_filter
        ),
        Back(Const('Назад')),
        state=CreateEventDialog.photo,
    ),
    Window(
        Const('Укажите город:'),
        Select(
            Format("{item[0]}"),
            id="s_cities",
            item_id_getter=operator.itemgetter(0),
            items="cities",
            on_click=selected_city,
        ),
        Back(Const('Назад')),
        getter=available_cities,
        state=CreateEventDialog.city,
    ),
    Window(
        Const('Выберите дату проведения мероприятия:'),
        Calendar(
            id='event_calendar',
            on_click=on_date_selected
        ),
        Back(Const('Назад')),
        state=CreateEventDialog.datetime,
    ),
)