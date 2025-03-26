from aiogram import Router

from handlers import main_handlers


def get_routers() -> list[Router]:
    return [
        main_handlers.router
    ]