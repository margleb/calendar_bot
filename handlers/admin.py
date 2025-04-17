from aiogram import Router, F
from aiogram.filters import Command, MagicData
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

router = Router(name='admin commands')

# Фильтр: роутер доступен только chat id, равному admin_id,
# который передан в диспетчер
router.message.filter(MagicData(F.event.chat.id == F.admin_id)) # noqa

# @router.message(Command('moderate'))
# async def admin_handler(message: Message, dialog_manager: DialogManager):
#     await dialog_manager.start(ModerateEvents.events, mode=StartMode.RESET_STACK)
