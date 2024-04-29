import uuid
import datetime
from typing import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):  # type: ignore[misc]
    pass


class DBUser(Base):
    """"""

    __tablename__ = "user_account"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    tg_id: Mapped[int] = mapped_column(unique=True, index=True)
    username: Mapped[str] = mapped_column(String(50))

    reminders: Mapped[List["DBReminder"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return str(self.username)


class DBReminder(Base):
    """"""

    __tablename__ = "reminder"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    time: Mapped[datetime.datetime]
    text: Mapped[str] = mapped_column(String(200))
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_account.id"), nullable=False
    )

    user: Mapped["DBUser"] = relationship(back_populates="reminders")

    def __str__(self) -> str:
        return str(self.time)
