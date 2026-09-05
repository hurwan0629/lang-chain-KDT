from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import engine
from app.models import User

with Session(engine) as session:
    users = session.scalars(
        select(User)
    ).all()

    print("\n --- User 조회 완료 --- \n")

    for user in users:
        print("\n\n")
        print("user:", user.id, user.name)

        print("orders [1]:", user.orders)
        print("orders [2]:", user.orders)