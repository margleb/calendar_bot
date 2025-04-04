from aiogram import F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format, Jinja
from sqlalchemy import select, func, update

from models import Event


class ModerateEvents(StatesGroup):
    events = State()


async def get_events_data(dialog_manager: DialogManager, **kwargs) -> dict:
    session = dialog_manager.middleware_data.get("session")
    current_index = dialog_manager.dialog_data.get("current_index")

    event = await session.scalar(select(Event).where(Event.moderation.is_(False)).limit(1).offset(current_index))
    total_events = await session.scalar(select(func.count(Event.id)).where(Event.moderation.is_(False)))
    dialog_manager.dialog_data['total_events'] = total_events
    dialog_manager.dialog_data['event_id'] = event.id

    return {
        "description": event.description,
        "title": event.title,
        "city": event.city.value,
        "date": event.date,
        "username": event.username,
    }


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

dialog_moderate_dialog = Dialog(
    Window(
        Jinja(
            "{{description}}\n\n"
            "<b>______</b>\n\n"
            "<b>Что</b> {{title}}\n"
            "<b>Где:</b> {{city}}\n"
            "<b>Когда:</b> {{date}}\n"
            "<b>Пишите:</b> @{{username}}\n"
        ),
        Row(
            Button(Const("◀ Назад"), id="prev_event", on_click=on_prev_event, when=F["dialog_data"]["total_events"] > 1),
            Button(Const("✅ Принять"), id="accept_event", on_click=on_accept_event),
            Button(Const("❌ Отклонить"), id="reject_event"),
            Button(Const("▶ Вперед"), id="next_event", on_click=on_next_event, when=F["dialog_data"]["total_events"] > 1),
        ),
        parse_mode="HTML",
        state=ModerateEvents.events,
        getter=get_events_data
    )
)