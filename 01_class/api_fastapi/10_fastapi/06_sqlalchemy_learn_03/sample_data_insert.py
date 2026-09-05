from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, raiseload, selectinload

from app.database import engine
from app.models import Order, OrderItem, User

with Session(engine) as session:
    stmt = (
        select(User)
        .options(
            # selectinload(User.orders)
            # .selectinload(Order.items)
            # .joinedload(OrderItem.product),
            joinedload(User.orders)
            .joinedload(Order.items)
            .joinedload(OrderItem.product),

            raiseload("*"),
        )
    )

    # users = session.scalars(stmt).all()
    users = session.scalars(stmt).unique().all()

    for user in users:
        print("USER:", user.name)

        for order in user.orders:
            print("  ORDER:", order.id)

            for item in order.items:
                print(
                    "    ITEM:",
                    item.product.name,
                    item.quantity,
                    item.product.price
                )