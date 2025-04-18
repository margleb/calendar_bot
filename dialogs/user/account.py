from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel, Button, Start
from aiogram_dialog.widgets.text import Const

from dialogs.user.join_events import DJoinEvents
from dialogs.user.my_events import DMyEvents
from lexicon.lexicon import D_BUTTONS, DU_ACCOUNT


class DAccount(StatesGroup):
    account = State()

dialog = Dialog(
    Window(
        Const(DU_ACCOUNT['account']),
        Start(Const(DU_ACCOUNT['buttons']['join_events']), id='join_events', state=DJoinEvents.events),
        Start(Const(DU_ACCOUNT['buttons']['my_events']), id='my_events', state=DMyEvents.events),
        Cancel(Const(D_BUTTONS['back'])),
        parse_mode=ParseMode.HTML,
        state=DAccount.account
    )
)