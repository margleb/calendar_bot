from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Calendar, Cancel
from aiogram_dialog.widgets.text import Const

from lexicon.lexicon import D_BUTTONS, DU_CALENDAR


class DCalendar(StatesGroup):
    calendar = State()

dialog = Dialog(
    Window(
        Const(DU_CALENDAR['calendar']),
        Calendar(id='calendar'),
        Cancel(Const(D_BUTTONS['back'])),
        parse_mode=ParseMode.HTML,
        state=DCalendar.calendar
    )
)