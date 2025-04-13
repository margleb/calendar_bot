from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from dialogs.common.start import DCommon

router = Router(name='user commands')

@router.message(CommandStart())
async def cmd_start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(DCommon.start, mode=StartMode.RESET_STACK)

# Этот срабатывает из no_command
@router.callback_query(F.data == 'cmd_start')
async def cmd_start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(DCommon.start, mode=StartMode.RESET_STACK)

