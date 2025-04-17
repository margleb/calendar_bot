from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Start, Column, Next, Url, Back
from aiogram_dialog.widgets.text import Const, Format

from dialogs.user.account import DAccount
from dialogs.user.calendar import DCalendar
from lexicon.lexicon import DC_START, D_BUTTONS


class DCommon(StatesGroup):
    start = State()
    support = State()

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
            Start(
                Const(DC_START['buttons']['account']),
                id='account',
                state=DAccount.account
            ),
            Start(
                Const(DC_START['buttons']['calendar']),
                id='calendar',
                state=DCalendar.city
            ),
            Next(Const(DC_START['buttons']['support']), id='support')
        ),
        parse_mode=ParseMode.HTML,
        getter=get_start_data,
        state=DCommon.start
    ),
    Window(
        Const(DC_START['support']),
        Url(
            Const(DC_START['buttons']['support_msg']),
            Const(DC_START['buttons']['support_url']),
        ),
        Back(Const(D_BUTTONS['back'])),
        state=DCommon.support
    )
)