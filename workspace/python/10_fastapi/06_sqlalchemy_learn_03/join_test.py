from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import engine
from app.models import User, Order

with Session(engine) as session:
    # stmt = select(User, Order).join(
    #     Order,
    #     User.id == Order.user_id
    # ) # 거의 SQL의 표현 방식과 동일

    stmt = (
        select(User, Order)
        .join(Order)
    ) # FK를 통해 추론

    # stmt = (
    #     select(User, Order)
    #     .join(User.orders)
    # ) # relationship를 이용해서 sqlalchemy가 파악

    result = session.execute(stmt)

    for user, order in result:
        print(
            "id:", user.id,
            "name:", user.name,
            "id:", order.id,
            "product_name:", order.product_name,
        )