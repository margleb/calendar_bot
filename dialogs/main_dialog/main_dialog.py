from datetime import date, datetime
from operator import and_

from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Column, Back, Row
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Jinja
from sqlalchemy import select

from dialogs.create_event.states import CreateEventDialog
from dialogs.main_dialog.custom_calendar import EventCalendar
from models import Event


class MainDialog(StatesGroup):
    main = State()
    choice = State()
    choose_event = State()


async def on_date_selected(callback: CallbackQuery, widget, manager: DialogManager, selected_date: date):
    session = manager.middleware_data["session"]
    stmt = select(Event.id).where(
        and_(
            Event.date == selected_date,
            Event.moderation  # True
        )
    )
    total_events = await session.scalar(stmt) or 0
    if total_events == 0:
        await callback.answer('Нет на текущую дату событий, выберите другую')
    else:
        manager.dialog_data["selected_date"] = selected_date
        await manager.next()  # Переходим к следующему шагу


async def get_current_date(dialog_manager: DialogManager, **kwargs):
    dialog_data = dialog_manager.dialog_data
    return {
        'selected_date': dialog_data.get('selected_date'),
    }

async def create_event(callback: CallbackQuery, widget, manager: DialogManager):
    await manager.start(CreateEventDialog.title)

dialog_main_dialog = Dialog(
    Window(
        Const("Выберите дату:"),
        EventCalendar(id='calendar', on_click=on_date_selected),
        state=MainDialog.main
    ),
    Window(
        Format('Вот что можете сделать на дату {selected_date}:'),
        Column(
            Button(Const('Посмотреть мероприятия'), id='show_events'),
            Button(Const('Запланировать мероприятие'), id='create_event', on_click=create_event)
        ),
        Back(Const('Назад')),
        getter=get_current_date,
        state=MainDialog.choice
    ),
    # Window(
    #     DynamicMedia("photo", when=~F["dialog_data"]["no_events"]),
    #     Jinja(
    #         "{{description}}\n\n"
    #         "<b>______</b>\n\n"
    #         "<b>Что</b> {{title}}\n"
    #         "<b>Где:</b> {{city}}\n"
    #         "<b>Когда:</b> {{date}}\n"
    #         "<b>Пишите:</b> @{{username}}\n"
    #     ),
    #     Row(
    #         Button(Const("◀ Назад"), id="prev_event", on_click=on_prev_event,
    #                when=~F["dialog_data"]["no_events"] & (F["dialog_data"]["total_events"] > 1)),
    #         Button(Const("▶ Вперед"), id="next_event", on_click=on_next_event,
    #                when=~F["dialog_data"]["no_events"] & (F["dialog_data"]["total_events"] > 1)),
    #     ),
    #     parse_mode="HTML",
    #     state=MainDialog.choose_event,
    #     getter=get_events_data
    # )
)