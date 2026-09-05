from sqlalchemy.orm import Session

from app.database import engine
from app.models import Order, OrderItem, Product, User

with Session(engine) as session:
    user = User(
        name="kim",
        email="kim@test.com"
    )

    order = Order(
        user=user
    )

    keyboard = Product(
        name="keyboard",
        price=50000
    )

    item1 = OrderItem(
        order=order,
        product=keyboard,
        quantity=2
    )

    mouse = Product(
        name="mouse",
        price=20000
    )

    item2 = OrderItem(
        order=order,
        product=mouse,
        quantity=1
    )

    session.add(user)

    print(" --- add 이후 --- ")
    print("session.new:", session.new)
    print("identity map:", session.identity_map.values())

    session.flush()

    print(" --- flush 이후 --- ")

    print("identity map:", session.identity_map.values())

    print("user:", user.id)
    print("order:", order.id)
    print("keyboard:", keyboard.id)
    print("mouse:", mouse.id)

    print(
        "item1:",
        item1.id,
        item1.order_id,
        item1.product_id
    )

    print(
        "item2:",
        item2.id,
        item2.order_id,
        item2.product_id
    )

    session.commit()
