from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy import delete, update

from models import Event


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


async def on_accept_event(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):

    session = dialog_manager.middleware_data.get("session")
    event_id = dialog_manager.dialog_data.get("event_id")
    stmt = update(Event).where(Event.id == event_id).values({"moderation": True})

    await session.execute(stmt)
    await session.commit()

async def on_reject_event(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):

    session = dialog_manager.middleware_data.get("session")
    event_id = dialog_manager.dialog_data.get("event_id")
    stmt = delete(Event).where(Event.id == event_id)

    await session.execute(stmt)
    await session.commit()