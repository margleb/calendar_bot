from datetime import datetime, timedelta, date
from aiogram.types import InlineKeyboardButton

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import (
    Calendar,
    CalendarUserConfig,
    CalendarScope
)
from aiogram_dialog.widgets.kbd.calendar_kbd import (
    CalendarScopeView,
    CalendarMonthView,
    CalendarYearsView, CalendarDaysView, raw_from_date, CallbackGenerator
)

class EventCalendarDaysView(CalendarDaysView):
    def __init__(self, callback_generator: CallbackGenerator, **kwargs):
        super().__init__(callback_generator)

    async def _render_date_button(
            self,
            selected_date: date,
            today: date,
            data: dict,
            manager: DialogManager,
    ) -> InlineKeyboardButton:
        current_data = {
            "date": selected_date,
            "data": data,
        }
        if selected_date == today:
            text = self.today_text
        else:
            text = self.date_text

        raw_date = raw_from_date(selected_date)

        suffix = "🔥"
        rendered_text = await text.render_text(current_data, manager)

        return InlineKeyboardButton(
            # text=f"{suffix}{rendered_text}",
            text=f"{suffix}",
            callback_data=self.callback_generator(str(raw_date)),
        )

class EventCalendar(Calendar):

    def _init_views(self) -> dict[CalendarScope, CalendarScopeView]:
        return {
            CalendarScope.DAYS: EventCalendarDaysView(self._item_callback_data),
            CalendarScope.MONTHS: CalendarMonthView(self._item_callback_data),
            CalendarScope.YEARS: CalendarYearsView(self._item_callback_data),
        }

    async def _get_user_config(
            self,
            data: dict,
            manager: DialogManager,
    ) -> CalendarUserConfig:

        today = datetime.now().date() # текущая дата
        max_date = today + timedelta(days=180) # 6 месяцев
        return CalendarUserConfig(
            min_date=today, # минимальная дата - сегодня
            max_date=max_date, # максимальная дата - не более полугода
        )