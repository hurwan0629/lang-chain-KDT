from datetime import datetime

from sqlalchemy import ForeignKey, String, func, DateTime, Integer, CheckConstraint, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    pk: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    id: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now()
    )

    orders: Mapped[list["Order"]] = relationship(
        back_populates="user"
    )

class Order(Base):
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
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now()
    )

    user: Mapped["User"] = relationship(
        back_populates="orders"
    )