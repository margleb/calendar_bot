from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from dialogs.common.start import DCommon
from lexicon.lexicon import HANDLERS

router = Router(name='user commands')

@router.message(CommandStart())
async def cmd_start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(DCommon.start, mode=StartMode.RESET_STACK)


@router.message(Command('support'))
async def cmd_support(message: Message, dialog_manager: DialogManager):
    await message.answer(HANDLERS['support'])


# Этот срабатывает из no_command
@router.callback_query(F.data == 'cmd_start')
async def cmd_start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(DCommon.start, mode=StartMode.RESET_STACK)

