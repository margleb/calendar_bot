from datetime import date

from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const

from dialogs.main_dialog.custom_calendar import EventCalendarDaysView, EventCalendar


class MainDialog(StatesGroup):
    main = State()


async def on_date_selected(callback: CallbackQuery, widget,
                           manager: DialogManager, selected_date: date):
    await callback.answer(str(selected_date))


dialog_main_dialog = Dialog(
    Window(
        Const("Выберите дату:"),
        EventCalendar(id='calendar', on_click=on_date_selected),
        state=MainDialog.main
    ),
)