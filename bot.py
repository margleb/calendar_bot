import asyncio

from aiogram import Dispatcher, Bot
from aiogram_dialog import setup_dialogs
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from config.config import get_config, BotConfig, DbConfig
from dialogs.create_event import dialog_create_event
from handlers.commands import commands_router


async def main():

    # экземпляр бота
    bot_config = get_config(BotConfig, 'bot')
    bot = Bot(token=bot_config.token.get_secret_value())

    # создаем engine
    db_config = get_config(DbConfig, 'db')
    engine = create_async_engine(
        url=str(db_config.dsn),  # здесь требуется приведение к строке
        echo=db_config.is_echo
    )

    # Проверка соединения с СУБД
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))

    # маршруты
    dp = Dispatcher()
    dp.include_routers(commands_router, dialog_create_event)

    # запускаем dialog-manager
    setup_dialogs(dp)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )
    asyncio.run(main())