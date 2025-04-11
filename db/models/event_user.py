from sqlalchemy import Table, Column, Integer, ForeignKey

from db.base import Base

association_table = Table(
    "event_user",
    Base.metadata,
    Column("event_id", ForeignKey("events.id"), primary_key=True),
    Column("user_id", ForeignKey("users.telegram_id"), primary_key=True),
)