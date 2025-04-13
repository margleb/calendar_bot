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
        # BotCommand(command='/contacts',
        #            description='Другие способы связи'),
        # BotCommand(command='/payments',
        #            description='Платежи')
    ]

    await bot.set_my_commands(main_menu_commands)