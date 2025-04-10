from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Select, Cancel
from aiogram_dialog.widgets.text import Const, Format

from lexicon.lexicon import DU_CALENDAR, D_BUTTONS


class DCalendar(StatesGroup):
    city = State()
    calendar = State()

dialog = Dialog(
    Window(
        Const(DU_CALENDAR['city']),
        Select(
            Format("{item}"),
            id='city',
            item_id_getter=str,
            items=['Москва', 'Санкт-Петербург'],
        ),
        Cancel(Const(D_BUTTONS['back'])),
        parse_mode=ParseMode.HTML,
        state=DCalendar.city
    ),
    # Window(
    #     Const(DU_CALENDAR['calendar']),
    #     EventCalendar(id='calendar'),
    #     Cancel(Const(D_BUTTONS['back'])),
    #     parse_mode=ParseMode.HTML,
    #     state=DCalendar.calendar
    # )
)