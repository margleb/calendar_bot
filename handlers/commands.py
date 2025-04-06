from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from dialogs.main_dialog.main_dialog import MainDialog
from dialogs.my_events.my_events import MyEvents

router = Router(name='user commands')

@router.message(CommandStart())
async def cmd_start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainDialog.city, mode=StartMode.RESET_STACK)


@router.message(Command('events'))
async def cmd_events(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MyEvents.events, mode=StartMode.RESET_STACK)


# @router.message()
# async def echo_handler(message: Message):
#     print(message.model_dump_json())
#     await message.answer(f'Извини, команда {message.text} мне неизвестна')