from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const

from lexicon.lexicon import D_BUTTONS


class CreateEvent(StatesGroup):
    title = State()

dialog = Dialog(
   Window(
       Const('Создать мероприятие'),
        Cancel(Const(D_BUTTONS['back'])),
       state=CreateEvent.title
   )
)