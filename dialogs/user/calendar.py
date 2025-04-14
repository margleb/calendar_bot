from typing import Any

from aiogram import F
from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Cancel, Next, Back, Column, Button, Row, Group
from aiogram_dialog.widgets.text import Const, Format, Jinja
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload, with_loader_criteria

from db.models import Event, User
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
    offset = dialog_manager.dialog_data.get('offset')

    # Получаем здесь кол-во мероприятий для того, чтобы отработал when в row для кнопок
    stmt = select(func.count(Event.id)).where(Event.date_event == date_event)
    total_events = await session.scalar(stmt)
    dialog_manager.dialog_data['total_events'] = total_events

    stmt = (
        select(Event).
        options(selectinload(Event.user)).
        where(Event.date_event == date_event)
        .offset(offset)  # смещение
        .limit(1) # одна запись всегда
    )

    event = await session.scalar(stmt)
    dialog_manager.dialog_data['event_id'] = event.id

    current_usr_id = dialog_manager.event.from_user.id
    join_count = sum(1 for assoc in event.user if assoc.status == 'join')
    already_join = any(assoc.user_id == current_usr_id and assoc.status == 'join' for assoc in event.user)
    is_owner = any(assoc.user_id == current_usr_id and assoc.status == 'create' for assoc in event.user)

    return {
        'title': event.title,
        'description': event.description,
        'date': event.date_event,
        'city': event.city.value,
        'username': event.username,
        'is_owner': is_owner, # является ли создателем мероприятия
        'already_join': already_join, # присоединился ли к мероприятию
        'join_count': join_count, # количество присоединившеюся
    }

async def switch_event(callback_query: CallbackQuery, button: Button, manager: DialogManager):

    total_events = manager.dialog_data.get('total_events')
    offset = manager.dialog_data.get('offset', 0)

    # Увеличиваем или уменьшаем offset в зависимости от кнопки
    if button.widget_id == "next_event":
        offset = (offset + 1) % total_events
    elif button.widget_id == "prev_event":
        offset = (offset - 1 + total_events) % total_events

    manager.dialog_data['offset'] = offset

async def toggle_event(callback_query: CallbackQuery, button: Button, manager: DialogManager):
    session = manager.middleware_data.get('session')
    event_id = manager.dialog_data.get('event_id')
    user_id = callback_query.from_user.id

    # Проверяем, есть ли уже запись
    stmt = select(Association).where(
        Association.user_id == user_id,
        Association.event_id == event_id,
        Association.status == 'join'
    )
    result = await session.execute(stmt)
    existing_assoc = result.scalar_one_or_none()

    if existing_assoc:
        # Удаляем существующую запись
        await session.delete(existing_assoc)
    else:
        # Добавляем новую
        assoc = Association(
            user_id=user_id,
            event_id=event_id,
            status='join'
        )
        session.add(assoc)

    await session.commit()

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
        Group(
            Button(
                Const(DU_CALENDAR['buttons']['join_event']),
                id='join_event',
                on_click=toggle_event,
                when=~F['already_join']
            ),
            Button(
                Const(DU_CALENDAR['buttons']['cancel_event']),
                id='join_event',
                on_click=toggle_event,
                when=F['already_join']
            ),
            when=~F['is_owner']
        ),
        Row(
            Button(Const(DU_CALENDAR['buttons']['next_event']), id='prev_event', on_click=switch_event),
            Button(Const(DU_CALENDAR['buttons']['prev_event']), id='next_event', on_click=switch_event),
            when=F['dialog_data']['total_events'] > 1 # показывается если событий больше одного
        ),
        Back(Const(D_BUTTONS['back'])),
        getter=get_current_event,
        parse_mode=ParseMode.HTML,
        state=DCalendar.events
    ),
    getter=get_dialog_data,
)