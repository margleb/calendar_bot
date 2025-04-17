from aiogram import F
from aiogram.enums import ContentType, ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.kbd import Cancel, Button, Row
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Jinja
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload

from db.models import User, Association, Event
from lexicon.lexicon import D_BUTTONS, DU_JOIN_EVENTS


class DJoinEvents(StatesGroup):
    events = State()


async def switch_event(callback_query: CallbackQuery, button: Button, manager: DialogManager):

    total_events = manager.dialog_data.get('total_events')
    offset = manager.dialog_data.get('offset', 0)

    # Увеличиваем или уменьшаем offset в зависимости от кнопки
    if button.widget_id == "next_event":
        offset = (offset + 1) % total_events
    elif button.widget_id == "prev_event":
        offset = (offset - 1 + total_events) % total_events

    manager.dialog_data['offset'] = offset


async def get_user_events(dialog_manager:DialogManager, **kwargs):
    session = dialog_manager.middleware_data['session']
    offset = dialog_manager.dialog_data.get('offset', 0)
    user_id = dialog_manager.event.from_user.id
    stmt = (
        select(
            Event,
            func.count(Event.id).over().label('total_events') # общее количество
        ).
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
        offset(offset).
        limit(1)
    )

    result = await session.execute(stmt)
    row = result.first()

    if row is None:
        return {'has_events': False}

    event, total_events = row
    dialog_manager.dialog_data['event_id'] = event.id
    dialog_manager.dialog_data['total_events'] = total_events
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
        'has_events': True,
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
DynamicMedia("photo", when=lambda data, widget, manager: data.get("photo") is not None),
        Jinja(DU_JOIN_EVENTS['result']),
        Button(Const(DU_JOIN_EVENTS['buttons']['cancel_event']), id='cancel_event', on_click=cancel_event, when=F['has_events']),
        Row(
            Button(Const(DU_JOIN_EVENTS['buttons']['prev_event']), id='prev_event', on_click=switch_event),
           Button(Const(DU_JOIN_EVENTS['buttons']['next_event']), id='next_event', on_click=switch_event),
           when=F['dialog_data']['total_events'] > 1
        ),
        Cancel(Const(D_BUTTONS['back'])),
        state=DJoinEvents.events,
        getter=get_user_events,
        parse_mode=ParseMode.HTML
    )
)