import asyncio

from aiogram import Dispatcher, Bot
from aiogram_dialog import setup_dialogs

from config.config import get_config, BotConfig
from dialogs.create_event import dialog_create_event
from handlers.commands import commands_router


async def main():

    # экземпляр бота
    bot_config = get_config(BotConfig, 'bot')
    bot = Bot(token=bot_config.token.get_secret_value())

    # маршруты
    dp = Dispatcher()
    dp.include_routers(commands_router, dialog_create_event)

    # запускаем dialog-manager
    setup_dialogs(dp)

    await dp.start_polling(bot)

asyncio.run(main())