import asyncio
from datetime import datetime
from enum import Enum

from aiogram import Dispatcher, Bot
from aiogram_dialog import setup_dialogs
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from config.config import get_config, BotConfig, DbConfig
from dialogs.create_event import dialog_create_event
from handlers import get_routes
from middlewares.session import DbSessionMiddleware
from models import Base, Event
from models.event import CityEnum


async def main():

    # экземпляр бота
    bot_config = get_config(BotConfig, 'bot')
    bot = Bot(token=bot_config.token.get_secret_value())

    # маршруты
    dp = Dispatcher(admin_id=bot_config.admin_id)
    dp.include_routers(*get_routes(), dialog_create_event)

    # запускаем dialog-manager
    setup_dialogs(dp)

    # создаем engine
    db_config = get_config(DbConfig, 'db')
    engine = create_async_engine(
        url=str(db_config.dsn),  # здесь требуется приведение к строке
        echo=db_config.is_echo
    )

    # Проверка соединения с СУБД
    # async with engine.begin() as conn:
    #     await conn.execute(text("SELECT 1"))

    # созданием таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Создаем сессию
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    async with session_maker() as session:
        session.add(Event(
            tg_user_id=123456,
            title='Название мероприятия',
            description='Описание мероприятия',
            city=CityEnum.moscow.value,
            date=datetime.strptime('2025-04-03', '%Y-%m-%d'),
        ))
        await session.commit()

    # dp.update.outer_middleware(DbSessionMiddleware(session_maker))

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )
    asyncio.run(main())