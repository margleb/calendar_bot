from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format, Jinja
from sqlalchemy import select, func

from models import Event


class ModerateEvents(StatesGroup):
    events = State()


async def get_events_data(dialog_manager, **kwargs):
    # Получаем текущий индекс из данных диалога
    current_index = dialog_manager.dialog_data.get("current_index", 0)

    # Получаем общее количество событий
    session = dialog_manager.middleware_data.get("session")
    total_events = await session.scalar(select(func.count(Event.id)).where(Event.moderation == False))

    # Получаем текущее событие
    stmt = select(Event).order_by(Event.id).offset(current_index).limit(1)
    current_event = await session.scalar(stmt)

    return {
        "event": current_event,
        "current_position": current_index + 1,
        "total_events": total_events,
    }


async def on_prev_event(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    current_index = dialog_manager.dialog_data.get("current_index", 0)
    if current_index > 0:
        dialog_manager.dialog_data["current_index"] = current_index - 1


async def on_next_event(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    current_index = dialog_manager.dialog_data.get("current_index", 0)
    session = dialog_manager.middleware_data.get("session")
    total_events = await session.scalar(select(func.count(Event.id)))

    if current_index < total_events - 1:
        dialog_manager.dialog_data["current_index"] = current_index + 1


dialog_moderate_dialog = Dialog(
    Window(
        Jinja(
            "\n\n"
            "{{event.description}}\n\n"
            "<b>______</b>\n"
            "<b>Что:</b> {{event.title}}\n"
            "<b>Где:</b> {{event.city.value}}\n"
            "<b>Когда:</b> {{event.date}}\n"
            "<b>Пишите:</b> @{{event.username}}\n"
        ),
        Row(
            Button(Const("◀ Назад"), id="prev_event", on_click=on_prev_event),
            Button(Const("▶ Вперед"), id="next_event", on_click=on_next_event),
        ),
        parse_mode="HTML",
        state=ModerateEvents.events,
        getter=get_events_data
    )
)