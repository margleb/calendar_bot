from aiogram.enums import ParseMode, ContentType
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Back, Next, Button
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Jinja, Format
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db.models import User, Event
from db.models.Association import Association
from lexicon.lexicon import D_BUTTONS, DU_CREATE_EVENT


class CreateEvent(StatesGroup):
    title = State() # название
    description = State() # описание
    image = State() # фотография
    participants = State() # количество участников
    event = State() # событие
    moderation = State() # модерация

async def on_image_received(message: Message, message_input: MessageInput, manager: DialogManager):
    if not message.photo:
        await message.answer(DU_CREATE_EVENT['errors']['img_error'])
        return
    photo = message.photo[-1]
    file_id = photo.file_id
    manager.dialog_data['image_file_id'] = file_id
    await manager.next()

async def validate_title(message: Message, **kwargs):
    if len(message.text) < 5 or len(message.text) > 30:
        await message.answer(DU_CREATE_EVENT['errors']['title_error'], parse_mode=ParseMode.HTML)
        return

async def validate_description(message: Message, **kwargs):
    if len(message.text) < 15 or len(message.text) > 100:
        await message.answer(DU_CREATE_EVENT['errors']['description_error'], parse_mode=ParseMode.HTML)
        return

async def validate_participants(message: Message, **kwargs):
    if not message.text.isdigit():
        await message.answer(DU_CREATE_EVENT['errors']['participants_error'])
        pass

async def create_event(callback: CallbackQuery, button: Button, manager: DialogManager):
    session = manager.middleware_data.get('session')  # получаем сессию
    user = await session.scalar(
        select(User)
        .options(selectinload(User.events)) # lazy load
        .where(User.telegram_id == callback.from_user.id)
    )
    assoc = Association(status='create')
    assoc.event = Event(
        title=manager.find('title').get_value(),
        description=manager.find('description').get_value(),
        image_id=manager.dialog_data.get('image_file_id'), # добавляет фото, если оно есть
        participants=manager.find('participants').get_value(),
        city=manager.start_data['city'],
        date_event=manager.start_data['date'],
        username=manager.event.from_user.username
    )
    user.events.append(assoc) # добавляем промежуточную запись
    session.add(user)
    await session.commit()
    await manager.next()


async def get_event_data(dialog_manager: DialogManager, **kwargs):
    image_id = dialog_manager.dialog_data.get('image_file_id')
    photo = None
    if image_id:
        photo = MediaAttachment(ContentType.PHOTO, file_id=MediaId(image_id))
    return {
        'title': dialog_manager.find('title').get_value(),
        'description': dialog_manager.find('description').get_value(),
        'photo': photo,
        'participants': dialog_manager.find('participants').get_value(),
        'city': dialog_manager.start_data['city'],
        'date': dialog_manager.start_data['date'],
        'username': dialog_manager.event.from_user.username,
    }


dialog = Dialog(
   Window(
       Const(DU_CREATE_EVENT['title']),
       TextInput(
           id='title',
           type_factory=str,
           on_success=Next(),
           filter=validate_title,
       ),
       Cancel(Const(D_BUTTONS['back'])),
       parse_mode=ParseMode.HTML,
       state=CreateEvent.title
   ),
   Window(
       Const(DU_CREATE_EVENT['description']),
       TextInput(
           id='description',
           type_factory=str,
           on_success=Next(),
           filter=validate_description,
       ),
       Cancel(Const(D_BUTTONS['back'])),
       parse_mode=ParseMode.HTML,
       state=CreateEvent.description
   ),
   Window(
       Const(DU_CREATE_EVENT['image']),
       MessageInput(on_image_received, content_types=[ContentType.ANY]),
       Next(Const(DU_CREATE_EVENT['buttons']['no_image'])),
       state=CreateEvent.image
   ),
   Window(
      Const(DU_CREATE_EVENT['participants']),
      TextInput(
          id='participants',
          type_factory=int,
          filter=validate_participants,
          on_success=Next()
      ),
       Back(Const(D_BUTTONS['back'])),
       state=CreateEvent.participants,
   ),
   Window(
       DynamicMedia("photo", when=lambda data, widget, manager: data.get("photo") is not None),
       Jinja(DU_CREATE_EVENT['result']),
       Button(
           Const(DU_CREATE_EVENT['buttons']['create_event']),
           on_click=create_event,
           id='moderate_event'
       ),
       Back(Const(D_BUTTONS['back'])),
       parse_mode=ParseMode.HTML,
       state=CreateEvent.event
   ),
   Window(
       Format(DU_CREATE_EVENT['moderation']),
       Cancel(Const(DU_CREATE_EVENT['buttons']['apply_moderation'])),
       parse_mode=ParseMode.HTML,
       state=CreateEvent.moderation
   ),
   getter=get_event_data
)