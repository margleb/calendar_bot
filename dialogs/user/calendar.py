from typing import Any

from aiogram import F
from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Cancel, Next, Start, Back, Column, Button
from aiogram_dialog.widgets.text import Const, Format

from dialogs.user.create_event import CreateEvent
from dialogs.widgets.calendar import EventCalendar
from lexicon.lexicon import DU_CALENDAR, D_BUTTONS
from datetime import date

class DCalendar(StatesGroup):
    city = State() # выбор города
    calendar = State() # выбор даты в календаре
    choice = State() # выбор действия (создать/посмотреть)
    events = State() # список мероприятий


async def on_city_selected(callback: CallbackQuery, widget: Any, manager: DialogManager, selected_city: str):
    manager.dialog_data['city'] = selected_city
    await manager.next()


async def on_date_selected(callback: CallbackQuery, widget, manager: DialogManager, selected_date: date):
    manager.dialog_data['date'] = selected_date
    await manager.next()


async def on_start_create_event(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(CreateEvent.title, data=manager.dialog_data)


async def get_dialog_data(dialog_manager: DialogManager, **kwargs) -> dict:
    return {
        'city': dialog_manager.dialog_data.get('city'),
        'date': dialog_manager.dialog_data.get('date')
    }



dialog = Dialog(
    Window(
        Const(DU_CALENDAR['city']),
        Select(
            Format("{item}"),
            id='city',
            item_id_getter=str,
            items=['Москва', 'Санкт-Петербург'],
            on_click=on_city_selected
        ),
        Cancel(Const(D_BUTTONS['back'])),
        parse_mode=ParseMode.HTML,
        state=DCalendar.city
    ),
    Window(
        Const(DU_CALENDAR['calendar']),
        EventCalendar(
            id='calendar',
            on_click=on_date_selected
        ),
        Back(Const(D_BUTTONS['back'])),
        parse_mode=ParseMode.HTML,
        state=DCalendar.calendar
    ),
    Window(
        Format(DU_CALENDAR['choice']),
        Column(
            Next(
                Const(DU_CALENDAR['buttons']['show_events']),
                id='show_events'
            ),
            Button(
                Const(DU_CALENDAR['buttons']['create_event']),
                id='create_event',
                on_click=on_start_create_event,
            ),
            Back(Const(D_BUTTONS['back'])),
        ),
        parse_mode=ParseMode.HTML,
        state=DCalendar.choice
    ),
    Window(
        Format(DU_CALENDAR['events']),
        Back(Const(D_BUTTONS['back'])),
        parse_mode=ParseMode.HTML,
        state=DCalendar.events
    ),
    getter=get_dialog_data,
)