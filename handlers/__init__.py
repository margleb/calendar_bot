from aiogram import Router
from handlers import commands, admin

def get_routes() -> list[Router]:
    return [
        commands.router, # основные маршруты
        admin.router # маршруты админа
    ]