from sqlalchemy.orm import Session

from app.database import engine
from app.models import User, Order

user = User(name="lee")
order = Order(product_name="monitor")

user.orders.append(order)

print("1. order.user:", order.user)
print("2. order.user is user:", order.user is user)
print("3. order.user_id:", order.user_id)

with Session(engine) as session:
    session.add(user)

    print("4. flush 이전 user.id:", user.id)
    print("5. flush 이전 order.user_id:", order.user_id)

    # DB 세션에 Python session 상태가 적용되었다고 보면 됨.
    session.flush()

    print("6. flush 이후 user.id:", user.id)
    print("7. flush 이후 order.user_id:", order.user_id)

    session.commit()

    print("8. commit 이후 order.user_id:", order.user_id)