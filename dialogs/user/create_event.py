from aiogram.enums import ParseMode
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel, Back, Next, Button
from aiogram_dialog.widgets.text import Const, Jinja
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from db.models import User, Event
from db.models.Association import Association
from db.models.Event import CityEnum
from lexicon.lexicon import D_BUTTONS, DU_CREATE_EVENT


class CreateEvent(StatesGroup):
    title = State() # название
    description = State() # описание
    result = State() # событие

async def create_event(callback: CallbackQuery, button: Button, manager: DialogManager):
    session = manager.middleware_data.get('session')  # получаем сессию
    data = manager.dialog_data
    print(session)
    user = await session.scalar(
        select(User)
        .options(selectinload(User.events)) # lazy load
        .where(User.telegram_id == callback.from_user.id)
    )
    assoc = Association(status='create')
    assoc.event = Event(
        title='title',
        description='description',
        city=CityEnum.moscow.value,
        date_event=func.now()
    )
    user.events.append(assoc) # добавляем промежуточную запись
    session.add(user)
    await session.commit()


async def get_event_data(dialog_manager: DialogManager, **kwargs):
    return {
        'title': dialog_manager.find('title').get_value(),
        'description': dialog_manager.find('description').get_value(),
        'city': dialog_manager.start_data['city'],
        'date': dialog_manager.start_data['date'],
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
       Jinja("""
       <b>{{title}}</b>
       <b>{{description}}</b>
       <b>{{city}}</b>
       <b>{{date}}</b>
       """),
       Button(
           Const(DU_CREATE_EVENT['buttons']['create_event']),
           on_click=create_event,
           id='moderate_event'
       ),
       Back(Const(D_BUTTONS['back'])),
       parse_mode = ParseMode.HTML,
       getter=get_event_data,
       state=CreateEvent.result
   )
)