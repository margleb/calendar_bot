from aiogram import F
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Row, Next, Back
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Jinja, List, Format
from sqlalchemy import select

from dialogs.my_events.getters import get_events_data
from dialogs.my_events.handlers import on_prev_event, on_next_event, on_reject_event
from dialogs.my_events.states import MyEvents
from models import EventUsers


async def get_event_participants(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data['session']
    event_id = dialog_manager.dialog_data['event_id']

    smtp = select(EventUsers.tg_username).where(
        EventUsers.event_id == event_id
    )

    result = await session.execute(smtp)
    participants = result.scalars().all()

    return {
        'usernames': participants
    }

dialog_my_events_dialog = Dialog(
    Window(
DynamicMedia("photo", when=~F["dialog_data"]["no_events"]),
        Jinja(
            "{% if no_events %}"
            "{{message}}"
            "{% else %}"
            "{{description}}\n\n"
            "<b>______</b>\n\n"
            "<b>Что</b> {{title}}\n"
            "<b>Где:</b> {{city}}\n"
            "<b>Когда:</b> {{date}}\n"
            "<b>Пишите:</b> @{{username}}\n"
            "<b>Участников:</b> {{participants}}\n"
            "<b>Модерация:</b> {% if moderate %}одобрено{% else %}на модерации{% endif %}\n"
            "{% endif %}"
        ),
        Row(
            Button(Const("◀ Назад"), id="prev_event", on_click=on_prev_event, when=~F["dialog_data"]["no_events"] & (F["dialog_data"]["total_events"] > 1)),
            Button(Const("❌ Удалить"), id="reject_event", on_click=on_reject_event, when=~F["dialog_data"]["no_events"]),
            Button(Const("▶ Вперед"), id="next_event", on_click=on_next_event, when=~F["dialog_data"]["no_events"] & (F["dialog_data"]["total_events"] > 1)),
        ),
        Button(Const('Посмотреть участников'), id='show_participants', on_click=Next(), when=~F["dialog_data"]["no_events"]),
        parse_mode="HTML",
        state=MyEvents.events,
        getter=get_events_data
    ),
    Window(
        Const('Участники мероприятия:'),
        List(
            Format("@{item}"),  # Используем {item}, а не {username}
            items="usernames",  # Берет список из ключа 'usernames'
        ),
        Back(Const('Назад')),
        state=MyEvents.participants,
        getter=get_event_participants  # Передаем функцию-геттер
    )
)