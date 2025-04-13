from aiogram import Router

from dialogs.common import start
from dialogs.user import calendar
from dialogs.user import create_event


def get_dialogs() -> list[Router]:
    return [
        start.dialog, # основное окно
        calendar.dialog, # календарь
        create_event.dialog # создать события
    ]