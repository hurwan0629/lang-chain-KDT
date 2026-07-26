from sqlalchemy.orm import Session

from app.database import engine
from app.models import User, Order

user = User(name="customer1")

order1 = Order(product_name="keyboard")
order2 = Order(product_name="mouse")

user.orders.append(order1)
user.orders.append(order2)

with Session(engine) as session:

    session.add(user)

    print("order1.user exists:", bool(order1.user))
    print("order2.user exists:", bool(order2.user))

    print("session.new:", session.new)


    session.commit()