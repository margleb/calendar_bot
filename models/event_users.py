from datetime import datetime

from sqlalchemy import BigInteger, DateTime, func, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base


class EventUsers(Base):
    __tablename__ = 'event_users'


    id: Mapped[int] = mapped_column(primary_key=True)
    event_id:Mapped[int] = mapped_column(BigInteger, ForeignKey("events.id", ondelete="CASCADE"))
    tg_user_id: Mapped[int] = mapped_column(BigInteger)
    tg_username: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    event: Mapped[list["Event"]] = relationship(back_populates="users")