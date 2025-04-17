from aiogram.fsm.state import StatesGroup, State
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const

from lexicon.lexicon import D_BUTTONS


class DAccount(StatesGroup):
    account = State()


dialog = Dialog(
    Window(
        Const('Аккаунт'),
        Cancel(Const(D_BUTTONS['back'])),
        state=DAccount.account
    )
)