from aiogram.enums import ParseMode
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.api.entities import EventContext
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel, Back, Next, Button
from aiogram_dialog.widgets.text import Const, Jinja, Format
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db.models import User, Event
from db.models.Association import Association
from lexicon.lexicon import D_BUTTONS, DU_CREATE_EVENT


class CreateEvent(StatesGroup):
    title = State() # название
    description = State() # описание
    event = State() # событие
    moderation = State() # модерация

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
        city=manager.start_data['city'],
        date_event=manager.start_data['date'],
    )
    user.events.append(assoc) # добавляем промежуточную запись
    session.add(user)
    await session.commit()
    await manager.next()


async def get_event_data(dialog_manager: DialogManager, **kwargs):
    return {
        'title': dialog_manager.find('title').get_value(),
        'description': dialog_manager.find('description').get_value(),
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
           on_success=Next()
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
           on_success=Next()
       ),
       Cancel(Const(D_BUTTONS['back'])),
       parse_mode=ParseMode.HTML,
       state=CreateEvent.description
   ),
   Window(
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