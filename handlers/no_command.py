from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_dialog import DialogManager

from lexicon.lexicon import HANDLERS

no_cmd = Router(name='unknown command')

@no_cmd.message()
async def cmd_echo(message: Message, dialog_manager: DialogManager):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Создать мероприятие",
                callback_data="cmd_start" # отлавливается в handler /start
            )]
        ]
    )
    await message.answer(
        HANDLERS['no_cmd'].format(message=message),
        parse_mode=ParseMode.HTML,
        reply_markup=markup
    )