from datetime import date, datetime

from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Column, Back
from aiogram_dialog.widgets.text import Const, Format

from dialogs.create_event.states import CreateEventDialog
from dialogs.main_dialog.custom_calendar import EventCalendar


class MainDialog(StatesGroup):
    main = State()
    choice = State()


async def on_date_selected(callback: CallbackQuery, widget, manager: DialogManager, selected_date: date):
    manager.dialog_data["selected_date"] = selected_date
    await manager.next()  # Переходим к следующему шагу

async def get_current_date(dialog_manager: DialogManager, **kwargs):
    dialog_data = dialog_manager.dialog_data
    return {
        'selected_date': await dialog_data.get('selected_date'),
    }

async def create_event(callback: CallbackQuery, widget, manager: DialogManager):
    await manager.start(CreateEventDialog.title)

dialog_main_dialog = Dialog(
    Window(
        Const("Выберите дату:"),
        EventCalendar(id='calendar', on_click=on_date_selected),
        state=MainDialog.main
    ),
    Window(
        Format('Вот что можете сделать на дату {selected_date}:'),
        Column(
            Button(Const('Посмотреть мероприятия'), id='show_events'),
            Button(Const('Запланировать мероприятие'), id='create_event', on_click=create_event)
        ),
        Back(Const('Назад')),
        # getter=get_current_date,
        state=MainDialog.choice
    ),
    Window()
)