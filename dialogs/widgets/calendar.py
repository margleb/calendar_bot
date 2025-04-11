from datetime import datetime, timedelta

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import (
    Calendar,
    CalendarUserConfig,
    CalendarScope
)
from aiogram_dialog.widgets.kbd.calendar_kbd import (
    CalendarScopeView,
    CalendarDaysView,
    CalendarMonthView,
    CalendarYearsView
)

class EventCalendar(Calendar):

    def _init_views(self) -> dict[CalendarScope, CalendarScopeView]:
        return {
            CalendarScope.DAYS: CalendarDaysView(self._item_callback_data),
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