from aiogram import F
from aiogram.enums import ContentType
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.kbd import Button, Back, Next, Row
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Jinja
from sqlalchemy import select

from dialogs.main_dialog.custom_calendar import EventCalendar
from dialogs.main_dialog.getters import dialog_data_getter
from dialogs.main_dialog.handlers import on_date_selected, create_event
from dialogs.main_dialog.states import MainDialog
from models import Event


async def get_events_data(dialog_manager: DialogManager, **kwargs) -> dict:

    session = dialog_manager.middleware_data.get("session")
    current_index = dialog_manager.dialog_data.get("current_index", 0)

    # Получаем событие для модерации
    event = await session.scalar(
        select(Event)
        .where(Event.moderation.is_(True))
        .limit(1)
        .offset(current_index)
    )

    # Если события есть
    image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(event.image_id))

    return {
        "title": event.title,
        "description": event.description,
        "photo": image,
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

dialog_main_dialog = Dialog(
    Window(
        Const("Выберите дату:"),
        EventCalendar(id='calendar', on_click=on_date_selected),
        state=MainDialog.main
    ),
    Window(
        Format("Вот что вы можете сделать на дату {selected_date}:"),
        Button(Const('Запланировать мероприятие'), id='create_event', on_click=create_event),
        Next(Const('Посмотреть список мероприятий'), id='show_events', when=F['dialog_data']['total_events'] > 0),
        Back(Const('Назад')),
        state=MainDialog.choice
    ),
    Window(
        DynamicMedia("photo", when=~F["dialog_data"]["no_events"]),
        Jinja(
            "{{description}}\n\n"
            "<b>______</b>\n\n"
            "<b>Что</b> {{title}}\n"
            "<b>Где:</b> {{city}}\n"
            "<b>Когда:</b> {{date}}\n"
            "<b>Пишите:</b> @{{username}}\n"
        ),
        Row(
            Button(Const("◀ Назад"), id="prev_event", on_click=on_prev_event,
                   when=F["dialog_data"]["total_events"] > 1),
            Button(Const("▶ Вперед"), id="next_event", on_click=on_next_event,
                   when=F["dialog_data"]["total_events"] > 1),
        ),
        Back(Const('Назад')),
        parse_mode="HTML",
        getter=get_events_data,
        state=MainDialog.choose_event
    ),
    getter=dialog_data_getter
)