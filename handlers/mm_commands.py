from aiogram import Bot
from aiogram.types import BotCommand


# Создаем асинхронную функцию
async def set_main_menu(bot: Bot):

    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Начать пользоваться ботом'),
        BotCommand(command='/support',
                   description='Поддержка'),
        BotCommand(command='/account',
                   description='Перейти в аккаунт'),
        BotCommand(command='/calendar',
                   description='Перейти в календарь'),
    ]

    await bot.set_my_commands(main_menu_commands)