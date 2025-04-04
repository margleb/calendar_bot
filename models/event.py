import enum
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import String, Text, Enum, DateTime, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

class CityEnum(enum.Enum):
    moscow = 'Москва'
    spb = 'Санкт-Петербург'

class Event(Base):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_user_id: Mapped[int] = mapped_column(BigInteger)
    image_id: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text)
    city: Mapped[CityEnum] = mapped_column(Enum(CityEnum, values_callable=lambda x: [e.value for e in x]))
    date: Mapped[datetime] = mapped_column(DateTime)
    username: Mapped[str] = mapped_column(String)
    moderation: Mapped[bool] = mapped_column(Boolean, server_default='false')