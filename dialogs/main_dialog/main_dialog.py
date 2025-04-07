from aiogram import F

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Back, Next, Row, Select
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Jinja

from dialogs.main_dialog.custom_calendar import EventCalendar
from dialogs.main_dialog.getters import dialog_data_getter, get_events_data
from dialogs.main_dialog.handlers import on_date_selected, create_event, on_prev_event, on_next_event, on_select_city
from dialogs.main_dialog.states import MainDialog


dialog_main_dialog = Dialog(
    Window(
        Const("В каком городе вы хотите посмотреть/создать мероприятие?"),
        Select(
            Format("{item}"),
            id='city',
            item_id_getter=lambda x: x,
            items=['Москва', 'Санкт-Петербург'],
            on_click=on_select_city
        ),
        state=MainDialog.city
    ),
    Window(
        Const("Выберите дату:"),
        EventCalendar(id='calendar', on_click=on_date_selected),
        Back(Const('Назад')),
        state=MainDialog.calendar
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
            # Button(Const("Я иду"), id="join_event"),
            # Button(Const("Я не пойду"), id="join_event"),
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