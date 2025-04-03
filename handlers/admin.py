from aiogram import Router, F
from aiogram.filters import Command, MagicData
from aiogram.types import Message

router = Router(name='admin commands')

# Фильтр: роутер доступен только chat id, равному admin_id,
# который передан в диспетчер
router.message.filter(MagicData(F.event.chat.id == F.admin_id)) # noqa

@router.message(Command('admin'))
async def admin_handler(message: Message):
    await message.answer('Hello, admin!')