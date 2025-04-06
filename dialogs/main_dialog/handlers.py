from datetime import date

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy import and_, select, func

from dialogs.create_event.states import CreateEventDialog
from models import Event


async def on_date_selected(callback: CallbackQuery, widget, manager: DialogManager, selected_date: date):

    session = manager.middleware_data["session"]
    selected_city = manager.dialog_data["selected_city"]
    stmt = select(func.count(Event.id)).where(
        and_(
            Event.date == selected_date,
            Event.city == selected_city,
            Event.moderation  # True
        )
    )

    total_events = await session.scalar(stmt) or 0
    manager.dialog_data["total_events"] = total_events
    manager.dialog_data["selected_date"] = selected_date
    await manager.next()  # Переходим к следующему шагу


async def create_event(callback: CallbackQuery, widget, manager: DialogManager):
    selected_date = manager.dialog_data["selected_date"]
    selected_city = manager.dialog_data["selected_city"]
    await manager.start(CreateEventDialog.title, data={"selected_date": selected_date, "selected_city": selected_city})


async def on_prev_event(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    data = dialog_manager.dialog_data
    current_index = data.get("current_index", 0)
    total_events = data["total_events"]  # Без .get(), так как total_events должен быть

    data["current_index"] = (current_index - 1) % total_events


async def on_next_event(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    data = dialog_manager.dialog_data
    current_index = data.get("current_index", 0)
    total_events = data["total_events"]

    data["current_index"] = (current_index + 1) % total_events

async def on_select_city(callback: CallbackQuery, widget, manager: DialogManager, selected_city: str):
    manager.dialog_data["selected_city"] = selected_city
    await manager.next()