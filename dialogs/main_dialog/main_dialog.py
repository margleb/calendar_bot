from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Back
from aiogram_dialog.widgets.text import Const, Format
from dialogs.main_dialog.custom_calendar import EventCalendar
from dialogs.main_dialog.getters import dialog_data_getter
from dialogs.main_dialog.handlers import on_date_selected, create_event
from dialogs.main_dialog.states import MainDialog

dialog_main_dialog = Dialog(
    Window(
        Const("Выберите дату:"),
        EventCalendar(id='calendar', on_click=on_date_selected),
        state=MainDialog.main
    ),
    Window(
        Format("Вот что вы можете сделать на дату {selected_date}:"),
        Button(Const('Запланировать мероприятие'), id='create_event', on_click=create_event),
        Button(Const('Посмотреть список мероприятий'), id='show_events', when=F['dialog_data']['total_events'] > 0),
        Back(Const('Назад')),
        state=MainDialog.choice
    ),
    getter=dialog_data_getter
)