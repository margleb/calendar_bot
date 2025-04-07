from itertools import count

from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from models import Event


async def dialog_data_getter(dialog_manager: DialogManager, **kwargs):
    dialog_data = dialog_manager.dialog_data
    return {
        'selected_date': dialog_data.get('selected_date'),
        'total_events': dialog_data.get('total_events')
    }

async def get_events_data(dialog_manager: DialogManager, **kwargs) -> dict:

    session = dialog_manager.middleware_data.get("session")
    current_index = dialog_manager.dialog_data.get("current_index", 0)

    # Получаем событие для модерации
    event = await session.scalar(
        select(Event)
        .where(
            and_(
                Event.date == dialog_manager.dialog_data['selected_date'],
                Event.moderation  # True
            )
        )
        .options(selectinload(Event.users))
        .limit(1)
        .offset(current_index)
    )

    # Получаем количество пользователей
    users_count = len(event.users) if event.users else 0

    # Если события есть
    image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(event.image_id))
    dialog_manager.dialog_data['event_id'] = event.id

    return {
        "title": event.title,
        "description": event.description,
        'participants': f"{event.participants}/{users_count}",
        "photo": image,
        "city": event.city.value,
        "date": event.date,
        "username": event.username,
    }