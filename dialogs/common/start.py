from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Start, Column
from aiogram_dialog.widgets.text import Const, Format

from dialogs.user.calendar import DCalendar
from lexicon.lexicon import DC_START


class DCommon(StatesGroup):
    start = State()

async def get_start_data(dialog_manager: DialogManager, **kwargs):
    # Получаем объект пользователя из события Telegram
    event_from_user = dialog_manager.event.from_user
    return {
        'username': event_from_user.first_name or event_from_user.username or ""
    }

dialog = Dialog(
    Window(
        Format(DC_START['start']),
        Column(
            Button(Const(DC_START['buttons']['account']), id='account'),
            Start(
                Const(DC_START['buttons']['calendar']),
                id='calendar',
                state=DCalendar.city
            ),
        ),
        parse_mode=ParseMode.HTML,
        getter=get_start_data,
        state=DCommon.start
    )
)