from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload, joinedload, raiseload

from app.database import engine
from app.models import User, Order

with Session(engine) as session:
    # stmt = (
    #     select(User)
    #     .options(
    #         selectinload(User.orders)
    #         .selectinload(Order.items)
    #     )
    # )
    #
    # users = session.scalars(stmt).all()

    # stmt = (
    #     select(User)
    #     .options(
    #         joinedload(User.orders)
    #     )
    # )
    # users = session.scalars(stmt).unique().all()

    stmt = select(User).options(
        raiseload(User.orders)
    )

    user = session.scalars(stmt).first()


    print("\n --- User 조회 완료 --- \n")
    print(" # 예측 상 다시 쿼리를 날리는 현상이 보이면 안됨 \n\n")

    print(user.name)
    print(user.orders)

    # for user in users:
    #     print("\n\n")
    #     print("user:", user.id, user.name)
    #     orders = user.orders
    #     print("orders:", orders)
    #
    #     for order in orders:
    #         order_items = order.items
    #         print("order_item:", order_items)


