from datetime import date, datetime

from aiogram.types import InlineKeyboardButton
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd.calendar_kbd import CalendarScopeView, CalendarDaysView, Calendar, CalendarScope, \
    CalendarMonthView, CalendarYearsView, CalendarUserConfig
from aiogram_dialog.widgets.text import Format
from sqlalchemy import select, and_, func

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
        stmt = select(func.count(Event.id)).where(
            and_(
                Event.date == selected_date,
                Event.moderation # True
            )
        )
        total_events = await session.scalar(stmt) or 0
        manager.dialog_data["total_events"] = total_events

        current_data = {
            "date": selected_date,
            "data": data,
        }
        if selected_date == today:
            text = self.today_text
        elif total_events > 0:
            # Чередующиеся эмодзи в зависимости от количества событий
            if 1 <= total_events <= 2:
                emoji = "🟢"  # зеленый
            elif 3 <= total_events <= 5:
                emoji = "🟡"  # желтый
            elif 6 <= total_events <= 8:
                emoji = "🟠"  # оранжевый
            elif 9 <= total_events <= 12:
                emoji = "🔴"  # красный
            else:
                emoji = "💥"  # для очень большого количества
            print(total_events)
            text = self.date_text + f" {emoji}"
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
    async def _get_user_config(
            self,
            data: dict,
            manager: DialogManager,
    ) -> CalendarUserConfig:
        return CalendarUserConfig(
            min_date=datetime.now().date(), # минимальная дата - сегодня
        )