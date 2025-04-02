import operator
from typing import Any

from aiogram.enums import ContentType
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.api.entities import MediaId, MediaAttachment
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Next, Back, SwitchTo, Select
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Jinja, Format


class CreateEventDialog(StatesGroup):
    title = State() # что
    description = State() # описание
    photo = State() # фото
    city = State() # где
    result = State() # событие

async def get_event_data(dialog_manager: DialogManager, **kwargs) -> dict:
    # image_id = dialog_manager.dialog_data['photo']  # Your file_id
    city = dialog_manager.dialog_data['city']
    # image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(image_id))
    return {
        'title': dialog_manager.find('title').get_value(),
        'description': dialog_manager.find('description').get_value(),
        # 'photo': image,
        'city': city
    }

async def handle_photo(message: Message, message_input: MessageInput, manager: DialogManager):
    if message.photo:
        manager.dialog_data['photo'] = message.photo[-1].file_id
        await manager.next()
    else:
        await message.reply('Пожалуйста, загрузите фотографию мероприятия')

async def selected_city(callback: CallbackQuery, widget: Any, manager: DialogManager, city: str):
    manager.dialog_data['city'] = city
    await manager.next()

dialog_create_event = Dialog(
    Window(
        Const('Название мероприятия:'),
        TextInput(
            id='title',
            # on_success=Next()
            on_success=SwitchTo(Const('К Городу'), id='to_city', state=CreateEventDialog.city),
        ),
        state=CreateEventDialog.title
    ),
    Window(
        Const('Описание мероприятия:'),
        TextInput(
            id='description',
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
        state=CreateEventDialog.city,
    ),
    Window(
        # DynamicMedia("photo"),
        Jinja(
            "<b>You entered</b>:\n\n"
            "<b>Что:</b>: {{title}}\n"
            "<b>Описание:</b>: {{description}}\n"
            "<b>Город:</b>: {{city}}\n"
        ),
        getter=get_event_data,
        state=CreateEventDialog.result
    ),
)