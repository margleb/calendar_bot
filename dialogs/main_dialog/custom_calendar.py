from datetime import date

from aiogram.types import InlineKeyboardButton
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd.calendar_kbd import CalendarScopeView, CalendarDaysView, Calendar, CalendarScope, \
    CalendarMonthView, CalendarYearsView
from aiogram_dialog.widgets.text import Format
from sqlalchemy import select, and_

from models import Event

EPOCH = date(1970, 1, 1)


def raw_from_date(d: date) -> int:
    diff = d - EPOCH
    return int(diff.total_seconds())


class EventCalendarDaysView(CalendarDaysView):
    async def _render_date_button(
            self,
            selected_date: date,
            today: date,
            data: dict,
            manager: DialogManager,
    ) -> InlineKeyboardButton:

        session = manager.middleware_data["session"]
        stmt = select(Event.id).where(
            and_(
                Event.date == selected_date,
                Event.moderation # True
            )
        )
        total_events = await session.scalar(stmt) or 0

        current_data = {
            "date": selected_date,
            "data": data,
        }
        if selected_date == today:
            text = self.today_text
        elif total_events > 0:
            text = self.date_text + f" событий: ({total_events})"
        else:
            text = self.date_text

        raw_date = raw_from_date(selected_date)

        return InlineKeyboardButton(
            text=await text.render_text(
                current_data, manager,
            ),
            callback_data=self.callback_generator(str(raw_date)),
        )

class EventCalendar(Calendar):
    def _init_views(self) -> dict[CalendarScope, CalendarScopeView]:
        return {
            CalendarScope.DAYS: EventCalendarDaysView(
                self._item_callback_data,
                date_text=Format("{date:%d}"),
            ),
            CalendarScope.MONTHS: CalendarMonthView(self._item_callback_data),
            CalendarScope.YEARS: CalendarYearsView(self._item_callback_data),
        }