from aiogram import Router

from dialogs.common import start
from dialogs.user import calendar


def get_dialogs() -> list[Router]:
    return [
        start.dialog, # основное окно
        calendar.dialog # календарь
    ]