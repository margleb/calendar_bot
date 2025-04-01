from aiogram.enums import ContentType
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.api.entities import MediaId, MediaAttachment
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Next, Back, SwitchTo
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Jinja


class CreateEventDialog(StatesGroup):
    title = State() # что
    description = State() # описание
    photo = State() # фото
    result = State() # событие

async def get_event_data(dialog_manager: DialogManager, **kwargs) -> dict:
    image_id = dialog_manager.dialog_data['photo']  # Your file_id
    image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(image_id))
    return {
        'title': dialog_manager.find('title').get_value(),
        'description': dialog_manager.find('description').get_value(),
        'photo': image
    }

async def handle_photo(message: Message, message_input: MessageInput, manager: DialogManager):
    if message.photo:
        manager.dialog_data['photo'] = message.photo[-1].file_id
        await manager.next()
    else:
        await message.reply('Пожалуйста, загрузите фотографию мероприятия')

dialog_create_event = Dialog(
    Window(
        Const('Название мероприятия:'),
        TextInput(
            id='title',
            # on_success=Next()
            on_success=SwitchTo(Const('К фотографии'), id='photo', state=CreateEventDialog.photo),
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
        DynamicMedia("photo"),
        Jinja(
            "<b>You entered</b>:\n\n"
            "<b>Что:</b>: {{title}}\n"
            "<b>Описание:</b>: {{description}}\n"
        ),
        getter=get_event_data,
        state=CreateEventDialog.result
    ),
)