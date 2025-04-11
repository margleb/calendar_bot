import enum
from typing import List

from sqlalchemy import String, Text, Enum, BigInteger, Boolean, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from db.mixins import TimestampMixin
from db.models.event_user import association_table


class CityEnum(enum.Enum):
    moscow = 'Москва'
    spb = 'Санкт-Петербург'

class Event(TimestampMixin, Base):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(primary_key=True)
    # image_id: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String(50))
    # description: Mapped[str] = mapped_column(Text)
    # participants: Mapped[int] = mapped_column(Integer)
    # city: Mapped[CityEnum] = mapped_column(Enum(CityEnum, values_callable=lambda x: [e.value for e in x]))
    # date_event: Mapped[Date] = mapped_column(Date)
    # moderation: Mapped[bool] = mapped_column(Boolean, server_default='false')
    users: Mapped[List["User"]] = relationship(
        secondary=association_table, back_populates="events"
    )
    # created_at добавляется из миксина