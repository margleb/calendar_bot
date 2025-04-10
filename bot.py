import asyncio

from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs

from config.config import get_config, BotConfig
from dialogs import get_dialogs
from handlers import get_routes



async def main():

    # экземпляр бота
    bot_config = get_config(BotConfig, 'bot')
    bot = Bot(token=bot_config.token.get_secret_value())

    # маршруты
    dp = Dispatcher(admin_id=bot_config.admin_id)
    dp.include_routers(*get_routes(), *get_dialogs())

    # запускаем dialog-manager
    setup_dialogs(dp)

    # создаем engine
    # db_config = get_config(DbConfig, 'db')
    # engine = create_async_engine(
    #     url=str(db_config.dsn),  # здесь требуется приведение к строке
    #     echo=db_config.is_echo
    # )

    # созданием таблицы
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    #     await conn.run_sync(Base.metadata.create_all)

    # Создаем сессию
    # session_maker = async_sessionmaker(engine, expire_on_commit=False)
    # dp.update.outer_middleware(DbSessionMiddleware(session_maker))

    # Регистрируем асинхронную функцию в диспетчере,
    # которая будет выполняться на старте бота,
    # dp.startup.register(set_main_menu)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )
    asyncio.run(main())