from datetime import date

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from sqlalchemy import and_, select, func

from dialogs.create_event.states import CreateEventDialog
from models import Event


async def on_date_selected(callback: CallbackQuery, widget, manager: DialogManager, selected_date: date):

    session = manager.middleware_data["session"]
    stmt = select(func.count(Event.id)).where(
        and_(
            Event.date == selected_date,
            Event.moderation  # True
        )
    )

    total_events = await session.scalar(stmt) or 0
    manager.dialog_data["total_events"] = total_events
    manager.dialog_data["selected_date"] = selected_date
    await manager.next()  # Переходим к следующему шагу


async def create_event(callback: CallbackQuery, widget, manager: DialogManager):
    selected_date = manager.dialog_data["selected_date"]
    await manager.start(CreateEventDialog.title, data={"selected_date": selected_date})