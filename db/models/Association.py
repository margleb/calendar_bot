from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.base import Base


class Association(Base):
    __tablename__ = "association_table"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"), primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), primary_key=True)
    status: Mapped[Optional[str]] # статус (join/create)
    event: Mapped["Event"] = relationship()
    user: Mapped["User"] = relationship()