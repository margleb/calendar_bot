
from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot):

    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Создать/найти мероприятие'),
        BotCommand(command='/events',
                   description='Посмотреть свои мероприятия'),
        BotCommand(command='/support',
                   description='Связаться с разработчиком'),
    ]

    await bot.set_my_commands(main_menu_commands)