from aiogram.enums import ParseMode
from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Cancel, Back, Next
from aiogram_dialog.widgets.text import Const, Jinja

from lexicon.lexicon import D_BUTTONS, DU_CREATE_EVENT


class CreateEvent(StatesGroup):
    title = State() # название
    description = State() # описание
    result = State() # событие


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
       Back(Const(D_BUTTONS['back'])),
       parse_mode = ParseMode.HTML,
       getter=get_event_data,
       state=CreateEvent.result
   )
)