from tabnanny import check

from database.database import Base
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, func, ForeignKey, BigInteger, CheckConstraint


class Users(Base):
    __tablename__ = "users"

    pk: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    id: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=False
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    created_at:Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at:Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        server_onupdate=func.now()
    )

    def __repr__(self):
        return f"User(pk: {self.pk}, id: {self.id}, name: {self.name}, created_at: {self.created_at}, updated_at: {self.updated_at}"


class Orders(Base):
    __tablename__ = "orders"

    pk: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    user_pk: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.pk"),
        nullable=False
    )

    total_price: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("total_price >= 0"),
        nullable=False
    )

    created_at:Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at:Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        server_onupdate=func.now()
    )