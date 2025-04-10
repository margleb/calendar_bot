from aiogram import Router
from handlers import commands, admin

def get_routes() -> list[Router]:
    return [
        # admin.router,  # маршруты админа
        commands.router, # основные маршруты
    ]