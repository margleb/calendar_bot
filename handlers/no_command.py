from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram_dialog import DialogManager

from lexicon.lexicon import HANDLERS

no_cmd = Router(name='unknown command')

@no_cmd.message()
async def cmd_echo(message: Message, dialog_manager: DialogManager):
    await message.answer(
        HANDLERS['no_cmd'].format(message=message),
        parse_mode=ParseMode.HTML
    )