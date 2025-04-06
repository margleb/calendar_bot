from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from dialogs.create_event.states import CreateEventDialog
from dialogs.main_dialog.main_dialog import MainDialog

router = Router(name='user commands')

@router.message(CommandStart())
async def cmd_start(message: Message, dialog_manager: DialogManager):
    # await dialog_manager.start(MainDialog.main, mode=StartMode.RESET_STACK)
    await dialog_manager.start(CreateEventDialog.title, mode=StartMode.RESET_STACK)


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Готов помочь!')


# @router.message()
# async def echo_handler(message: Message):
#     print(message.model_dump_json())
#     await message.answer(f'Извини, команда {message.text} мне неизвестна')