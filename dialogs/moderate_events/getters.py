from aiogram_dialog import DialogManager
from sqlalchemy import select, func

from models import Event


async def get_events_data(dialog_manager: DialogManager, **kwargs) -> dict:
    session = dialog_manager.middleware_data.get("session")
    current_index = dialog_manager.dialog_data.get("current_index", 0)

    # Получаем событие для модерации
    event = await session.scalar(
        select(Event)
        .where(Event.moderation.is_(False))
        .limit(1)
        .offset(current_index)
    )

    # Получаем общее количество событий для модерации
    total_events = await session.scalar(
        select(func.count(Event.id))
        .where(Event.moderation.is_(False))
    )

    # Если событий нет
    if not event:
        dialog_manager.dialog_data['no_events'] = True
        return {
            "no_events": True,
            "message": "Нет событий для модерации"
        }

    # Если события есть
    dialog_manager.dialog_data['total_events'] = total_events
    dialog_manager.dialog_data['event_id'] = event.id
    dialog_manager.dialog_data['no_events'] = False

    return {
        "description": event.description,
        "title": event.title,
        "city": event.city.value,
        "date": event.date,
        "username": event.username,
    }