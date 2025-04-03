import asyncio
import random
from datetime import datetime, timedelta

from aiogram import Dispatcher, Bot
from aiogram_dialog import setup_dialogs
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config.config import get_config, BotConfig, DbConfig
from dialogs.create_event.create_event import dialog_create_event
from dialogs.moderate_events.moderate_events import dialog_moderate_dialog
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
    dp.include_routers(*get_routes(), dialog_create_event, dialog_moderate_dialog)

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
    dp.update.outer_middleware(DbSessionMiddleware(session_maker))

    # async with session_maker() as session:
    #
    #     # Список возможных заголовков
    #     titles = [
    #         "Концерт рок-группы",
    #         "Выставка современного искусства",
    #         "Мастер-класс по программированию",
    #         "Фестиваль еды",
    #         "Спортивный турнир",
    #         "Литературный вечер",
    #         "Кинофестиваль",
    #         "Воркшоп по дизайну"
    #     ]
    #
    #     # Список возможных описаний
    #     descriptions = [
    #         "Уникальное мероприятие для всех ценителей искусства и культуры.",
    #         "Приходите и проведите время с пользой и удовольствием!",
    #         "Отличная возможность научиться чему-то новому.",
    #         "Мероприятие для всей семьи с развлечениями на любой вкус.",
    #         "Соревнования с призовым фондом и зрелищными выступлениями.",
    #         "Встреча с известными авторами и обсуждение новых книг.",
    #         "Показ лучших фильмов года и встречи с режиссерами."
    #     ]
    #
    #     # Список возможных имен пользователей
    #     usernames = ["alex123", "margleb", "ivan_art", "sport_lover", "music_fan"]
    #
    #     # Генерируем 4 случайных события
    #     events = [
    #         Event(
    #             tg_user_id=100000 + i,  # Увеличиваем ID для каждого события
    #             image_id=''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10)),
    #             title=random.choice(titles),
    #             description=random.choice(descriptions),
    #             city=random.choice(list(CityEnum)).value,
    #             date=datetime.now() + timedelta(days=random.randint(1, 30)),
    #             username=random.choice(usernames)
    #         ) for i in range(1, 5)  # Генерируем 4 события
    #     ]
    #
    #     session.add_all([*events])
    #     await session.commit()

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )
    asyncio.run(main())