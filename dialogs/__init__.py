from aiogram import Router

from dialogs.common import start
from dialogs.user import calendar, account, join_events, my_events
from dialogs.user import create_event


def get_dialogs() -> list[Router]:
    return [
        start.dialog, # основное окно
        calendar.dialog, # календарь
        create_event.dialog, # создать события
        account.dialog, # аккаунт
        join_events.dialog, # мероприятия, к которым присоеденился
        my_events.dialog # мероприятия, которые создал
    ]