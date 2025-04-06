from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId, EventContext
from sqlalchemy import func, select, and_

from models import Event

async def get_events_data(dialog_manager: DialogManager, event_context: EventContext, **kwargs) -> dict:
    session = dialog_manager.middleware_data.get("session")
    current_index = dialog_manager.dialog_data.get("current_index", 0)

    # Получаем событие для модерации
    event = await session.scalar(
        select(Event)
        .where(Event.tg_user_id == event_context.user.id)
        .limit(1)
        .offset(current_index)
    )

    # Получаем общее количество событий для модерации
    total_events = await session.scalar(
        select(func.count(Event.id))
        .where(Event.tg_user_id == event_context.user.id)
    )

    # Если событий нет
    if not event:
        dialog_manager.dialog_data['no_events'] = True
        return {
            "no_events": True,
            "message": "Вами не создано ни одного события. Создайте событие /start"
        }

    # Если события есть
    dialog_manager.dialog_data['total_events'] = total_events
    dialog_manager.dialog_data['event_id'] = event.id

    image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(event.image_id))

    return {
        "title": event.title,
        "description": event.description,
        "photo": image,
        "city": event.city.value,
        "date": event.date,
        "username": event.username,
        "moderate": event.moderation,
    }