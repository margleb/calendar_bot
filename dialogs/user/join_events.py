from aiogram import F
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

from db.models import User, Association, Event
from lexicon.lexicon import D_BUTTONS, DU_JOIN_EVENTS


class DJoinEvents(StatesGroup):
    events = State()

async def get_user_events(dialog_manager:DialogManager, **kwargs):
    session = dialog_manager.middleware_data['session']
    user_id = dialog_manager.event.from_user.id
    stmt = (
        select(Event).
        join(Event.user). # association
        join(Association.user). # event
        options(selectinload(Event.user)). # получаем в ассоциативной таблице ВСЕХ пользователей
        where(
            and_(
                User.telegram_id == user_id, # только текущего пользователя
                Association.status == 'join', # только мероприятия к которым присоединился
                Event.date_event >= func.current_date() # текущая или позже дата
            )
        ).
        # offset(1).
        limit(1)
    )

    # print(stmt.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))

    event = await session.scalar(stmt)
    if event is None:
        return {
            'has_event': False,
        }
    else:
        dialog_manager.dialog_data['event_id'] = event.id

    total_join = sum(1 for assoc in event.user if assoc.status == 'join')

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
        'has_event': True
    }


async def cancel_event(callback_query: CallbackQuery, button: Button, manager: DialogManager):

    session = manager.middleware_data.get('session')
    event_id = manager.dialog_data.get('event_id')
    user_id = callback_query.from_user.id

    # Проверяем, есть ли уже запись
    stmt = select(Association).where(
        Association.user_id == user_id,
        Association.event_id == event_id,
        Association.status == 'join'
    )

    existing_assoc = await session.scalar(stmt)

    # Удаляем существующую запись
    await session.delete(existing_assoc)
    await session.commit()


dialog = Dialog(
    Window(
        Jinja(DU_JOIN_EVENTS['result']),
        Button(Const(DU_JOIN_EVENTS['buttons']['cancel_event']), id='cancel_event', on_click=cancel_event, when=F['has_event']),
        Cancel(Const(D_BUTTONS['back'])),
        state=DJoinEvents.events,
        getter=get_user_events,
        parse_mode=ParseMode.HTML
    )
)