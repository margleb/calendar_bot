from aiogram.enums import ContentType, ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.kbd import Cancel, Button
from aiogram_dialog.widgets.text import Const, Jinja
from sqlalchemy import select, and_, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import selectinload

from db.models import Event, Association
from lexicon.lexicon import D_BUTTONS, DU_MY_EVENTS


class DMyEvents(StatesGroup):
    events = State()


async def get_event(dialog_manager:DialogManager, **kwargs) -> dict:

    session = dialog_manager.middleware_data.get('session')

    stmt = (
        select(
            Event,
            func.count(Event.id).over().label('total_events') # общее количество
        )
        .join(Event.user). # association
        options(selectinload(Event.user)).  # получаем в ассоциативной таблице ВСЕХ пользователей
        where(
            and_(
                Event.user.any(
                    user_id=dialog_manager.event.from_user.id,
                    status='create'
                ), # Используем any для проверки наличия
                Event.date_event >=  func.current_date()
            )
        )
        # .offset(1)
        .limit(1)
    )

    result = await session.execute(stmt)
    row = result.first()
    if row is None:
        return {'has_events': False}

    event, total_events = row
    dialog_manager.dialog_data['event_id'] = event.id
    dialog_manager.dialog_data['total_events'] = total_events
    total_join = sum(1 for assoc in event.user if assoc.status == 'join')

    event = await session.scalar(stmt)

    photo = None
    if event.image_id:
        photo = MediaAttachment(ContentType.PHOTO, file_id=MediaId(event.image_id))

    return {
        'title': event.title,
        'description': event.description,
        'photo': photo,
        'participants': f"{event.participants}/{total_join}",
        'date': event.date_event,
        'city': event.city.value,
        'username': event.username,
        'has_events': True,
    }


dialog = Dialog(
    Window(
      Jinja(DU_MY_EVENTS['result']),
      Button(Const(DU_MY_EVENTS['buttons']['delete_event']), id='delete_event'),
      Cancel(Const(D_BUTTONS['back'])),
      getter=get_event,
      parse_mode=ParseMode.HTML,
      state=DMyEvents.events
    )
)