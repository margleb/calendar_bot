import asyncio

from aiogram import Dispatcher, Bot
from aiogram_dialog import setup_dialogs
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config.config import get_config, BotConfig, DbConfig
from dialogs.create_event.create_event import dialog_create_event
from dialogs.main_dialog.main_dialog import dialog_main_dialog
from dialogs.moderate_events.moderate_events import dialog_moderate_dialog
from handlers import get_routes
from handlers.main_menu import set_main_menu
from middlewares.session import DbSessionMiddleware
from models import Base


async def main():

    # экземпляр бота
    bot_config = get_config(BotConfig, 'bot')
    bot = Bot(token=bot_config.token.get_secret_value())

    # маршруты
    dp = Dispatcher(admin_id=bot_config.admin_id)
    dp.include_routers(*get_routes(), dialog_main_dialog, dialog_create_event, dialog_moderate_dialog)

    # запускаем dialog-manager
    setup_dialogs(dp)

    # создаем engine
    db_config = get_config(DbConfig, 'db')
    engine = create_async_engine(
        url=str(db_config.dsn),  # здесь требуется приведение к строке
        echo=db_config.is_echo
    )

    # созданием таблицы
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    #     await conn.run_sync(Base.metadata.create_all)

    # Создаем сессию
    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    dp.update.outer_middleware(DbSessionMiddleware(session_maker))

    # Регистрируем асинхронную функцию в диспетчере,
    # которая будет выполняться на старте бота,
    dp.startup.register(set_main_menu)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )
    asyncio.run(main())