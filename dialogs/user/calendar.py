from typing import Any

from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Cancel, Next, Start, Back, Column, Button, Row
from aiogram_dialog.widgets.text import Const, Format, Jinja
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload

from db.models import Event
from db.models.Association import Association
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

async def get_current_event(dialog_manager: DialogManager, **kwargs) -> dict:
    session = dialog_manager.middleware_data.get('session')
    date_event = dialog_manager.dialog_data.get('date')
    stmt = (
        select(Event).
        join(Association).
        options(
            selectinload(Event.user). # подгружаем пользователя
            selectinload(Association.user) # ассоциативная таблица
        ).
        where(
            and_(
                Event.date_event == date_event, # за эту дату
                Association.status == 'create' # находим только созданные
            )
        )
        .offset(0)  # смещение
    )
    event = await session.scalar(stmt)
    return {
        'title': event.title,
        'description': event.description,
        'date': event.date_event,
        'city': event.city.value,
        'username': event.user[0].user.username,
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
        Jinja(DU_CALENDAR['result']),
        Row(
            Button(Const('<<'), id='prev_event'),
            Button(Const('>>'), id='next_event')
        ),
        Back(Const(D_BUTTONS['back'])),
        getter=get_current_event,
        parse_mode=ParseMode.HTML,
        state=DCalendar.events
    ),
    getter=get_dialog_data,
)