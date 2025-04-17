from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from dialogs.common.start import DCommon
from dialogs.user.account import DAccount
from dialogs.user.calendar import DCalendar
from lexicon.lexicon import HANDLERS

router = Router(name='user commands')

@router.message(CommandStart())
async def cmd_start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(DCommon.start, mode=StartMode.RESET_STACK)

@router.message(Command('support'))
async def cmd_support(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(DCommon.support, mode=StartMode.RESET_STACK)


@router.message(Command('account'))
async def cmd_support(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(DAccount.account, mode=StartMode.RESET_STACK)


@router.message(Command('calendar'))
async def cmd_support(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(DCalendar.city, mode=StartMode.RESET_STACK)


# Этот срабатывает из no_command
@router.callback_query(F.data == 'cmd_start')
async def cmd_start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(DCommon.start, mode=StartMode.RESET_STACK)

