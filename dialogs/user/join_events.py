from aiogram.fsm.state import StatesGroup, State
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const

from lexicon.lexicon import D_BUTTONS


class DJoinEvents(StatesGroup):
    events = State()

dialog = Dialog(
    Window(
        Const('Мероприятия'),
        Cancel(Const(D_BUTTONS['back'])),
        state=DJoinEvents.events
    )
)