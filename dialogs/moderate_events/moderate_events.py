from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Jinja

from dialogs.moderate_events.getters import get_events_data
from dialogs.moderate_events.handlers import on_prev_event, on_accept_event, on_reject_event, on_next_event
from dialogs.moderate_events.states import ModerateEvents

dialog_moderate_dialog = Dialog(
    Window(
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
            "{% endif %}"
        ),
        Row(
            Button(Const("◀ Назад"), id="prev_event", on_click=on_prev_event, when=~F["dialog_data"]["no_events"] & (F["dialog_data"]["total_events"] > 1)),
            Button(Const("✅ Принять"), id="accept_event", on_click=on_accept_event, when=~F["dialog_data"]["no_events"]),
            Button(Const("❌ Отклонить"), id="reject_event", on_click=on_reject_event, when=~F["dialog_data"]["no_events"]),
            Button(Const("▶ Вперед"), id="next_event", on_click=on_next_event, when=~F["dialog_data"]["no_events"] & (F["dialog_data"]["total_events"] > 1)),
        ),
        parse_mode="HTML",
        state=ModerateEvents.events,
        getter=get_events_data
    )
)