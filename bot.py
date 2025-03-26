import asyncio

from aiogram import Dispatcher, Bot
from config.config import get_config, BotConfig
from handlers import get_routers


async def main():

    # экземпляр бота
    bot_config = get_config(BotConfig, 'bot')
    bot = Bot(token=bot_config.token.get_secret_value())

    # маршруты
    dp = Dispatcher()
    dp.include_routers(*get_routers())

    await dp.start_polling(bot)

asyncio.run(main())