import enum
from typing import List

from sqlalchemy import String, Text, Enum, BigInteger, Boolean, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from db.mixins import TimestampMixin

class CityEnum(enum.Enum):
    moscow = 'Москва'
    spb = 'Санкт-Петербург'

class Event(TimestampMixin, Base):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text)
    image_id: Mapped[str] = mapped_column(String, nullable=True)
    # participants: Mapped[int] = mapped_column(Integer)
    city: Mapped[CityEnum] = mapped_column(Enum(CityEnum, values_callable=lambda x: [e.value for e in x]))
    date_event: Mapped[Date] = mapped_column(Date)
    # moderation: Mapped[bool] = mapped_column(Boolean, server_default='false')
    username: Mapped[str] = mapped_column(Text)
    user: Mapped[List["Association"]] = relationship(back_populates="event")
    # created_at добавляется из миксина